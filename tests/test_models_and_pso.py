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
    assert len(c_df) >= 4, f"Expected at least 4 compared models, got {len(c_df)}"

    pso_sel = FEATURE_SEL_DIR / "pso_selected_features.csv"
    assert pso_sel.exists(), "pso_selected_features.csv missing!"
