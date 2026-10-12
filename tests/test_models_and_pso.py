"""
Unit and Integration Tests: Phase 5-8 Baseline Models, Metrics & Binary PSO.
"""

import sys
from pathlib import Path
import pytest
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.evaluate import compute_metrics
from src.models.pso_optimizer import BinaryPSO
from src.config import METRICS_DIR, FEATURE_SEL_DIR


def test_compute_metrics_accuracy():
    """Verify that compute_metrics produces valid bounded numbers and all expected fields."""
    y_true = np.array([0, 0, 1, 1, 0, 1, 0, 0, 1, 0])
    y_prob = np.array([0.1, 0.2, 0.8, 0.9, 0.3, 0.7, 0.4, 0.2, 0.6, 0.1])

    res = compute_metrics(y_true, y_prob, model_name="UnitTestModel", feature_count=5, fit_time=0.1)

    assert "pr_auc" in res
    assert "roc_auc" in res
    assert "f1_score" in res
    assert "precision" in res
    assert "recall" in res
    assert 0.0 <= res["pr_auc"] <= 1.0
    assert 0.0 <= res["roc_auc"] <= 1.0
    assert 0.0 <= res["f1_score"] <= 1.0
    assert res["true_positives"] + res["false_negatives"] == 4  # Total positives


def test_binary_pso_toy_convergence():
    """Verify Binary PSO runs on synthetic data, enforces valid binary masks, and converges."""
    rng = np.random.RandomState(42)
    # Synthetic data: 100 samples, 8 features (first 2 features contain signal, remaining 6 noise)
    X = rng.randn(100, 8)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    feat_names = [f"feat_{i}" for i in range(8)]

    pso = BinaryPSO(n_particles=6, n_iterations=4, alpha=0.9, random_state=42)
    res = pso.optimize(X[:70], y[:70], X[70:], y[70:], feat_names)

    assert res["gbest_fitness"] > 0
    assert 1 <= res["gbest_n_features"] <= 8
    assert len(res["history"]) == 5  # Iteration 0 (Init) + 4 iterations
    assert len(res["selected_features"]) == res["gbest_n_features"]


def test_output_metrics_files_exist():
    """Verify that final benchmark and comparison metrics CSV files exist and have valid entries."""
    baseline_csv = METRICS_DIR / "baseline_metrics.csv"
    assert baseline_csv.exists(), "baseline_metrics.csv missing!"
    b_df = pd.read_csv(baseline_csv)
    assert len(b_df) == 7, f"Expected 7 baseline models in baseline_metrics.csv, got {len(b_df)}"

    comp_csv = METRICS_DIR / "metrics_comparison.csv"
    assert comp_csv.exists(), "metrics_comparison.csv missing!"
    c_df = pd.read_csv(comp_csv)
    assert len(c_df) == 5, f"Expected 5 compared models in metrics_comparison.csv, got {len(c_df)}"

    pso_sel = FEATURE_SEL_DIR / "pso_selected_features.csv"
    assert pso_sel.exists(), "pso_selected_features.csv missing!"


def test_split_consistency_and_holdout_isolation():
    """Verify that split indices are disjoint and holdout is strictly isolated from inner tuning."""
    from src.config import CONFIGS_DIR, OUTPUTS_DIR
    import json

    split_npz = OUTPUTS_DIR / "processed" / "split_indices.npz"
    assert split_npz.exists(), "split_indices.npz missing!"
    data = np.load(split_npz)

    train_idx = data["train_idx"]
    holdout_idx = data["holdout_idx"]
    inner_tr = data["pso_inner_train_idx"]
    inner_va = data["pso_inner_val_idx"]

    assert len(train_idx) == 128000, f"Expected 128000 train samples, got {len(train_idx)}"
    assert len(holdout_idx) == 32000, f"Expected 32000 holdout samples, got {len(holdout_idx)}"

    # Check zero overlap between train and holdout
    train_set = set(train_idx)
    holdout_set = set(holdout_idx)
    assert len(train_set.intersection(holdout_set)) == 0, "Data leakage detected: train and holdout overlap!"

    # Check inner tuning partitions are strictly subsets of train_idx
    assert set(inner_tr).issubset(train_set), "Inner train must be a strict subset of train_idx"
    assert set(inner_va).issubset(train_set), "Inner val must be a strict subset of train_idx"

    # Check inner tuning NEVER touches holdout
    assert len(set(inner_tr).intersection(holdout_set)) == 0, "Holdout leakage in PSO inner train!"
    assert len(set(inner_va).intersection(holdout_set)) == 0, "Holdout leakage in PSO inner val!"

    # Check metadata consistency
    meta_path = CONFIGS_DIR / "split_metadata.json"
    assert meta_path.exists(), "split_metadata.json missing!"
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    assert meta["train_size"] == 128000
    assert meta["holdout_size"] == 32000
    assert meta["split_id"] == "stratified_80_20_v1"


def test_metrics_comparison_metadata_and_threshold():
    """Verify that all models in metrics_comparison.csv share identical evaluation design and fixed threshold."""
    comp_csv = METRICS_DIR / "metrics_comparison.csv"
    df = pd.read_csv(comp_csv)

    for _, row in df.iterrows():
        assert row["split_id"] == "stratified_80_20_v1", f"Inconsistent split_id for {row['model_name']}"
        assert row["evaluation_set"] == "holdout_32k", f"Inconsistent evaluation_set for {row['model_name']}"
        assert row["threshold"] == 0.5, f"Optimistic threshold used instead of standard 0.5 for {row['model_name']}"
        assert row["threshold_source"] == "fixed_0.5"
        assert row["search_time_seconds"] >= 0.0
        assert row["fit_time_seconds"] > 0.0
        assert round(row["total_time_seconds"], 2) == round(row["search_time_seconds"] + row["fit_time_seconds"], 2)


def test_pso_experiment_search_cost_accounting():
    """Verify that PSO experiment records fitness, search cost, evaluations, and sparsity trade-off."""
    from src.config import CONFIGS_DIR
    import json

    cfg_path = CONFIGS_DIR / "pso_experiment_config.json"
    assert cfg_path.exists(), "pso_experiment_config.json missing!"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    assert "search_time_seconds" in cfg and cfg["search_time_seconds"] > 0.0
    assert "n_evaluations" in cfg and cfg["n_evaluations"] > 0
    assert "n_unique_masks" in cfg and cfg["n_unique_masks"] > 0
    assert cfg["n_evaluations"] >= cfg["n_unique_masks"]
    assert "alpha_pr_weight" in cfg and cfg["alpha_pr_weight"] == 0.92
    assert "sparsity_reduction_pct" in cfg and cfg["sparsity_reduction_pct"] > 50.0


def test_feature_selection_comparison_fairness():
    """Verify that feature selection comparison matches k between Statistical and PSO on identical holdout."""
    fs_csv = METRICS_DIR / "feature_selection_comparison.csv"
    assert fs_csv.exists(), "feature_selection_comparison.csv missing!"
    df = pd.read_csv(fs_csv)

    assert len(df) == 3, f"Expected 3 approaches, got {len(df)}"
    stat_row = df[df["approach"].str.contains("Statistical")].iloc[0]
    pso_row = df[df["approach"].str.contains("PSO")].iloc[0]

    assert stat_row["feature_count"] == pso_row["feature_count"], "Statistical and PSO must compare at identical k!"
    assert stat_row["search_time_seconds"] >= 0.0
    assert pso_row["search_time_seconds"] > 0.0
    assert pso_row["search_time_seconds"] > stat_row["search_time_seconds"]
