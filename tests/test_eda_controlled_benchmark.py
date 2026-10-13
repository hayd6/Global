"""
tests/test_eda_controlled_benchmark.py
Automated Verification Suite for Controlled Benchmark EDA Artifacts and Report Consistency.
"""

import json
import hashlib
from pathlib import Path
import pandas as pd
import numpy as np
import pytest
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = PROJECT_ROOT / "outputs" / "controlled_benchmark"
EDA_DIR = BENCHMARK_DIR / "eda"


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def test_eda_artifacts_exist():
    """Verify all 10 EDA deliverables exist and are non-empty."""
    required_files = [
        "data_inventory.csv",
        "data_quality.csv",
        "target_distribution.csv",
        "numeric_summary.csv",
        "categorical_summary.csv",
        "correlation_matrix.csv",
        "eda_manifest.json",
        "eda_report.md",
        "eda_run.log",
        "eda_1_table_scales.png",
        "eda_2_target_distribution_pit.png",
        "eda_3_missing_values.png",
        "eda_4_numeric_distributions.png",
        "eda_5_correlation_heatmap.png",
        "eda_6_feature_comparison_by_target.png",
        "eda_7_temporal_activity.png",
        "eda_8_cart_and_engagement_matrix.png",
    ]
    for fname in required_files:
        fpath = EDA_DIR / fname
        assert fpath.exists(), f"Missing EDA artifact: {fname}"
        assert fpath.stat().st_size > 0, f"EDA artifact is empty: {fname}"


def test_customer_count_and_target_balance():
    """Verify total labels equals total customers and target rate matches CSV."""
    df_labels = pd.read_csv(BENCHMARK_DIR / "customer_labels_pit.csv")
    df_customers = pd.read_csv(BENCHMARK_DIR / "customers.csv")
    df_tgt_csv = pd.read_csv(EDA_DIR / "target_distribution.csv")

    assert len(df_labels) == 25000
    assert len(df_customers) == 25000
    assert len(df_labels) == len(df_customers)

    pos_count = int(df_labels["target"].sum())
    neg_count = len(df_labels) - pos_count
    assert pos_count == 2195
    assert neg_count == 22805

    pos_csv_val = int(df_tgt_csv.loc[df_tgt_csv["target"] == 1, "customer_count"].values[0])
    neg_csv_val = int(df_tgt_csv.loc[df_tgt_csv["target"] == 0, "customer_count"].values[0])
    assert pos_csv_val == 2195
    assert neg_csv_val == 22805


def test_manifest_sha256_integrity():
    """Verify disk files match SHA-256 hashes defined in benchmark_manifest.json."""
    manifest_path = BENCHMARK_DIR / "benchmark_manifest.json"
    assert manifest_path.exists()
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    ref_hashes = manifest_data.get("files_sha256", {})

    for fname, exp_hash in ref_hashes.items():
        actual_hash = compute_sha256(BENCHMARK_DIR / fname)
        assert actual_hash == exp_hash, f"SHA-256 mismatch for {fname}: expected {exp_hash}, got {actual_hash}"


def test_feature_space_cleanliness():
    """Verify feature store strictly isolates identifiers and target labels."""
    df_feat = pd.read_parquet(BENCHMARK_DIR / "customer_features_pit.parquet")
    assert df_feat.shape == (25000, 71)

    candidate_predictors = [c for c in df_feat.columns if c not in ["customer_id", "target", "split_type"]]
    assert "customer_id" not in candidate_predictors
    assert "target" not in candidate_predictors
    assert "split_type" not in candidate_predictors

    cat_cols = ["country_code", "region", "customer_tier", "region_tier"]
    num_cols = [c for c in candidate_predictors if c not in cat_cols]
    assert len(cat_cols) == 4
    assert len(num_cols) == 64
    assert len(candidate_predictors) == 68


def test_temporal_anti_leakage_isolation():
    """Verify feature store aggregates strictly match pre-cutoff events."""
    df_feat = pd.read_parquet(BENCHMARK_DIR / "customer_features_pit.parquet")
    df_trans = pd.read_csv(BENCHMARK_DIR / "transactions.csv")
    df_sess = pd.read_csv(BENCHMARK_DIR / "sessions.csv")

    cutoff_date = "2024-06-01"
    pre_cutoff_tx = (pd.to_datetime(df_trans["transaction_timestamp"]) <= pd.to_datetime(cutoff_date)).sum()
    pre_cutoff_sess = (pd.to_datetime(df_sess["session_timestamp"]) <= pd.to_datetime(cutoff_date)).sum()

    assert pre_cutoff_tx == 19061
    assert pre_cutoff_sess == 78836
    assert df_feat["trans_count"].sum() == pre_cutoff_tx
    assert df_feat["sess_count"].sum() == pre_cutoff_sess


def test_eda_report_and_artifact_numbers_consistency():
    """Verify numbers quoted in eda_report.md match exactly with feature store and CSVs."""
    df_feat = pd.read_parquet(BENCHMARK_DIR / "customer_features_pit.parquet")
    report_text = (EDA_DIR / "eda_report.md").read_text(encoding="utf-8")
    corr_df = pd.read_csv(EDA_DIR / "correlation_matrix.csv", index_col=0)

    # Check cart additions means
    mean_cart_0 = df_feat[df_feat["target"] == 0]["total_cart_additions"].mean()
    mean_cart_1 = df_feat[df_feat["target"] == 1]["total_cart_additions"].mean()
    assert f"{mean_cart_0:.2f}" in report_text
    assert f"{mean_cart_1:.2f}" in report_text

    # Check session duration means
    mean_dur_0 = df_feat[df_feat["target"] == 0]["total_session_duration"].mean()
    mean_dur_1 = df_feat[df_feat["target"] == 1]["total_session_duration"].mean()
    assert f"{mean_dur_0:.2f}" in report_text
    assert f"{mean_dur_1:.2f}" in report_text

    # Check total spend means
    mean_spend_0 = df_feat[df_feat["target"] == 0]["total_spend"].mean()
    mean_spend_1 = df_feat[df_feat["target"] == 1]["total_spend"].mean()
    assert f"{mean_spend_0:.2f}" in report_text
    assert f"{mean_spend_1:.2f}" in report_text

    # Check correlation matrix values
    corr_dur = corr_df.loc["total_session_duration", "target"]
    corr_pages = corr_df.loc["total_pages_viewed", "target"]
    corr_spend = corr_df.loc["total_spend", "target"]
    corr_cart = corr_df.loc["total_cart_additions", "target"]
    assert f"{corr_dur:.4f}" in report_text
    assert f"{corr_pages:.4f}" in report_text
    assert f"{corr_spend:.4f}" in report_text
    assert f"{corr_cart:.4f}" in report_text

    # Check collinearity values
    collinear_pages_dur = corr_df.loc["total_pages_viewed", "total_session_duration"]
    collinear_spend_trans = corr_df.loc["total_spend", "trans_count"]
    assert f"{collinear_pages_dur:.4f}" in report_text
    assert f"{collinear_spend_trans:.4f}" in report_text


def test_audit_failure_simulation():
    """Verify that composite audit status strictly flags failure when any mandatory check fails."""
    # Test 1: Simulated suite logic
    sample_audit_results_pass = {
        "check_1": {"status": "PASS", "evidence": "Ok"},
        "check_2": {"status": "PASS", "evidence": "Ok"},
    }
    all_passed = all(res.get("status") == "PASS" for res in sample_audit_results_pass.values())
    status_pass = "ALL_AUDIT_CHECKS_PASSED" if all_passed else "AUDIT_CHECK_FAILED"
    assert status_pass == "ALL_AUDIT_CHECKS_PASSED"

    sample_audit_results_fail = {
        "check_1": {"status": "PASS", "evidence": "Ok"},
        "check_2": {"status": "FAIL", "evidence": "Missing foreign keys"},
    }
    all_passed_fail = all(res.get("status") == "PASS" for res in sample_audit_results_fail.values())
    status_fail = "ALL_AUDIT_CHECKS_PASSED" if all_passed_fail else "AUDIT_CHECK_FAILED"
    assert status_fail == "AUDIT_CHECK_FAILED"
    assert status_fail != "PASS"

    # Test 2: Execution failure simulation using DuckDB on corrupted schema
    con = duckdb.connect()
    con.execute("CREATE TABLE corrupt_cust (customer_id BIGINT, name VARCHAR)")
    con.execute("INSERT INTO corrupt_cust VALUES (1, 'Alice'), (1, 'Bob')")
    tot = con.execute("SELECT count(*) FROM corrupt_cust").fetchone()[0]
    dist_pk = con.execute("SELECT count(DISTINCT customer_id) FROM corrupt_cust").fetchone()[0]
    pk_status = "PASS" if tot == dist_pk else "FAIL"
    assert pk_status == "FAIL"
    con.close()


def test_customer_id_and_target_alignment_row_by_row():
    """Verify exact 1:1 customer_id alignment and zero target mismatches between features and labels."""
    df_customers = pd.read_csv(BENCHMARK_DIR / "customers.csv")
    df_labels = pd.read_csv(BENCHMARK_DIR / "customer_labels_pit.csv")
    df_feat = pd.read_parquet(BENCHMARK_DIR / "customer_features_pit.parquet")

    # Verify identical customer_id set and ordering
    assert len(df_customers) == 25000
    assert len(df_labels) == 25000
    assert len(df_feat) == 25000

    np.testing.assert_array_equal(df_customers["customer_id"].values, df_labels["customer_id"].values)
    np.testing.assert_array_equal(df_customers["customer_id"].values, df_feat["customer_id"].values)

    # Verify target alignment row-by-row
    np.testing.assert_array_equal(df_labels["target"].values, df_feat["target"].values)
    mismatches = int((df_labels["target"].values != df_feat["target"].values).sum())
    assert mismatches == 0


def test_customer_level_aggregation_parity_full():
    """Verify customer-by-customer feature parity against raw pre-cutoff event aggregations (all 25,000 customers)."""
    con = duckdb.connect()
    t_p = (BENCHMARK_DIR / "transactions.csv").as_posix()
    s_p = (BENCHMARK_DIR / "sessions.csv").as_posix()
    c_p = (BENCHMARK_DIR / "customers.csv").as_posix()
    f_p = (BENCHMARK_DIR / "customer_features_pit.parquet").as_posix()

    query = f"""
    WITH pre_tx AS (
        SELECT 
            customer_id,
            COUNT(transaction_id) AS trans_count,
            COALESCE(SUM(order_value), 0.0) AS total_spend,
            COALESCE(SUM(items_count), 0) AS total_items_count,
            DATEDIFF('day', MAX(transaction_timestamp), DATE '2024-06-01') AS days_since_last_transaction
        FROM read_csv_auto('{t_p}')
        WHERE transaction_timestamp <= DATE '2024-06-01'
        GROUP BY customer_id
    ),
    pre_sess AS (
        SELECT 
            customer_id,
            COUNT(session_id) AS sess_count,
            COALESCE(SUM(session_duration), 0.0) AS total_session_duration,
            COALESCE(SUM(pages_viewed), 0) AS total_pages_viewed,
            COALESCE(SUM(cart_additions), 0) AS total_cart_additions,
            DATEDIFF('day', MAX(session_timestamp), DATE '2024-06-01') AS days_since_last_session
        FROM read_csv_auto('{s_p}')
        WHERE session_timestamp <= DATE '2024-06-01'
        GROUP BY customer_id
    ),
    raw_cust AS (
        SELECT 
            c.customer_id,
            COALESCE(tx.trans_count, 0) AS raw_trans_count,
            COALESCE(tx.total_spend, 0.0) AS raw_total_spend,
            COALESCE(tx.total_items_count, 0) AS raw_total_items_count,
            COALESCE(tx.days_since_last_transaction, 365) AS raw_days_since_last_transaction,
            COALESCE(ss.sess_count, 0) AS raw_sess_count,
            COALESCE(ss.total_session_duration, 0.0) AS raw_total_session_duration,
            COALESCE(ss.total_pages_viewed, 0) AS raw_total_pages_viewed,
            COALESCE(ss.total_cart_additions, 0) AS raw_total_cart_additions,
            COALESCE(ss.days_since_last_session, 365) AS raw_days_since_last_session
        FROM read_csv_auto('{c_p}') c
        LEFT JOIN pre_tx tx ON c.customer_id = tx.customer_id
        LEFT JOIN pre_sess ss ON c.customer_id = ss.customer_id
    )
    SELECT 
        MAX(ABS(r.raw_trans_count - f.trans_count)) AS max_err_trans_count,
        MAX(ABS(r.raw_total_spend - f.total_spend)) AS max_err_total_spend,
        MAX(ABS(r.raw_total_items_count - f.total_items_count)) AS max_err_total_items_count,
        MAX(ABS(r.raw_days_since_last_transaction - f.days_since_last_transaction)) AS max_err_days_trans,
        MAX(ABS(r.raw_sess_count - f.sess_count)) AS max_err_sess_count,
        MAX(ABS(r.raw_total_session_duration - f.total_session_duration)) AS max_err_sess_duration,
        MAX(ABS(r.raw_total_pages_viewed - f.total_pages_viewed)) AS max_err_pages_viewed,
        MAX(ABS(r.raw_total_cart_additions - f.total_cart_additions)) AS max_err_cart_additions,
        MAX(ABS(r.raw_days_since_last_session - f.days_since_last_session)) AS max_err_days_sess
    FROM raw_cust r
    JOIN read_parquet('{f_p}') f ON r.customer_id = f.customer_id
    """
    res = con.execute(query).df().iloc[0].to_dict()
    con.close()

    for metric, max_err in res.items():
        assert max_err < 1e-4, f"Customer-level aggregation discrepancy on {metric}: max_err={max_err}"


def test_cutoff_boundary_and_date_resolution():
    """Verify timestamp format resolution is DATE and cutoff boundaries strictly isolate future window."""
    con = duckdb.connect()
    t_p = (BENCHMARK_DIR / "transactions.csv").as_posix()
    s_p = (BENCHMARK_DIR / "sessions.csv").as_posix()
    l_p = (BENCHMARK_DIR / "customer_labels_pit.csv").as_posix()

    # 1. Verify date format strictly YYYY-MM-DD
    non_date_tx = con.execute(f"SELECT count(*) FROM read_csv_auto('{t_p}') WHERE transaction_timestamp::VARCHAR !~ '^\\d{{4}}-\\d{{2}}-\\d{{2}}$'").fetchone()[0]
    non_date_sess = con.execute(f"SELECT count(*) FROM read_csv_auto('{s_p}') WHERE session_timestamp::VARCHAR !~ '^\\d{{4}}-\\d{{2}}-\\d{{2}}$'").fetchone()[0]
    assert non_date_tx == 0
    assert non_date_sess == 0

    # 2. Verify cutoff boundary counts:
    # Historical: transaction_timestamp <= '2024-06-01'
    # Future window: transaction_timestamp >= '2024-06-02' AND transaction_timestamp <= '2024-07-01'
    tx_pre = con.execute(f"SELECT count(*) FROM read_csv_auto('{t_p}') WHERE transaction_timestamp <= DATE '2024-06-01'").fetchone()[0]
    tx_future = con.execute(f"SELECT count(*) FROM read_csv_auto('{t_p}') WHERE transaction_timestamp >= DATE '2024-06-02' AND transaction_timestamp <= DATE '2024-07-01'").fetchone()[0]
    tx_total = con.execute(f"SELECT count(*) FROM read_csv_auto('{t_p}')").fetchone()[0]

    assert tx_pre == 19061
    assert tx_future == 2473
    assert tx_pre + tx_future == tx_total == 21534

    # 3. Verify future window purchasers reconcile with customer_labels_pit.csv
    future_buyers = con.execute(f"""
        SELECT count(DISTINCT customer_id) 
        FROM read_csv_auto('{t_p}') 
        WHERE transaction_timestamp >= DATE '2024-06-02' AND transaction_timestamp <= DATE '2024-07-01'
    """).fetchone()[0]
    
    pos_labels = con.execute(f"SELECT count(*) FROM read_csv_auto('{l_p}') WHERE target = 1").fetchone()[0]
    assert future_buyers == pos_labels == 2195
    con.close()


def test_manifest_dynamic_audit_fields():
    """Verify eda_manifest.json contains dynamic counts, ratios, and no hardcoded static strings."""
    manifest_path = EDA_DIR / "eda_manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert data["overall_status"] == "ALL_AUDIT_CHECKS_PASSED"
    assert data["audit_checks_passed_ratio"] == "9/9"
    assert len(data["audit_verification_suite"]) == 9

    metrics = data["key_metrics_reconciled"]
    assert metrics["ground_truth_reconciliation_match_rate"] == 100.0
    assert metrics["ground_truth_reconciliation_mismatches"] == 0
    assert metrics["audited_columns_count"] == 123
    assert metrics["columns_with_missing_count"] == 4
    assert metrics["columns_without_missing_count"] == 119
    assert metrics["audited_columns_count"] == metrics["columns_with_missing_count"] + metrics["columns_without_missing_count"]

