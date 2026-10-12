"""
Unit and Integration Tests: Phase 1 Data Audit and Referential Integrity.
"""

import sys
from pathlib import Path
import pytest
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    CUSTOMERS_CSV,
    GEO_DATA_CSV,
    MARKETING_CSV,
    SESSIONS_CSV,
    TRANSACTIONS_CSV,
    TRAIN_CSV,
    TEST_CSV,
    SAMPLE_SUBMISSION_CSV,
)


def test_all_8_csv_files_exist():
    """Verify that all 8 required CSV source files are present."""
    files = [
        CUSTOMERS_CSV,
        GEO_DATA_CSV,
        MARKETING_CSV,
        SESSIONS_CSV,
        TRANSACTIONS_CSV,
        TRAIN_CSV,
        TEST_CSV,
        SAMPLE_SUBMISSION_CSV,
    ]
    for f in files:
        assert f.exists(), f"Source file missing: {f.name}"
        assert f.stat().st_size > 0, f"Source file is empty: {f.name}"


def test_primary_key_uniqueness():
    """Verify primary keys have zero duplicates across core tables."""
    con = duckdb.connect()
    
    # customers.customer_id
    dup_cust = con.execute(f"SELECT COUNT(*) - COUNT(DISTINCT customer_id) FROM read_csv_auto('{CUSTOMERS_CSV.as_posix()}')").fetchone()[0]
    assert dup_cust == 0, f"Found {dup_cust} duplicate customer_id in customers.csv"

    # train.customer_id
    dup_train = con.execute(f"SELECT COUNT(*) - COUNT(DISTINCT customer_id) FROM read_csv_auto('{TRAIN_CSV.as_posix()}')").fetchone()[0]
    assert dup_train == 0, f"Found {dup_train} duplicate customer_id in train.csv"

    # test.customer_id
    dup_test = con.execute(f"SELECT COUNT(*) - COUNT(DISTINCT customer_id) FROM read_csv_auto('{TEST_CSV.as_posix()}')").fetchone()[0]
    assert dup_test == 0, f"Found {dup_test} duplicate customer_id in test.csv"


def test_train_test_disjointness():
    """Verify that train and test customer_id sets are completely disjoint (zero leakage)."""
    con = duckdb.connect()
    overlap = con.execute(
        f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{TRAIN_CSV.as_posix()}') tr
        INNER JOIN read_csv_auto('{TEST_CSV.as_posix()}') te
        ON tr.customer_id = te.customer_id
        """
    ).fetchone()[0]
    assert overlap == 0, f"Train and Test sets overlap by {overlap} customer IDs!"


def test_target_distribution_validity():
    """Verify target in train.csv is binary (0 and 1) with ~20% positive rate."""
    con = duckdb.connect()
    targets = con.execute(f"SELECT DISTINCT target FROM read_csv_auto('{TRAIN_CSV.as_posix()}')").fetchall()
    target_vals = set(t[0] for t in targets)
    assert target_vals == {0, 1}, f"Target has invalid values: {target_vals}"

    pos_rate = con.execute(f"SELECT AVG(target) FROM read_csv_auto('{TRAIN_CSV.as_posix()}')").fetchone()[0]
    assert 0.18 <= pos_rate <= 0.22, f"Target positive rate unexpected: {pos_rate:.4f}"


def test_marketing_campaigns_inventory():
    """Verify that marketing_campaigns.csv has exactly 200 rows and 6 columns."""
    con = duckdb.connect()
    cnt = con.execute(f"SELECT COUNT(*) FROM read_csv_auto('{MARKETING_CSV.as_posix()}')").fetchone()[0]
    cols = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{MARKETING_CSV.as_posix()}') LIMIT 0").fetchall()
    assert cnt == 200, f"Expected 200 marketing campaigns, got {cnt}"
    assert len(cols) == 6, f"Expected 6 columns in marketing_campaigns, got {len(cols)}"


def test_dataset_date_bounds():
    """Verify that timestamps in sessions and transactions do not exceed the reference date 2024-09-26."""
    con = duckdb.connect()
    max_sess = con.execute(f"SELECT MAX(session_timestamp) FROM read_csv_auto('{SESSIONS_CSV.as_posix()}')").fetchone()[0]
    max_trans = con.execute(f"SELECT MAX(transaction_timestamp) FROM read_csv_auto('{TRANSACTIONS_CSV.as_posix()}')").fetchone()[0]
    import datetime
    assert max_sess <= datetime.date(2024, 9, 26), f"Session timestamp exceeded 2024-09-26: {max_sess}"
    assert max_trans <= datetime.date(2024, 9, 26), f"Transaction timestamp exceeded 2024-09-26: {max_trans}"


def test_feature_dictionary_has_temporal_and_leakage_metadata():
    """Verify feature dictionary contains temporal_nature and cutoff_rule columns."""
    import pandas as pd
    from src.config import OUTPUTS_DIR
    dict_path = OUTPUTS_DIR / "feature_dictionary.csv"
    assert dict_path.exists(), "feature_dictionary.csv missing!"
    df = pd.read_csv(dict_path)
    assert "temporal_nature" in df.columns, "Missing 'temporal_nature' column in feature_dictionary.csv"
    assert "cutoff_rule" in df.columns, "Missing 'cutoff_rule' column in feature_dictionary.csv"
    assert "leakage_risk" in df.columns, "Missing 'leakage_risk' column in feature_dictionary.csv"
    assert "customer_id" not in df["feature_name"].values, "customer_id must not be a feature!"
    assert "target" not in df["feature_name"].values, "target must not be a feature!"

