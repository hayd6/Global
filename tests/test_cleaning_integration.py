"""
Unit and Integration Tests: Phase 2 Data Cleaning & Integration.
"""

import sys
from pathlib import Path
import pytest
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import OUTPUTS_DIR, PROCESSED_DATA_DIR
from src.data.clean_data import create_cleaned_views


def test_cleaned_views_normalization():
    """Verify that SQL views successfully normalize booleans, currency, and placeholders."""
    con = duckdb.connect()
    create_cleaned_views(con)

    # 1. sessions bounce flag normalized to 0, 1, or null
    invalid_bounces = con.execute(
        """
        SELECT COUNT(*)
        FROM v_cleaned_sessions
        WHERE is_bounce NOT IN (0, 1) AND is_bounce IS NOT NULL
        """
    ).fetchone()[0]
    assert invalid_bounces == 0, f"Found {invalid_bounces} non-normalized bounce flags."

    # 2. transactions order_value is numeric (DOUBLE) non-negative
    non_null_order_vals = con.execute("SELECT COUNT(*) FROM v_cleaned_transactions WHERE order_value >= 0").fetchone()[0]
    assert non_null_order_vals == 500000, f"Expected 500,000 valid non-negative order values, got {non_null_order_vals}"

    # 3. customers credit_limit is numeric (DOUBLE)
    non_null_credit = con.execute("SELECT COUNT(*) FROM v_cleaned_customers WHERE credit_limit > 0").fetchone()[0]
    assert non_null_credit == 200000, f"Expected 200,000 valid positive credit limits, got {non_null_credit}"


def test_integrated_customer_table_shape():
    """Verify customer dataset has exactly 200,000 rows and correct train/test split."""
    parquet_path = OUTPUTS_DIR / "customer_features.parquet"
    assert parquet_path.exists(), "Customer features parquet file does not exist!"

    con = duckdb.connect()
    total_cust = con.execute(f"SELECT COUNT(*) FROM read_parquet('{parquet_path.as_posix()}')").fetchone()[0]
    train_cust = con.execute(f"SELECT COUNT(*) FROM read_parquet('{parquet_path.as_posix()}') WHERE split_type = 'train'").fetchone()[0]
    test_cust = con.execute(f"SELECT COUNT(*) FROM read_parquet('{parquet_path.as_posix()}') WHERE split_type = 'test'").fetchone()[0]

    assert total_cust == 200000, f"Expected 200,000 total customers, got {total_cust}"
    assert train_cust == 160000, f"Expected 160,000 train customers, got {train_cust}"
    assert test_cust == 40000, f"Expected 40,000 test customers, got {test_cust}"
