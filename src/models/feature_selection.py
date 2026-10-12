"""
Phase 7: Feature Selection Comparative Analysis.
Compares:
A. Full Candidate Features
B. Statistically Selected Features (SelectKBest ANOVA F-score)
C. Binary PSO Selected Features
Exports feature_selection_comparison.csv.
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
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import HistGradientBoostingClassifier

from src.config import (
    OUTPUTS_DIR,
    FEATURE_SEL_DIR,
    METRICS_DIR,
    CONFIGS_DIR,
    RANDOM_STATE,
    ensure_directories,
    get_logger,
)
from src.evaluation.evaluate import compute_metrics
from src.models.split_manager import get_preprocessed_features
from src.models.pso_optimizer import run_pso_optimization

logger = get_logger("feature_selection")


def run_feature_selection_comparison():
    """Runs comparative evaluation between Full vs Statistical vs PSO features on the unified holdout partition."""
    ensure_directories()

    logger.info("Loading unified leakage-free preprocessed data via split_manager...")
    prep = get_preprocessed_features(include_categoricals=False)
    X_train = prep["X_train"]
    X_holdout = prep["X_holdout"]
    y_train = prep["y_train"]
    y_holdout = prep["y_holdout"]
    candidate_cols = prep["feature_names"]

    # 1. Run PSO (or load existing results)
    pso_file = FEATURE_SEL_DIR / "pso_selected_features.csv"
    pso_cfg_file = CONFIGS_DIR / "pso_experiment_config.json"
    pso_search_time = 0.0

    if not pso_file.exists() or not pso_cfg_file.exists():
        logger.info("Running PSO feature optimizer on inner tuning partition...")
        pso_res = run_pso_optimization()
        pso_selected_cols = pso_res["selected_features"]
        pso_search_time = pso_res["search_time_seconds"]
    else:
        logger.info(f"Loading existing PSO selected features from {pso_file}...")
        pso_df = pd.read_csv(pso_file)
        pso_selected_cols = pso_df["feature_name"].tolist()
        try:
            with open(pso_cfg_file, "r", encoding="utf-8") as f:
                pso_cfg = json.load(f)
                pso_search_time = float(pso_cfg.get("search_time_seconds", 0.0))
        except Exception:
            pso_search_time = 0.0

    pso_indices = [candidate_cols.index(c) for c in pso_selected_cols if c in candidate_cols]
    k_pso = len(pso_indices)
    logger.info(f"PSO selected {k_pso} features out of {len(candidate_cols)} candidate features (Search time: {pso_search_time:.2f}s).")

    # 2. Statistical Selection (SelectKBest matching PSO's k, strictly fit on X_train)
    t0_stat = time.time()
    selector = SelectKBest(score_func=f_classif, k=k_pso)
    selector.fit(X_train, y_train)
    stat_search_time = round(time.time() - t0_stat, 2)
    stat_indices = np.where(selector.get_support())[0]
    stat_selected_cols = [candidate_cols[i] for i in stat_indices]

    # Save statistically selected features
    stat_df = pd.DataFrame({
        "feature_name": stat_selected_cols,
        "is_selected": 1,
    })
    stat_df.to_csv(FEATURE_SEL_DIR / "statistical_selected_features.csv", index=False)
    logger.info(f"Statistical ANOVA selected {len(stat_indices)} features (Search time: {stat_search_time:.2f}s).")

    # 3. Evaluate on Unified Holdout Set
    comparison_results = []
    approaches = [
        ("A. Full Feature Set", np.arange(len(candidate_cols)), candidate_cols, 0.0),
        ("B. Statistical Selection (ANOVA F-test)", stat_indices, stat_selected_cols, stat_search_time),
        ("C. Binary PSO Optimization", pso_indices, pso_selected_cols, pso_search_time),
    ]

    for label, indices, cols, search_time in approaches:
        logger.info(f"Evaluating: {label} ({len(indices)} features)...")
        X_tr_sub = X_train[:, indices]
        X_ho_sub = X_holdout[:, indices]

        # Model: HistGradientBoosting
        start_fit = time.time()
        clf = HistGradientBoostingClassifier(
            max_iter=80, max_depth=6, random_state=RANDOM_STATE, class_weight="balanced"
        )
        clf.fit(X_tr_sub, y_train)
        fit_time = round(time.time() - start_fit, 2)

        probs = clf.predict_proba(X_ho_sub)[:, 1]
        metrics = compute_metrics(
            y_true=y_holdout,
            y_prob=probs,
            model_name=label,
            feature_count=len(indices),
            fit_time=fit_time,
        )
        metrics["approach"] = label
        metrics["search_time_seconds"] = search_time
        metrics["fit_time_seconds"] = fit_time
        metrics["total_time_seconds"] = round(search_time + fit_time, 2)
        metrics["split_id"] = "stratified_80_20_v1"
        metrics["evaluation_set"] = "holdout_32k"
        metrics["feature_space"] = f"{len(indices)}_features"
        comparison_results.append(metrics)

        logger.info(
            f"[{label}] PR-AUC: {metrics['pr_auc']:.4f} | ROC-AUC: {metrics['roc_auc']:.4f} | "
            f"Search: {search_time:.2f}s | Fit: {fit_time:.2f}s | Total: {metrics['total_time_seconds']:.2f}s"
        )

    comp_df = pd.DataFrame(comparison_results)
    out_path = METRICS_DIR / "feature_selection_comparison.csv"
    comp_df.to_csv(out_path, index=False)
    logger.info(f"Saved feature selection comparison to {out_path}")

    return comp_df, pso_selected_cols, stat_selected_cols


if __name__ == "__main__":
    run_feature_selection_comparison()
