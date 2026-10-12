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
