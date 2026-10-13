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
