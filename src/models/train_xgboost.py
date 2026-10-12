"""
Phase 8: XGBoost Training & Comparative Evaluation Pipeline.
Compares:
1. Best Baseline (Gradient Boosting) with Full Features
2. Best Baseline with Statistically Selected Features
3. Best Baseline with PSO Selected Features
4. XGBoost with Full Features
5. XGBoost with PSO Selected Features

Outputs:
- outputs/metrics/metrics_comparison.csv
- outputs/plots/roc_curve.png
- outputs/plots/precision_recall_curve.png
- outputs/plots/confusion_matrix.png
- outputs/feature_selection/feature_importance.csv
"""

import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import duckdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingClassifier
from xgboost import XGBClassifier

from src.config import (
    OUTPUTS_DIR,
    METRICS_DIR,
    PLOTS_DIR,
    FEATURE_SEL_DIR,
    CONFIGS_DIR,
    RANDOM_STATE,
    ensure_directories,
    get_logger,
)
from src.evaluation.evaluate import compute_metrics, plot_comparison_curves
from src.models.split_manager import get_preprocessed_features

logger = get_logger("train_xgboost")


def run_xgboost_experiments():
    """Runs Phase 8 model training and comparative evaluation on the unified holdout partition."""
    ensure_directories()

    logger.info("Loading unified leakage-free preprocessed data via split_manager...")
    prep = get_preprocessed_features(include_categoricals=False)
    X_train = prep["X_train"]
    X_holdout = prep["X_holdout"]
    y_train = prep["y_train"]
    y_holdout = prep["y_holdout"]
    candidate_cols = prep["feature_names"]
    preprocessor = prep["preprocessor"]

    # Load Feature Subsets
    pso_df = pd.read_csv(FEATURE_SEL_DIR / "pso_selected_features.csv")
    pso_cols = pso_df["feature_name"].tolist()
    pso_idx = [candidate_cols.index(c) for c in pso_cols if c in candidate_cols]

    stat_df = pd.read_csv(FEATURE_SEL_DIR / "statistical_selected_features.csv")
    stat_cols = stat_df["feature_name"].tolist()
    stat_idx = [candidate_cols.index(c) for c in stat_cols if c in candidate_cols]

    full_idx = np.arange(len(candidate_cols))

    logger.info(f"Feature dimensions: Full={len(full_idx)}, Statistical={len(stat_idx)}, PSO={len(pso_idx)}")

    # Load Search Times
    pso_search_time = 0.0
    pso_cfg_file = CONFIGS_DIR / "pso_experiment_config.json"
    if pso_cfg_file.exists():
        try:
            with open(pso_cfg_file, "r", encoding="utf-8") as f:
                pso_cfg = json.load(f)
                pso_search_time = float(pso_cfg.get("search_time_seconds", 0.0))
        except Exception:
            pso_search_time = 0.0

    stat_search_time = 0.0
    fs_comp_file = METRICS_DIR / "feature_selection_comparison.csv"
    if fs_comp_file.exists():
        try:
            fs_df = pd.read_csv(fs_comp_file)
            stat_row = fs_df[fs_df["approach"].str.contains("Statistical", na=False)]
            if not stat_row.empty:
                stat_search_time = float(stat_row["search_time_seconds"].values[0])
        except Exception:
            stat_search_time = 0.0

    # Class weighting ratio for XGBoost (imbalance in training set)
    pos_weight = float(np.sum(y_train == 0) / np.sum(y_train == 1))
    logger.info(f"Scale pos weight for XGBoost: {pos_weight:.2f}")

    # Experiments dictionary: (model, indices, feat_names, search_time)
    experiments = {
        "Baseline (Full Features)": (
            HistGradientBoostingClassifier(max_iter=100, max_depth=6, random_state=RANDOM_STATE, class_weight="balanced"),
            full_idx,
            candidate_cols,
            0.0,
        ),
        "Baseline (Statistical Features)": (
            HistGradientBoostingClassifier(max_iter=100, max_depth=6, random_state=RANDOM_STATE, class_weight="balanced"),
            stat_idx,
            stat_cols,
            stat_search_time,
        ),
        "Baseline (PSO Features)": (
            HistGradientBoostingClassifier(max_iter=100, max_depth=6, random_state=RANDOM_STATE, class_weight="balanced"),
            pso_idx,
            pso_cols,
            pso_search_time,
        ),
        "XGBoost (Full Features)": (
            XGBClassifier(
                n_estimators=150,
                max_depth=6,
                learning_rate=0.08,
                scale_pos_weight=pos_weight,
                subsample=0.85,
                colsample_bytree=0.85,
                random_state=RANDOM_STATE,
                n_jobs=-1,
                eval_metric="logloss",
            ),
            full_idx,
            candidate_cols,
            0.0,
        ),
        "XGBoost (PSO Features)": (
            XGBClassifier(
                n_estimators=150,
                max_depth=6,
                learning_rate=0.08,
                scale_pos_weight=pos_weight,
                subsample=0.85,
                colsample_bytree=0.85,
                random_state=RANDOM_STATE,
                n_jobs=-1,
                eval_metric="logloss",
            ),
            pso_idx,
            pso_cols,
            pso_search_time,
        ),
    }

    results = []
    eval_curves_data = {}
    fitted_models = {}

    for exp_name, (model, indices, feat_names, search_time) in experiments.items():
        logger.info(f"Training experiment: {exp_name} ({len(indices)} features)...")
        X_tr = X_train[:, indices]
        X_ho = X_holdout[:, indices]

        t0 = time.time()
        model.fit(X_tr, y_train)
        fit_time = round(time.time() - t0, 2)

        probs = model.predict_proba(X_ho)[:, 1]
        metrics = compute_metrics(
            y_true=y_holdout,
            y_prob=probs,
            model_name=exp_name,
            feature_count=len(indices),
            fit_time=fit_time,
        )
        metrics["search_time_seconds"] = search_time
        metrics["fit_time_seconds"] = fit_time
        metrics["total_time_seconds"] = round(search_time + fit_time, 2)
        metrics["split_id"] = "stratified_80_20_v1"
        metrics["evaluation_set"] = "holdout_32k"
        metrics["feature_space"] = f"{len(indices)}_features"
        results.append(metrics)
        fitted_models[exp_name] = model

        # Data for curves
        y_pred = (probs >= metrics["threshold"]).astype(int)
        eval_curves_data[exp_name] = {
            "y_true": y_holdout,
            "y_prob": probs,
            "y_pred": y_pred,
        }

        logger.info(
            f"[{exp_name}] PR-AUC: {metrics['pr_auc']:.4f} | ROC-AUC: {metrics['roc_auc']:.4f} | "
            f"F1: {metrics['f1_score']:.4f} | Search: {search_time:.2f}s | Fit: {fit_time:.2f}s | Total: {metrics['total_time_seconds']:.2f}s"
        )

    # 1. Save metrics comparison
    comparison_df = pd.DataFrame(results)
    out_csv = METRICS_DIR / "metrics_comparison.csv"
    comparison_df.to_csv(out_csv, index=False)
    logger.info(f"Saved comprehensive metrics comparison to {out_csv}")

    # 2. Plot ROC, PR, and Confusion Matrix curves
    plot_comparison_curves(eval_curves_data, output_dir=PLOTS_DIR)

    # 3. XGBoost Feature Importance
    xgb_full = fitted_models["XGBoost (Full Features)"]
    importances = xgb_full.feature_importances_
    feat_imp_df = pd.DataFrame({
        "feature_name": candidate_cols,
        "importance_weight": importances,
    }).sort_values("importance_weight", ascending=False)

    feat_imp_path = FEATURE_SEL_DIR / "feature_importance.csv"
    feat_imp_df.to_csv(feat_imp_path, index=False)
    logger.info(f"Saved XGBoost feature importance to {feat_imp_path}")

    # Plot top 20 Feature Importance chart
    plt.figure(figsize=(10, 7))
    top20 = feat_imp_df.head(20).sort_values("importance_weight", ascending=True)
    plt.barh(top20["feature_name"], top20["importance_weight"], color="#4C72B0", edgecolor="black", alpha=0.85)
    plt.title("Top 20 Features by XGBoost Importance Weight", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Relative Importance Weight", fontsize=11)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "xgboost_feature_importance.png", dpi=200)
    plt.close()
    logger.info("Saved xgboost_feature_importance.png")

    # 4. Generate Final Predictions for test.csv (Phase 9 / Final Pipeline)
    logger.info("Generating test set predictions with final XGBoost model...")
    con = duckdb.connect()
    parquet_path = OUTPUTS_DIR / "customer_features.parquet"
    test_df = con.execute(
        f"""
        SELECT * 
        FROM read_parquet('{parquet_path.as_posix()}')
        WHERE split_type = 'test'
        ORDER BY customer_id
        """
    ).df()

    X_test_scaled = preprocessor.transform(test_df[candidate_cols])
    test_probs = xgb_full.predict_proba(X_test_scaled)[:, 1]

    # Save test submission matching sample_submission.csv format
    sub_df = pd.DataFrame({
        "customer_id": test_df["customer_id"],
        "target": (test_probs >= 0.5).astype(int),
        "purchase_probability": np.round(test_probs, 4),
    })
    sub_path = OUTPUTS_DIR / "test_predictions.csv"
    sub_df[["customer_id", "target"]].to_csv(sub_path, index=False)
    logger.info(f"Saved final test predictions for {len(sub_df):,} customers to {sub_path}")

    return comparison_df, feat_imp_df


if __name__ == "__main__":
    run_xgboost_experiments()
