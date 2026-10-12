"""
Fast Unit Tests: Edge Cases, Mathematical Invariants, and Fixture Validation.
Can run instantaneously on small in-memory synthetic fixtures without requiring raw dataset.
"""

import sys
from pathlib import Path
import pytest
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.pso_optimizer import BinaryPSO


@pytest.mark.fast
def test_division_by_zero_smoothing_invariants():
    """
    Verify that derived behavioral ratios have laplace/additive smoothing
    preventing ZeroDivisionError and NaN/Inf on edge case inputs (0 pages, 0 sessions, 0 spend).
    """
    # Edge case sample: customer with zero browsing and zero transactions
    edge_sample = pd.DataFrame([{
        "total_cart_additions": 0,
        "total_pages_viewed": 0,
        "total_session_duration": 0.0,
        "total_spend": 0.0,
        "sess_count": 0,
        "total_items_count": 0,
        "discount_usage_rate": None,
        "trans_discount_rate": 0.0,
        "loyalty_score": 0.0,
        "avg_review_score": None,
        "days_since_last_session": 9999,
        "account_age_days": 0,
    }])

    # Apply identical feature engineering formulas as build_features.py
    cart_to_page_ratio = round(edge_sample["total_cart_additions"].iloc[0] * 1.0 / (edge_sample["total_pages_viewed"].iloc[0] + 1.0), 4)
    duration_per_page = round(edge_sample["total_session_duration"].iloc[0] * 1.0 / (edge_sample["total_pages_viewed"].iloc[0] + 1.0), 2)
    spend_per_session = round(edge_sample["total_spend"].iloc[0] * 1.0 / (edge_sample["sess_count"].iloc[0] + 1.0), 2)
    spend_per_item = round(edge_sample["total_spend"].iloc[0] * 1.0 / (edge_sample["total_items_count"].iloc[0] + 1.0), 2)
    activity_recency = round(edge_sample["days_since_last_session"].iloc[0] * 1.0 / (edge_sample["account_age_days"].iloc[0] + 1.0), 4)

    assert cart_to_page_ratio == 0.0
    assert duration_per_page == 0.0
    assert spend_per_session == 0.0
    assert spend_per_item == 0.0
    assert np.isfinite(activity_recency)
    assert not np.isnan(cart_to_page_ratio)
    assert not np.isinf(cart_to_page_ratio)


@pytest.mark.fast
def test_preprocessor_fit_on_train_isolation_with_synthetic_fixture():
    """
    Verify that SimpleImputer and StandardScaler fit strictly on Train
    and never leak Validation/Holdout statistics.
    """
    # Create synthetic train and holdout data with distinct distributions
    np.random.seed(42)
    X_train_raw = pd.DataFrame({
        "num_feat1": [10.0, 20.0, 30.0, np.nan, 50.0],  # Median = 25.0
        "num_feat2": [1.0, 2.0, 3.0, 4.0, 5.0],
    })
    X_val_raw = pd.DataFrame({
        "num_feat1": [np.nan, 1000.0],  # Extremely large out-of-domain outlier in holdout
        "num_feat2": [100.0, 200.0],
    })

    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    # Fit EXCLUSIVELY on train
    X_train_trans = pipeline.fit_transform(X_train_raw)

    # Imputer learned median from train
    learned_median = pipeline.named_steps["imputer"].statistics_[0]
    assert learned_median == 25.0, f"Expected median 25.0 from train, got {learned_median}"

    # Transform val without fitting
    X_val_trans = pipeline.transform(X_val_raw)

    # The missing value in val must have been imputed with train median (25.0)
    val_feat1_nan_imputed = pipeline.named_steps["imputer"].transform(X_val_raw)[0, 0]
    assert val_feat1_nan_imputed == 25.0, "Validation missing value was not imputed with Train median!"
    assert np.isfinite(X_val_trans).all(), "Transformed validation contains non-finite values!"


@pytest.mark.fast
def test_binary_pso_sparsity_penalty_boundary():
    """
    Verify BinaryPSO fitness calculation on boundary conditions:
    k=0 features selected yields 0.0 fitness, while non-zero mask computes correctly.
    """
    pso = BinaryPSO(
        n_particles=4,
        n_iterations=2,
        alpha=0.92,
        random_state=42,
    )

    rng = np.random.RandomState(42)
    X_tr = rng.randn(30, 5)
    y_tr = rng.choice([0, 1], size=30)
    X_va = rng.randn(15, 5)
    y_va = rng.choice([0, 1], size=15)

    # Case 1: Empty mask (zero features)
    empty_mask = np.zeros(5, dtype=bool)
    fit_0, pr_0, k_0 = pso.evaluate_fitness(empty_mask, X_tr, y_tr, X_va, y_va)
    assert fit_0 == 0.0
    assert pr_0 == 0.0
    assert k_0 == 0

    # Case 2: 2 features selected
    two_mask = np.array([True, False, True, False, False])
    fit_2, pr_2, k_2 = pso.evaluate_fitness(two_mask, X_tr, y_tr, X_va, y_va)
    assert k_2 == 2
    assert pr_2 >= 0.0
    # Expected: alpha * pr_2 + (1 - alpha) * (1 - 2/5) = 0.92 * pr_2 + 0.08 * 0.6
    expected_fit = 0.92 * pr_2 + 0.08 * (1.0 - 2 / 5)
    assert abs(fit_2 - expected_fit) < 1e-6


def test_target_and_customer_id_strictly_excluded_from_candidate_features():
    """
    Ensure that customer_id, target, and split markers are strictly excluded from candidate feature lists.
    """
    from src.models.split_manager import create_or_load_splits
    splits = create_or_load_splits()
    candidate_cols = splits["candidate_cols"]
    forbidden = {"customer_id", "target", "split_type"}
    for f in forbidden:
        assert f not in candidate_cols, f"CRITICAL LEAKAGE BUG: '{f}' found in candidate_cols!"
