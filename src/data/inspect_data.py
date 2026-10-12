"""
Phase 1: Automated Data Audit and Quality Inspection using DuckDB.
Generates comprehensive quality reports, referential integrity checks,
target distribution stats, and initial audit visual charts.
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.config import (
    DATA_DIR,
    OUTPUTS_DIR,
    EDA_DIR,
    CUSTOMERS_CSV,
    GEO_DATA_CSV,
    MARKETING_CSV,
    SESSIONS_CSV,
    TRANSACTIONS_CSV,
    TRAIN_CSV,
    TEST_CSV,
    SAMPLE_SUBMISSION_CSV,
    ensure_directories,
    get_logger,
)

logger = get_logger("inspect_data")


def inspect_all_tables(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Inspect all CSV files for row count, column count, memory size, and missing values."""
    tables = {
        "customers": CUSTOMERS_CSV,
        "geo_data": GEO_DATA_CSV,
        "marketing_campaigns": MARKETING_CSV,
        "sessions": SESSIONS_CSV,
        "transactions": TRANSACTIONS_CSV,
        "train": TRAIN_CSV,
        "test": TEST_CSV,
        "sample_submission": SAMPLE_SUBMISSION_CSV,
    }

    quality_records = []

    for name, path in tables.items():
        if not path.exists():
            logger.error(f"File missing: {path}")
            continue

        size_mb = round(os.path.getsize(path) / (1024 * 1024), 2)
        row_count = con.execute(f"SELECT COUNT(*) FROM read_csv_auto('{path.as_posix()}')").fetchone()[0]
        cols_info = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{path.as_posix()}')").fetchall()
        col_count = len(cols_info)

        logger.info(f"Auditing '{name}': {row_count:,} rows, {col_count} columns, {size_mb} MB")

        # Column-level inspection
        for col in cols_info:
            col_name = col[0]
            col_type = col[1]

            # Null count query
            null_res = con.execute(
                f"""
                SELECT 
                    COUNT(CASE WHEN "{col_name}" IS NULL THEN 1 END) AS null_cnt,
                    COUNT(DISTINCT "{col_name}") AS distinct_cnt
                FROM read_csv_auto('{path.as_posix()}')
                """
            ).fetchone()
            null_cnt = null_res[0]
            distinct_cnt = null_res[1]
            null_pct = round((null_cnt / row_count) * 100, 3) if row_count > 0 else 0.0

            quality_records.append({
                "table_name": name,
                "table_size_mb": size_mb,
                "total_rows": row_count,
                "column_name": col_name,
                "data_type": col_type,
                "null_count": null_cnt,
                "null_percentage": null_pct,
                "distinct_count": distinct_cnt,
            })

    quality_df = pd.DataFrame(quality_records)
    quality_report_path = OUTPUTS_DIR / "data_quality_report.csv"
    quality_df.to_csv(quality_report_path, index=False)
    logger.info(f"Saved data quality report to {quality_report_path}")

    # Generate data_dictionary.csv as requested
    dict_df = quality_df[["table_name", "column_name", "data_type", "distinct_count", "null_percentage"]].copy()
    dict_path = OUTPUTS_DIR / "data_dictionary.csv"
    dict_df.to_csv(dict_path, index=False)
    logger.info(f"Saved data dictionary to {dict_path}")

    return quality_df


def check_referential_integrity(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Verify primary key uniqueness, foreign key relationships, and train/test disjointness."""
    logger.info("Performing referential integrity and key validation checks...")

    checks = []

    # 1. Primary key uniqueness
    pk_checks = [
        ("customers", "customer_id", CUSTOMERS_CSV),
        ("sessions", "session_id", SESSIONS_CSV),
        ("transactions", "transaction_id", TRANSACTIONS_CSV),
        ("marketing_campaigns", "campaign_id", MARKETING_CSV),
        ("geo_data", "geo_ip_region", GEO_DATA_CSV),
        ("train", "customer_id", TRAIN_CSV),
        ("test", "customer_id", TEST_CSV),
    ]

    for table, pk, path in pk_checks:
        dup_count = con.execute(
            f"""
            SELECT COUNT(*) - COUNT(DISTINCT "{pk}")
            FROM read_csv_auto('{path.as_posix()}')
            """
        ).fetchone()[0]
        checks.append({
            "check_type": "Primary Key Uniqueness",
            "relationship": f"{table}.{pk} is unique",
            "violations_count": dup_count,
            "status": "PASS" if dup_count == 0 else "FAIL",
            "details": f"Zero duplicate keys expected. Found {dup_count} duplicates."
        })

    # 2. Train and Test overlap check
    overlap_cnt = con.execute(
        f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{TRAIN_CSV.as_posix()}') tr
        INNER JOIN read_csv_auto('{TEST_CSV.as_posix()}') te
        ON tr.customer_id = te.customer_id
        """
    ).fetchone()[0]
    checks.append({
        "check_type": "Train-Test Leakage / Disjointness",
        "relationship": "train.customer_id INTERSECT test.customer_id",
        "violations_count": overlap_cnt,
        "status": "PASS" if overlap_cnt == 0 else "FAIL",
        "details": f"Train and test sets must have 0 overlapping customer_id. Overlap = {overlap_cnt}"
    })

    # 3. Foreign Key: train and test customers in customers.csv
    train_unmatched = con.execute(
        f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{TRAIN_CSV.as_posix()}') tr
        LEFT JOIN read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c
        ON tr.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    ).fetchone()[0]
    checks.append({
        "check_type": "Foreign Key Integrity",
        "relationship": "train.customer_id -> customers.customer_id",
        "violations_count": train_unmatched,
        "status": "PASS" if train_unmatched == 0 else "FAIL",
        "details": f"Unmatched customers in train: {train_unmatched}"
    })

    test_unmatched = con.execute(
        f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{TEST_CSV.as_posix()}') te
        LEFT JOIN read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c
        ON te.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    ).fetchone()[0]
    checks.append({
        "check_type": "Foreign Key Integrity",
        "relationship": "test.customer_id -> customers.customer_id",
        "violations_count": test_unmatched,
        "status": "PASS" if test_unmatched == 0 else "FAIL",
        "details": f"Unmatched customers in test: {test_unmatched}"
    })

    # 4. Sessions and Transactions foreign keys to customers
    sess_unmatched = con.execute(
        f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{SESSIONS_CSV.as_posix()}') s
        LEFT JOIN read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c
        ON s.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    ).fetchone()[0]
    checks.append({
        "check_type": "Foreign Key Integrity",
        "relationship": "sessions.customer_id -> customers.customer_id",
        "violations_count": sess_unmatched,
        "status": "PASS" if sess_unmatched == 0 else "FAIL",
        "details": f"Unmatched customer_id in sessions: {sess_unmatched}"
    })

    trans_unmatched = con.execute(
        f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{TRANSACTIONS_CSV.as_posix()}') t
        LEFT JOIN read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c
        ON t.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    ).fetchone()[0]
    checks.append({
        "check_type": "Foreign Key Integrity",
        "relationship": "transactions.customer_id -> customers.customer_id",
        "violations_count": trans_unmatched,
        "status": "PASS" if trans_unmatched == 0 else "FAIL",
        "details": f"Unmatched customer_id in transactions: {trans_unmatched}"
    })

    # 5. Sessions foreign keys to geo_data and marketing_campaigns
    geo_unmatched = con.execute(
        f"""
        SELECT COUNT(*)
        FROM read_csv_auto('{SESSIONS_CSV.as_posix()}') s
        LEFT JOIN read_csv_auto('{GEO_DATA_CSV.as_posix()}') g
        ON s.geo_ip_region = g.geo_ip_region
        WHERE g.geo_ip_region IS NULL AND s.geo_ip_region IS NOT NULL
        """
    ).fetchone()[0]
    checks.append({
        "check_type": "Foreign Key Integrity",
        "relationship": "sessions.geo_ip_region -> geo_data.geo_ip_region",
        "violations_count": geo_unmatched,
        "status": "PASS" if geo_unmatched == 0 else "FAIL",
        "details": f"Unmatched geo_ip_region in sessions: {geo_unmatched}"
    })

    ref_df = pd.DataFrame(checks)
    ref_path = OUTPUTS_DIR / "referential_integrity_report.csv"
    ref_df.to_csv(ref_path, index=False)
    logger.info(f"Saved referential integrity report to {ref_path}")
    return ref_df


def audit_target_distribution(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Analyze target distribution in train.csv."""
    logger.info("Auditing target distribution in train.csv...")
    target_df = con.execute(
        f"""
        SELECT 
            target,
            COUNT(*) AS count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM read_csv_auto('{TRAIN_CSV.as_posix()}')), 2) AS percentage
        FROM read_csv_auto('{TRAIN_CSV.as_posix()}')
        GROUP BY target
        ORDER BY target
        """
    ).df()

    target_path = OUTPUTS_DIR / "target_distribution.csv"
    target_df.to_csv(target_path, index=False)
    logger.info(f"Saved target distribution report to {target_path}")

    return target_df


def plot_audit_charts(quality_df: pd.DataFrame, target_df: pd.DataFrame):
    """Plot visual audit charts for initial inspection."""
    logger.info("Generating audit charts in outputs/eda/...")
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # 1. Target distribution chart
    plt.figure(figsize=(7, 5))
    colors = ["#4C72B0", "#DD8452"]
    bars = plt.bar([str(x) for x in target_df["target"]], target_df["count"], color=colors, width=0.5, edgecolor="black", alpha=0.85)
    plt.title("Target Distribution in train.csv (Imbalance: 79.7% vs 20.3%)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Purchase Target (0 = No Purchase, 1 = Purchase)", fontsize=11)
    plt.ylabel("Number of Customers", fontsize=11)
    for bar, pct in zip(bars, target_df["percentage"]):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2000, f"{yval:,} ({pct}%)", ha="center", va="bottom", fontsize=10, fontweight="bold")
    plt.ylim(0, max(target_df["count"]) * 1.15)
    plt.tight_layout()
    plt.savefig(EDA_DIR / "audit_target_distribution.png", dpi=200)
    plt.close()

    # 2. Table row count & size chart
    table_summary = quality_df.groupby("table_name").agg(
        total_rows=("total_rows", "first"),
        table_size_mb=("table_size_mb", "first")
    ).reset_index().sort_values("total_rows", ascending=True)

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax2 = ax1.twinx()
    
    y_pos = np.arange(len(table_summary))
    ax1.barh(y_pos - 0.15, table_summary["total_rows"], height=0.3, color="#55A868", label="Rows (Log Scale)", alpha=0.85)
    ax1.set_xscale("log")
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(table_summary["table_name"], fontsize=10)
    ax1.set_xlabel("Number of Rows (Logarithmic Scale)", fontsize=11, color="#55A868")

    ax2.barh(y_pos + 0.15, table_summary["table_size_mb"], height=0.3, color="#C44E52", label="File Size (MB)", alpha=0.85)
    ax2.set_xlabel("File Size (MB)", fontsize=11, color="#C44E52")

    plt.title("Dataset Overview: Rows vs Storage Size per CSV", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(EDA_DIR / "audit_table_sizes.png", dpi=200)
    plt.close()

    # 3. Missing values summary chart
    missing_cols = quality_df[quality_df["null_percentage"] > 0].sort_values("null_percentage", ascending=True)
    if not missing_cols.empty:
        plt.figure(figsize=(8, max(4, len(missing_cols)*0.4)))
        plt.barh(missing_cols["table_name"] + "." + missing_cols["column_name"], missing_cols["null_percentage"], color="#8172B3", edgecolor="black")
        plt.title("Columns with Explicit NULLs (%)", fontsize=12, fontweight="bold")
        plt.xlabel("Missing Percentage (%)", fontsize=11)
        plt.tight_layout()
        plt.savefig(EDA_DIR / "audit_missing_values.png", dpi=200)
        plt.close()

    logger.info("Audit charts successfully created.")


def run_audit():
    """Main execution function for Phase 1 Data Audit."""
    ensure_directories()
    con = duckdb.connect()
    logger.info("=== STARTING PHASE 1: DATA AUDIT ===")

    quality_df = inspect_all_tables(con)
    ref_df = check_referential_integrity(con)
    target_df = audit_target_distribution(con)
    plot_audit_charts(quality_df, target_df)

    logger.info("=== COMPLETED PHASE 1: DATA AUDIT ===")
    return quality_df, ref_df, target_df


if __name__ == "__main__":
    run_audit()
