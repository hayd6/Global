"""
Integration Tests: Relational Integrity, Foreign Keys, and Join Cardinality Validation.
Ensures zero cartesian-product inflation and 100% referential consistency across the 8 tables.
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


def test_foreign_key_sessions_and_transactions_to_customers():
    """Verify that 100% of session and transaction customer IDs exist in customers.csv (0 orphans)."""
    con = duckdb.connect()

    # Sessions orphans
    orphan_sessions = con.execute(
        f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{SESSIONS_CSV.as_posix()}') s
        LEFT JOIN read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c
        ON s.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    ).fetchone()[0]
    assert orphan_sessions == 0, f"Found {orphan_sessions} orphan customer_ids in sessions.csv"

    # Transactions orphans
    orphan_trans = con.execute(
        f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{TRANSACTIONS_CSV.as_posix()}') t
        LEFT JOIN read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c
        ON t.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    ).fetchone()[0]
    assert orphan_trans == 0, f"Found {orphan_trans} orphan customer_ids in transactions.csv"


def test_foreign_key_sessions_to_geo_and_marketing():
    """Verify referential consistency of geo_ip_region and campaign_id from sessions."""
    con = duckdb.connect()

    # Geo IP Region consistency
    orphan_geo = con.execute(
        f"""
        SELECT COUNT(*)
        FROM (SELECT DISTINCT geo_ip_region FROM read_csv_auto('{SESSIONS_CSV.as_posix()}') WHERE geo_ip_region IS NOT NULL) s
        LEFT JOIN read_csv_auto('{GEO_DATA_CSV.as_posix()}') g
        ON TRIM(s.geo_ip_region) = TRIM(g.geo_ip_region)
        WHERE g.geo_ip_region IS NULL
        """
    ).fetchone()[0]
    assert orphan_geo == 0, f"Found {orphan_geo} unrecognized geo regions in sessions.csv"

    # Campaign ID consistency
    orphan_camp = con.execute(
        f"""
        SELECT COUNT(*)
        FROM (SELECT DISTINCT campaign_id FROM read_csv_auto('{SESSIONS_CSV.as_posix()}') WHERE campaign_id IS NOT NULL) s
        LEFT JOIN read_csv_auto('{MARKETING_CSV.as_posix()}') m
        ON s.campaign_id = m.campaign_id
        WHERE m.campaign_id IS NULL
        """
    ).fetchone()[0]
    assert orphan_camp == 0, f"Found {orphan_camp} unrecognized campaign IDs in sessions.csv"


def test_sample_submission_matches_test_csv_exactly():
    """Verify sample_submission.csv has identical 40,000 customer_ids in identical order as test.csv."""
    con = duckdb.connect()

    mismatches = con.execute(
        f"""
        WITH t AS (
            SELECT customer_id, ROW_NUMBER() OVER () AS rn
            FROM read_csv_auto('{TEST_CSV.as_posix()}')
        ),
        s AS (
            SELECT customer_id, ROW_NUMBER() OVER () AS rn
            FROM read_csv_auto('{SAMPLE_SUBMISSION_CSV.as_posix()}')
        )
        SELECT COUNT(*)
        FROM t
        FULL OUTER JOIN s ON t.rn = s.rn
        WHERE t.customer_id != s.customer_id OR t.customer_id IS NULL OR s.customer_id IS NULL
        """
    ).fetchone()[0]
    assert mismatches == 0, f"sample_submission.csv does not match test.csv! Mismatches: {mismatches}"


def test_join_cardinality_no_customer_inflation():
    """
    Verify that joining aggregated sessions and transactions to customers produces exactly 200,000 rows.
    Zero cartesian explosion or duplicate customer weights.
    """
    con = duckdb.connect()

    result_count = con.execute(
        f"""
        WITH sess_agg AS (
            SELECT customer_id, COUNT(*) as sess_cnt
            FROM read_csv_auto('{SESSIONS_CSV.as_posix()}')
            GROUP BY customer_id
        ),
        trans_agg AS (
            SELECT customer_id, COUNT(*) as trans_cnt
            FROM read_csv_auto('{TRANSACTIONS_CSV.as_posix()}')
            GROUP BY customer_id
        )
        SELECT COUNT(*)
        FROM read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c
        LEFT JOIN sess_agg s ON c.customer_id = s.customer_id
        LEFT JOIN trans_agg t ON c.customer_id = t.customer_id
        """
    ).fetchone()[0]

    assert result_count == 200000, f"Join cardinality violated: expected 200,000, got {result_count}"
