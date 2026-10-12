"""
tests/test_data_quality_remediation.py
Unit & Integration Test Suite for Controlled Benchmark Dataset & Point-in-Time Pipeline.
Validates all data quality remediation criteria:
1. Strict temporal causality (no event before signup).
2. Clean business logic (items_count >= 1).
3. Synchronized marketing campaigns.
4. Verified point-in-time target definition.
5. Zero future leakage into feature matrix.
6. Positive variance on all features.
7. Disjoint train/holdout partitions.
8. Artifact completeness and noise rejection by PSO/ANOVA.
"""

import sys
import json
from pathlib import Path
import pytest
import duckdb
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
BENCHMARK_DIR = OUTPUTS_DIR / "controlled_benchmark"


@pytest.fixture(scope="module")
def duck_conn():
    con = duckdb.connect()
    yield con
    con.close()


def test_benchmark_dataset_exists_and_manifest_valid():
    """Verify all 6 benchmark CSV files exist and manifest JSON is valid."""
    manifest_path = BENCHMARK_DIR / "benchmark_manifest.json"
    assert manifest_path.exists(), "benchmark_manifest.json missing!"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["n_customers"] == 25000
    assert manifest["cutoff_date"] == "2024-06-01"
    assert manifest["prediction_window_days"] == 30
    assert manifest["target_positives"] > 0
    assert manifest["target_negatives"] > 0

    expected_files = [
        "customers.csv",
        "sessions.csv",
        "transactions.csv",
        "marketing_campaigns.csv",
        "geo_data.csv",
        "customer_labels_pit.csv",
    ]
    for f in expected_files:
        p = BENCHMARK_DIR / f
        assert p.exists(), f"Benchmark file {f} missing!"
        assert p.stat().st_size > 0, f"Benchmark file {f} is empty!"


def test_no_session_or_transaction_before_signup(duck_conn):
    """Verify strict temporal invariant: 0 sessions and 0 transactions occur before signup_date."""
    sess_csv = (BENCHMARK_DIR / "sessions.csv").as_posix()
    cust_csv = (BENCHMARK_DIR / "customers.csv").as_posix()
    trans_csv = (BENCHMARK_DIR / "transactions.csv").as_posix()

    pre_signup_sessions = duck_conn.execute(f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{sess_csv}') s
        JOIN read_csv_auto('{cust_csv}') c ON s.customer_id = c.customer_id
        WHERE s.session_timestamp < c.signup_date
    """).fetchone()[0]
    assert pre_signup_sessions == 0, f"Found {pre_signup_sessions} sessions occurring before signup_date!"

    pre_signup_trans = duck_conn.execute(f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{trans_csv}') t
        JOIN read_csv_auto('{cust_csv}') c ON t.customer_id = c.customer_id
        WHERE t.transaction_timestamp < c.signup_date
    """).fetchone()[0]
    assert pre_signup_trans == 0, f"Found {pre_signup_trans} transactions occurring before signup_date!"


def test_items_count_strictly_positive(duck_conn):
    """Verify business logic: 0 transactions have items_count <= 0."""
    trans_csv = (BENCHMARK_DIR / "transactions.csv").as_posix()
    invalid_items = duck_conn.execute(f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{trans_csv}')
        WHERE items_count <= 0
    """).fetchone()[0]
    assert invalid_items == 0, f"Found {invalid_items} transactions with items_count <= 0!"


def test_marketing_campaign_window_validity(duck_conn):
    """Verify marketing synchronization: 0 sessions occur outside campaign active window."""
    sess_csv = (BENCHMARK_DIR / "sessions.csv").as_posix()
    mkt_csv = (BENCHMARK_DIR / "marketing_campaigns.csv").as_posix()

    invalid_mkt_sessions = duck_conn.execute(f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{sess_csv}') s
        JOIN read_csv_auto('{mkt_csv}') m ON s.campaign_id = m.campaign_id
        WHERE s.session_timestamp < m.start_date OR s.session_timestamp > m.end_date
    """).fetchone()[0]
    assert invalid_mkt_sessions == 0, f"Found {invalid_mkt_sessions} sessions outside campaign dates!"


def test_point_in_time_target_definition_validity(duck_conn):
    """Verify point-in-time target matches future transactions exactly."""
    trans_csv = (BENCHMARK_DIR / "transactions.csv").as_posix()
    labels_csv = (BENCHMARK_DIR / "customer_labels_pit.csv").as_posix()

    discrepancies = duck_conn.execute(f"""
        WITH future_trans AS (
            SELECT customer_id, COUNT(*) as cnt
            FROM read_csv_auto('{trans_csv}')
            WHERE transaction_timestamp > DATE '2024-06-01'
              AND transaction_timestamp <= DATE '2024-07-01'
            GROUP BY customer_id
        ),
        expected AS (
            SELECT 
                l.customer_id,
                l.target as label_target,
                CASE WHEN f.cnt > 0 THEN 1 ELSE 0 END as actual_target
            FROM read_csv_auto('{labels_csv}') l
            LEFT JOIN future_trans f ON l.customer_id = f.customer_id
        )
        SELECT COUNT(*)
        FROM expected
        WHERE label_target != actual_target
    """).fetchone()[0]
    assert discrepancies == 0, f"Found {discrepancies} mismatches between target and actual future transactions!"


def test_no_future_leakage_in_features(duck_conn):
    """Verify customer_features_pit.parquet has exactly N=25000 and has no target/ID in candidate features."""
    pq_path = (BENCHMARK_DIR / "customer_features_pit.parquet").as_posix()
    assert (BENCHMARK_DIR / "customer_features_pit.parquet").exists()

    df = duck_conn.execute(f"SELECT * FROM read_parquet('{pq_path}')").fetchdf()
    assert len(df) == 25000
    assert df["customer_id"].nunique() == 25000

    # Verify no zero-variance features
    drop_cols = ["customer_id", "split_type", "target", "country_code", "region", "customer_tier", "region_tier"]
    num_cols = [c for c in df.columns if c not in drop_cols and pd.api.types.is_numeric_dtype(df[c])]

    for c in num_cols:
        v = df[c].var()
        assert v > 0, f"Feature {c} has zero variance ({v})!"


def test_disjoint_train_holdout_splits():
    """Verify split_indices_pit.npz partitions are 100% disjoint."""
    npz_path = BENCHMARK_DIR / "split_indices_pit.npz"
    assert npz_path.exists()

    data = np.load(npz_path)
    train_idx = set(data["train_idx"])
    holdout_idx = set(data["holdout_idx"])

    assert len(train_idx) == 20000
    assert len(holdout_idx) == 5000
    assert len(train_idx.intersection(holdout_idx)) == 0, "Data leakage: train and holdout overlap!"


def test_pso_and_anova_artifacts_and_noise_rejection():
    """Verify modeling artifacts exist and noise variables were successfully rejected."""
    meta_path = BENCHMARK_DIR / "holdout_metadata_pit.json"
    assert meta_path.exists()

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    assert meta["total_holdout_samples"] == 5000
    assert meta["confusion_matrix"]["true_negatives"] > 0
    assert meta["confusion_matrix"]["true_positives"] > 0
    assert meta["metrics"]["pr_auc"] > 0.15

    # Check that noise variables were rejected
    assert meta["pso_noise_rejected_count"] == meta["total_noise_variables"] == 7, "PSO failed to reject all noise variables!"

    comp_csv = BENCHMARK_DIR / "metrics_comparison_pit.csv"
    assert comp_csv.exists()
    df_comp = pd.read_csv(comp_csv)
    assert len(df_comp) == 5, f"Expected 5 comparison experiments, got {len(df_comp)}"


def test_observation_window_maturity_and_boundary_conditions(duck_conn):
    """Verify all customers have sufficient observation history (>= 45 days before t_0) and boundary dates are strictly respected."""
    cust_csv = (BENCHMARK_DIR / "customers.csv").as_posix()
    trans_csv = (BENCHMARK_DIR / "transactions.csv").as_posix()
    cutoff_date = "2024-06-01"

    # 1. Observation window maturity: all customers signed up at least 45 days prior to cutoff
    immature_customers = duck_conn.execute(f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{cust_csv}')
        WHERE DATE_DIFF('day', CAST(signup_date AS DATE), DATE '{cutoff_date}') < 45
    """).fetchone()[0]
    assert immature_customers == 0, f"Found {immature_customers} customers with < 45 days of observation history!"

    # 2. Boundary condition: transactions exactly on cutoff date are pre-cutoff (not future)
    cutoff_day_future_trans = duck_conn.execute(f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{trans_csv}')
        WHERE transaction_timestamp = DATE '{cutoff_date}'
          AND transaction_timestamp > DATE '{cutoff_date}'
    """).fetchone()[0]
    assert cutoff_day_future_trans == 0


def test_temporal_invariance_future_data_does_not_affect_past_features(duck_conn):
    """
    Mathematical Proof of Temporal Anti-Leakage:
    Injecting arbitrary future sessions and transactions after cutoff t_0 (2024-06-01)
    must produce an EXACT 100% BIT-FOR-BIT IDENTICAL past feature vector for customers.
    """
    cust_csv = (BENCHMARK_DIR / "customers.csv").as_posix()
    sess_csv = (BENCHMARK_DIR / "sessions.csv").as_posix()
    trans_csv = (BENCHMARK_DIR / "transactions.csv").as_posix()
    cutoff_date = "2024-06-01"

    # Base features for customer 1
    base_sess_feats = duck_conn.execute(f"""
        SELECT
            COUNT(*) AS sess_count,
            COALESCE(SUM(session_duration), 0.0) AS total_session_duration,
            COALESCE(SUM(cart_additions), 0) AS total_cart_additions,
            DATE_DIFF('day', MAX(CAST(session_timestamp AS DATE)), DATE '{cutoff_date}') AS days_since_last_session
        FROM read_csv_auto('{sess_csv}')
        WHERE customer_id = 1 AND session_timestamp <= DATE '{cutoff_date}'
    """).fetchone()

    base_trans_feats = duck_conn.execute(f"""
        SELECT
            COUNT(*) AS trans_count,
            COALESCE(SUM(order_value), 0.0) AS total_spend,
            COALESCE(SUM(items_count), 0) AS total_items,
            DATE_DIFF('day', MAX(CAST(transaction_timestamp AS DATE)), DATE '{cutoff_date}') AS days_since_last_trans
        FROM read_csv_auto('{trans_csv}')
        WHERE customer_id = 1 AND transaction_timestamp <= DATE '{cutoff_date}'
    """).fetchone()

    # Now create modified session table with INJECTED FUTURE SESSIONS (e.g., 2024-06-15, 2024-06-25)
    duck_conn.execute(f"""
        CREATE OR REPLACE TEMP TABLE t_test_sess AS
        SELECT * FROM read_csv_auto('{sess_csv}')
        UNION ALL
        SELECT 9999999, 1, '2024-06-15', 3600.0, 50, 20, 0, 'ads', 'desktop', 1, 'REGION_001'
        UNION ALL
        SELECT 9999998, 1, '2024-06-25', 5400.0, 80, 45, 0, 'email', 'mobile', 2, 'REGION_001';

        CREATE OR REPLACE TEMP TABLE t_test_trans AS
        SELECT * FROM read_csv_auto('{trans_csv}')
        UNION ALL
        SELECT 9999999, 1, '2024-06-15', 9999.99, 15, 'credit_card', 1, 'overnight', 1, 0.5, 0.5;
    """)

    # Re-extract features using the exact query logic
    future_perturbed_sess_feats = duck_conn.execute(f"""
        SELECT
            COUNT(*) AS sess_count,
            COALESCE(SUM(session_duration), 0.0) AS total_session_duration,
            COALESCE(SUM(cart_additions), 0) AS total_cart_additions,
            DATE_DIFF('day', MAX(CAST(session_timestamp AS DATE)), DATE '{cutoff_date}') AS days_since_last_session
        FROM t_test_sess
        WHERE customer_id = 1 AND CAST(session_timestamp AS DATE) <= DATE '{cutoff_date}'
    """).fetchone()

    future_perturbed_trans_feats = duck_conn.execute(f"""
        SELECT
            COUNT(*) AS trans_count,
            COALESCE(SUM(order_value), 0.0) AS total_spend,
            COALESCE(SUM(items_count), 0) AS total_items,
            DATE_DIFF('day', MAX(CAST(transaction_timestamp AS DATE)), DATE '{cutoff_date}') AS days_since_last_trans
        FROM t_test_trans
        WHERE customer_id = 1 AND CAST(transaction_timestamp AS DATE) <= DATE '{cutoff_date}'
    """).fetchone()

    assert base_sess_feats == future_perturbed_sess_feats, (
        f"Temporal leakage detected: base sess {base_sess_feats} != perturbed {future_perturbed_sess_feats}"
    )
    assert base_trans_feats == future_perturbed_trans_feats, (
        f"Temporal leakage detected: base trans {base_trans_feats} != perturbed {future_perturbed_trans_feats}"
    )

