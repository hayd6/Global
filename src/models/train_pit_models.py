"""
src/models/train_pit_models.py
Executes Point-in-Time Model Training, ANOVA & Binary PSO Feature Selection,
and Holdout Evaluation on Controlled Benchmark Dataset.
Guarantees:
- Preprocessors fit EXCLUSIVELY on Train partition (20,000 samples).
- Holdout partition (5,000 samples) evaluated strictly without leakage.
- ANOVA and PSO run strictly on Train / Inner Train tuning splits.
- Compares Full vs ANOVA vs PSO on Holdout with complete confusion matrices.
- Checks whether PSO & ANOVA successfully reject artificial noise variables.
"""

import sys
import os
import time
import json
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    confusion_matrix,
)
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

from src.config import OUTPUTS_DIR, RANDOM_STATE, get_logger
from src.models.pso_optimizer import BinaryPSO

logger = get_logger("train_pit_models")
BENCHMARK_DIR = OUTPUTS_DIR / "controlled_benchmark"


def compute_metrics_dict(y_true, y_prob, model_name, feature_count, fit_time, search_time=0.0):
    y_prob = np.clip(y_prob, 1e-7, 1.0 - 1e-7)
    roc_auc = float(roc_auc_score(y_true, y_prob))
    pr_auc = float(average_precision_score(y_true, y_prob))
    y_pred = (y_prob >= 0.50).astype(int)

    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    precision = float(precision_score(y_true, y_pred, zero_division=0))
    recall = float(recall_score(y_true, y_pred, zero_division=0))
    accuracy = float(accuracy_score(y_true, y_pred))
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    return {
        "model_name": model_name,
        "feature_count": feature_count,
        "pr_auc": round(pr_auc, 4),
        "roc_auc": round(roc_auc, 4),
        "f1_score": round(f1, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "accuracy": round(accuracy, 4),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "fit_time_seconds": round(fit_time, 2),
        "search_time_seconds": round(search_time, 2),
        "total_time_seconds": round(fit_time + search_time, 2),
    }


def run_point_in_time_experiments() -> dict:
    """Executes the full machine learning and PSO evaluation on the PIT dataset."""
    logger.info("Loading Point-in-Time customer features from Parquet...")
    parquet_path = BENCHMARK_DIR / "customer_features_pit.parquet"
    df = pd.read_parquet(parquet_path)

    split_npz = BENCHMARK_DIR / "split_indices_pit.npz"
    split_data = np.load(split_npz)
    train_idx = split_data["train_idx"]
    holdout_idx = split_data["holdout_idx"]

    # Candidate feature columns (dropping IDs, split flags, target)
    drop_cols = ["customer_id", "split_type", "target"]
    candidate_cols = [c for c in df.columns if c not in drop_cols]

    cat_cols = ["country_code", "region", "customer_tier", "region_tier"]
    num_cols = [c for c in candidate_cols if c not in cat_cols]

    y = df["target"].values
    y_train = y[train_idx]
    y_holdout = y[holdout_idx]

    logger.info(f"Candidate Features: {len(candidate_cols)} total ({len(num_cols)} continuous, {len(cat_cols)} categorical).")

    # 1. Pipeline for 7 Baselines (with One-Hot categoricals)
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    full_preprocessor = ColumnTransformer([
        ("num", num_pipeline, num_cols),
        ("cat", cat_pipeline, cat_cols),
    ])

    X_train_full = full_preprocessor.fit_transform(df[candidate_cols].iloc[train_idx])
    X_holdout_full = full_preprocessor.transform(df[candidate_cols].iloc[holdout_idx])

    # 2. Pipeline for Continuous Features (for PSO, ANOVA, and E1-E5)
    cont_preprocessor = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    X_train_cont = cont_preprocessor.fit_transform(df[num_cols].iloc[train_idx])
    X_holdout_cont = cont_preprocessor.transform(df[num_cols].iloc[holdout_idx])

    # -------------------------------------------------------------
    # 3. Benchmark 7 Baseline Models on Full Preprocessed Features
    # -------------------------------------------------------------
    logger.info("Training and evaluating 7 Baseline Models on Holdout...")
    baselines_def = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, class_weight="balanced"),
        "Naive Bayes": GaussianNB(),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, min_samples_leaf=30, random_state=RANDOM_STATE, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=20, random_state=RANDOM_STATE, n_jobs=-1, class_weight="balanced"),
        "Gradient Boosting": HistGradientBoostingClassifier(max_iter=100, max_depth=6, random_state=RANDOM_STATE, class_weight="balanced"),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=9, n_jobs=-1),
        "SGDClassifier (log_loss)": SGDClassifier(loss="log_loss", penalty="l2", alpha=1e-4, max_iter=1000, random_state=RANDOM_STATE, class_weight="balanced"),
    }

    baseline_metrics = []
    for b_name, b_model in baselines_def.items():
        t0 = time.time()
        b_model.fit(X_train_full, y_train)
        fit_t = time.time() - t0
        probs = b_model.predict_proba(X_holdout_full)[:, 1]
        m = compute_metrics_dict(y_holdout, probs, b_name, X_train_full.shape[1], fit_t)
        baseline_metrics.append(m)

    df_baselines = pd.DataFrame(baseline_metrics)
    df_baselines.to_csv(BENCHMARK_DIR / "baseline_metrics_pit.csv", index=False)
    logger.info(f"Saved baseline metrics ({len(df_baselines)} models) to baseline_metrics_pit.csv")

    # -------------------------------------------------------------
    # 4. Binary PSO & ANOVA Feature Selection
    # -------------------------------------------------------------
    logger.info("Running Binary PSO on Inner Train Tuning Split...")
    # Subsample 15,000 inner train, 5,000 inner val from train partition only
    inner_tr_idx = np.arange(15000)
    inner_va_idx = np.arange(15000, 20000)

    pso = BinaryPSO(n_particles=16, n_iterations=12, w=0.729, c1=1.494, c2=1.494, alpha=0.90, random_state=RANDOM_STATE)
    pso_res = pso.optimize(
        X_train_cont[inner_tr_idx], y_train[inner_tr_idx],
        X_train_cont[inner_va_idx], y_train[inner_va_idx],
        num_cols
    )
    pso_search_time = pso_res["search_time_seconds"]
    pso_selected_cols = pso_res["selected_features"]
    pso_selected_idx = pso_res["selected_indices"]
    k_pso = len(pso_selected_idx)
    logger.info(f"PSO Selected {k_pso}/{len(num_cols)} features in {pso_search_time:.2f}s (Fitness={pso_res['gbest_fitness']:.4f}).")

    # Save PSO selected features and convergence
    pd.DataFrame({"feature_name": pso_selected_cols, "is_selected": 1}).to_csv(BENCHMARK_DIR / "pso_selected_features_pit.csv", index=False)
    pd.DataFrame(pso_res["history"]).to_csv(BENCHMARK_DIR / "pso_convergence_pit.csv", index=False)

    # Statistical Selection (ANOVA SelectKBest with exact same k)
    t0_stat = time.time()
    selector = SelectKBest(score_func=f_classif, k=k_pso)
    selector.fit(X_train_cont, y_train)
    stat_search_time = round(time.time() - t0_stat, 2)
    stat_selected_idx = np.where(selector.get_support())[0]
    stat_selected_cols = [num_cols[i] for i in stat_selected_idx]
    logger.info(f"ANOVA Selected {len(stat_selected_idx)} features in {stat_search_time:.2f}s.")
    pd.DataFrame({"feature_name": stat_selected_cols, "is_selected": 1}).to_csv(BENCHMARK_DIR / "statistical_selected_features_pit.csv", index=False)

    # Check Noise Variable Rejection
    noise_vars = {"noise_customer_0", "noise_customer_1", "noise_customer_2", "noise_customer_3", "noise_customer_4", "avg_noise_trans_0", "avg_noise_trans_1"}
    pso_noise_selected = set(pso_selected_cols).intersection(noise_vars)
    stat_noise_selected = set(stat_selected_cols).intersection(noise_vars)
    logger.info(f"Noise rejection check: PSO kept {len(pso_noise_selected)}/{len(noise_vars)} noise vars ({pso_noise_selected}).")
    logger.info(f"Noise rejection check: ANOVA kept {len(stat_noise_selected)}/{len(noise_vars)} noise vars ({stat_noise_selected}).")

    # -------------------------------------------------------------
    # 5. Core Experiments E1 - E5 on Holdout (5,000 samples)
    # -------------------------------------------------------------
    logger.info("Executing 5 Core Comparative Experiments E1 - E5 on Holdout...")
    pos_weight = float(np.sum(y_train == 0) / np.sum(y_train == 1))

    experiments = {
        "E1 (Baseline Full Features)": (
            HistGradientBoostingClassifier(max_iter=100, max_depth=6, random_state=RANDOM_STATE, class_weight="balanced"),
            np.arange(len(num_cols)),
            0.0,
        ),
        "E2 (Baseline ANOVA Features)": (
            HistGradientBoostingClassifier(max_iter=100, max_depth=6, random_state=RANDOM_STATE, class_weight="balanced"),
            stat_selected_idx,
            stat_search_time,
        ),
        "E3 (Baseline PSO Features)": (
            HistGradientBoostingClassifier(max_iter=100, max_depth=6, random_state=RANDOM_STATE, class_weight="balanced"),
            pso_selected_idx,
            pso_search_time,
        ),
        "E4 (XGBoost Full Features)": (
            XGBClassifier(n_estimators=120, max_depth=5, learning_rate=0.08, scale_pos_weight=pos_weight, subsample=0.85, colsample_bytree=0.85, random_state=RANDOM_STATE, n_jobs=-1, eval_metric="logloss"),
            np.arange(len(num_cols)),
            0.0,
        ),
        "E5 (XGBoost PSO Features)": (
            XGBClassifier(n_estimators=120, max_depth=5, learning_rate=0.08, scale_pos_weight=pos_weight, subsample=0.85, colsample_bytree=0.85, random_state=RANDOM_STATE, n_jobs=-1, eval_metric="logloss"),
            pso_selected_idx,
            pso_search_time,
        ),
    }

    comp_metrics = []
    e4_holdout_predictions = None

    for exp_id, (model, indices, s_time) in experiments.items():
        X_tr = X_train_cont[:, indices]
        X_ho = X_holdout_cont[:, indices]

        t0 = time.time()
        model.fit(X_tr, y_train)
        fit_t = time.time() - t0

        probs = model.predict_proba(X_ho)[:, 1]
        m = compute_metrics_dict(y_holdout, probs, exp_id, len(indices), fit_t, s_time)
        comp_metrics.append(m)

        if "E4" in exp_id:
            e4_holdout_predictions = probs

        logger.info(f"[{exp_id}] PR-AUC: {m['pr_auc']:.4f} | ROC-AUC: {m['roc_auc']:.4f} | F1: {m['f1_score']:.4f} | Fit: {m['fit_time_seconds']:.2f}s | Search: {m['search_time_seconds']:.2f}s")

    df_comp = pd.DataFrame(comp_metrics)
    df_comp.to_csv(BENCHMARK_DIR / "metrics_comparison_pit.csv", index=False)
    logger.info(f"Saved E1-E5 metrics comparison to metrics_comparison_pit.csv")

    # -------------------------------------------------------------
    # 6. Save Holdout Prediction Artifact & Metadata
    # -------------------------------------------------------------
    holdout_cust_ids = df["customer_id"].iloc[holdout_idx].values
    y_pred_e4 = (e4_holdout_predictions >= 0.50).astype(int)
    error_groups = np.select(
        [
            (y_holdout == 1) & (y_pred_e4 == 1),
            (y_holdout == 0) & (y_pred_e4 == 0),
            (y_holdout == 0) & (y_pred_e4 == 1),
            (y_holdout == 1) & (y_pred_e4 == 0),
        ],
        ["TP", "TN", "FP", "FN"],
        default="UNKNOWN",
    )

    df_holdout_art = pd.DataFrame({
        "customer_id": holdout_cust_ids,
        "y_true": y_holdout,
        "y_proba": np.round(e4_holdout_predictions, 5),
        "y_pred": y_pred_e4,
        "error_group": error_groups,
    })
    holdout_csv_path = BENCHMARK_DIR / "holdout_predictions_pit.csv"
    df_holdout_art.to_csv(holdout_csv_path, index=False)

    tn_e4, fp_e4, fn_e4, tp_e4 = confusion_matrix(y_holdout, y_pred_e4).ravel()
    holdout_meta = {
        "artifact_name": "holdout_predictions_pit.csv",
        "benchmark_dataset": "Controlled Synthetic Benchmark",
        "cutoff_date": "2024-06-01",
        "prediction_window": "30 days (2024-06-01 to 2024-07-01)",
        "total_holdout_samples": len(df_holdout_art),
        "model_name": "XGBoost (Full Features)",
        "threshold": 0.50,
        "confusion_matrix": {
            "true_negatives": int(tn_e4),
            "false_positives": int(fp_e4),
            "false_negatives": int(fn_e4),
            "true_positives": int(tp_e4),
        },
        "metrics": {
            "pr_auc": float(average_precision_score(y_holdout, e4_holdout_predictions)),
            "roc_auc": float(roc_auc_score(y_holdout, e4_holdout_predictions)),
            "f1_score": float(f1_score(y_holdout, y_pred_e4)),
            "accuracy": float(accuracy_score(y_holdout, y_pred_e4)),
        },
        "pso_noise_rejected_count": len(noise_vars) - len(pso_noise_selected),
        "total_noise_variables": len(noise_vars),
        "holdout_sha256": hashlib.sha256(holdout_csv_path.read_bytes()).hexdigest(),
    }
    with open(BENCHMARK_DIR / "holdout_metadata_pit.json", "w", encoding="utf-8") as f:
        json.dump(holdout_meta, f, indent=4)

    logger.info("Point-in-Time Model training and PSO verification completed successfully!")
    return {
        "df_comp": df_comp,
        "df_baselines": df_baselines,
        "holdout_meta": holdout_meta,
    }


if __name__ == "__main__":
    run_point_in_time_experiments()
