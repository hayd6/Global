"""
Comprehensive Unit & Integration Test Suite: Holdout Predictions Artifact & Pipeline Reproducibility.
Validates all data integrity, 1-to-1 customer alignment, dynamic metrics filtering, and scale_pos_weight derivation.
"""

import hashlib
import json
from pathlib import Path
import duckdb
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CONFIGS_DIR = PROJECT_ROOT / "configs"
PROCESSED_DIR = OUTPUTS_DIR / "processed"
CUSTOMER_PARQUET = OUTPUTS_DIR / "customer_features.parquet"


def test_holdout_csv_structure_and_row_count():
    """Item A.2: Verify CSV has exactly 32,000 rows, unique non-null customer_ids, and required columns."""
    csv_path = OUTPUTS_DIR / "holdout_predictions.csv"
    assert csv_path.exists(), "outputs/holdout_predictions.csv missing!"

    df = pd.read_csv(csv_path)
    assert len(df) == 32000, f"Expected 32,000 holdout rows, got {len(df)}"

    required_cols = {"customer_id", "y_true", "y_proba", "y_pred", "error_group"}
    assert required_cols.issubset(set(df.columns)), f"Missing required columns: {required_cols - set(df.columns)}"

    # Check non-null and uniqueness of customer_id
    assert df["customer_id"].isnull().sum() == 0, "customer_id column contains nulls"
    assert df["customer_id"].nunique() == 32000, "customer_id contains duplicates"


def test_holdout_values_range_and_validity():
    """Item A.3: Verify y_true and y_pred contain strictly {0, 1}; y_proba is finite, non-null, in [0, 1]."""
    csv_path = OUTPUTS_DIR / "holdout_predictions.csv"
    df = pd.read_csv(csv_path)

    # Check y_true and y_pred
    assert set(df["y_true"].unique()).issubset({0, 1}), f"Invalid y_true values: {df['y_true'].unique()}"
    assert set(df["y_pred"].unique()).issubset({0, 1}), f"Invalid y_pred values: {df['y_pred'].unique()}"
    assert df["y_true"].isnull().sum() == 0, "y_true contains nulls"
    assert df["y_pred"].isnull().sum() == 0, "y_pred contains nulls"

    # Check y_proba
    assert df["y_proba"].isnull().sum() == 0, "y_proba contains nulls"
    assert np.isfinite(df["y_proba"]).all(), "y_proba contains non-finite values (inf or nan)"
    assert (df["y_proba"] >= 0.0).all() and (df["y_proba"] <= 1.0).all(), "y_proba outside [0, 1] range"


def test_holdout_error_group_row_by_row_consistency():
    """Item A.4: Verify each row's error_group strictly matches y_true and y_pred under TP/TN/FP/FN rules."""
    csv_path = OUTPUTS_DIR / "holdout_predictions.csv"
    df = pd.read_csv(csv_path)

    yt = df["y_true"].values
    yp = df["y_pred"].values

    expected_groups = np.select(
        [
            (yt == 1) & (yp == 1),
            (yt == 0) & (yp == 0),
            (yt == 0) & (yp == 1),
            (yt == 1) & (yp == 0),
        ],
        ["TP", "TN", "FP", "FN"],
        default="UNKNOWN",
    )

    assert "UNKNOWN" not in expected_groups, "Unmapped classification state detected"
    assert np.array_equal(df["error_group"].values, expected_groups), "Row-by-row error_group mismatch detected"


def test_holdout_full_32k_customer_ids_and_order_match_ground_truth():
    """Item A.6: Verify all 32,000 customer_ids, row ordering, and y_true match ground truth holdout."""
    csv_path = OUTPUTS_DIR / "holdout_predictions.csv"
    df = pd.read_csv(csv_path)

    # Load ground truth split indices
    split_indices_file = PROCESSED_DIR / "split_indices.npz"
    assert split_indices_file.exists(), "split_indices.npz missing!"
    indices_data = np.load(split_indices_file)
    holdout_idx = indices_data["holdout_idx"]
    assert len(holdout_idx) == 32000, f"Expected 32,000 holdout indices, got {len(holdout_idx)}"

    # Load ground truth customer pool with exact deterministic order
    con = duckdb.connect()
    gt_df = con.execute(
        f"""
        SELECT customer_id, target
        FROM read_parquet('{CUSTOMER_PARQUET.as_posix()}')
        WHERE split_type = 'train'
        ORDER BY customer_id
        """
    ).df()

    gt_holdout_cids = gt_df["customer_id"].iloc[holdout_idx].values
    gt_holdout_target = gt_df["target"].iloc[holdout_idx].values.astype(int)

    # Assert 100% match across all 32,000 samples and row order
    assert np.array_equal(df["customer_id"].values, gt_holdout_cids), (
        "Artifact customer_id array does NOT match ground truth holdout customer_ids in exact row order!"
    )
    assert np.array_equal(df["y_true"].values, gt_holdout_target), (
        "Artifact y_true array does NOT match ground truth target in exact row order!"
    )


def test_holdout_customer_id_sha256_computation_and_comparison():
    """Item A.5: Independently compute SHA-256 on artifact customer_ids and cross-check with ground truth."""
    csv_path = OUTPUTS_DIR / "holdout_predictions.csv"
    df = pd.read_csv(csv_path)

    # 1. Compute SHA-256 from artifact customer_ids
    artifact_cids = df["customer_id"].values.astype(np.int64)
    computed_artifact_sha256 = hashlib.sha256(artifact_cids.tobytes()).hexdigest()

    # 2. Compute SHA-256 independently from ground truth data
    con = duckdb.connect()
    gt_df = con.execute(
        f"""
        SELECT customer_id
        FROM read_parquet('{CUSTOMER_PARQUET.as_posix()}')
        WHERE split_type = 'train'
        ORDER BY customer_id
        """
    ).df()
    split_indices_file = PROCESSED_DIR / "split_indices.npz"
    holdout_idx = np.load(split_indices_file)["holdout_idx"]
    gt_holdout_cids = gt_df["customer_id"].iloc[holdout_idx].values.astype(np.int64)
    computed_gt_sha256 = hashlib.sha256(gt_holdout_cids.tobytes()).hexdigest()

    # 3. Assert both computed hashes match
    assert computed_artifact_sha256 == computed_gt_sha256, (
        f"Computed SHA-256 mismatch: artifact={computed_artifact_sha256} vs gt={computed_gt_sha256}"
    )

    # 4. Compare with split_metadata.json
    split_meta_path = CONFIGS_DIR / "split_metadata.json"
    with open(split_meta_path, "r", encoding="utf-8") as f:
        split_meta = json.load(f)
    assert computed_artifact_sha256 == split_meta["holdout_sha256"], (
        "Computed hash does not match configs/split_metadata.json"
    )

    # 5. Compare with holdout_prediction_metadata.json
    meta_json_path = OUTPUTS_DIR / "holdout_prediction_metadata.json"
    with open(meta_json_path, "r", encoding="utf-8") as f:
        artifact_meta = json.load(f)
    assert computed_artifact_sha256 == artifact_meta["holdout_sha256"], (
        "Computed hash does not match outputs/holdout_prediction_metadata.json"
    )


def test_holdout_confusion_matrix_matches_metrics_comparison_filtered_row():
    """Item A.7: Dynamically filter metrics_comparison.csv row and cross-check TN/FP/FN/TP counts."""
    metrics_csv = OUTPUTS_DIR / "metrics" / "metrics_comparison.csv"
    assert metrics_csv.exists(), "metrics_comparison.csv missing!"
    metrics_df = pd.read_csv(metrics_csv)

    # Dynamic filter (do not rely on fixed row index!)
    matching_rows = metrics_df[
        (metrics_df["model_name"] == "XGBoost (Full Features)")
        & (metrics_df["split_id"] == "stratified_80_20_v1")
        & (metrics_df["evaluation_set"] == "holdout_32k")
        & (metrics_df["feature_space"] == "63_features")
    ]
    assert len(matching_rows) == 1, (
        f"Expected exactly 1 matching row for XGBoost Full, found {len(matching_rows)}"
    )
    target_row = matching_rows.iloc[0]

    # Compute confusion matrix directly from holdout_predictions.csv
    pred_df = pd.read_csv(OUTPUTS_DIR / "holdout_predictions.csv")
    tn = int(np.sum((pred_df["y_true"] == 0) & (pred_df["y_pred"] == 0)))
    fp = int(np.sum((pred_df["y_true"] == 0) & (pred_df["y_pred"] == 1)))
    fn = int(np.sum((pred_df["y_true"] == 1) & (pred_df["y_pred"] == 0)))
    tp = int(np.sum((pred_df["y_true"] == 1) & (pred_df["y_pred"] == 1)))

    assert tn == int(target_row["true_negatives"]), f"TN mismatch: {tn} != {target_row['true_negatives']}"
    assert fp == int(target_row["false_positives"]), f"FP mismatch: {fp} != {target_row['false_positives']}"
    assert fn == int(target_row["false_negatives"]), f"FN mismatch: {fn} != {target_row['false_negatives']}"
    assert tp == int(target_row["true_positives"]), f"TP mismatch: {tp} != {target_row['true_positives']}"

    # Also verify exact ground truth values
    assert tn == 15740
    assert fp == 9763
    assert fn == 3078
    assert tp == 3419


def test_holdout_scale_pos_weight_exact_derivation_from_train_split():
    """Item A.8: Verify scale_pos_weight against exact negative/positive label counts of the training partition."""
    # 1. Load Train partition indices
    split_indices_file = PROCESSED_DIR / "split_indices.npz"
    indices_data = np.load(split_indices_file)
    train_idx = indices_data["train_idx"]
    assert len(train_idx) == 128000, f"Expected 128,000 train samples, got {len(train_idx)}"

    # 2. Get Train targets
    con = duckdb.connect()
    gt_df = con.execute(
        f"""
        SELECT target
        FROM read_parquet('{CUSTOMER_PARQUET.as_posix()}')
        WHERE split_type = 'train'
        ORDER BY customer_id
        """
    ).df()
    y_train = gt_df["target"].iloc[train_idx].values.astype(int)

    # 3. Compute exact class counts
    n_neg_actual = int(np.sum(y_train == 0))
    n_pos_actual = int(np.sum(y_train == 1))

    assert n_neg_actual == 102011, f"Expected 102,011 negatives in Train, got {n_neg_actual}"
    assert n_pos_actual == 25989, f"Expected 25,989 positives in Train, got {n_pos_actual}"
    assert n_neg_actual + n_pos_actual == 128000

    expected_spw = n_neg_actual / n_pos_actual

    # 4. Cross-check against metadata
    meta_json_path = OUTPUTS_DIR / "holdout_prediction_metadata.json"
    assert meta_json_path.exists(), "holdout_prediction_metadata.json missing!"
    with open(meta_json_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    meta_spw = meta["scale_pos_weight"]
    assert meta_spw["train_negative_count"] == n_neg_actual
    assert meta_spw["train_positive_count"] == n_pos_actual
    assert abs(meta_spw["exact_value"] - expected_spw) < 1e-12, (
        f"scale_pos_weight mismatch: {meta_spw['exact_value']} vs {expected_spw}"
    )


def test_holdout_artifact_metrics_and_model_config_integrity():
    """Item A.8: Verify full metrics derivation from holdout_predictions.csv matches metrics_comparison.csv and metadata."""
    pred_path = OUTPUTS_DIR / "holdout_predictions.csv"
    meta_path = OUTPUTS_DIR / "holdout_prediction_metadata.json"
    comp_path = OUTPUTS_DIR / "metrics" / "metrics_comparison.csv"

    assert pred_path.exists(), "holdout_predictions.csv missing!"
    assert meta_path.exists(), "holdout_prediction_metadata.json missing!"
    assert comp_path.exists(), "metrics_comparison.csv missing!"

    df_preds = pd.read_csv(pred_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    df_comp = pd.read_csv(comp_path)

    # 1. Verify model name & split in metadata matches metrics_comparison
    model_name = meta["model_name"]
    matching_row = df_comp[
        (df_comp["model_name"] == model_name)
        & (df_comp["split_id"] == meta["split_id"])
        & (df_comp["evaluation_set"] == meta["evaluation_set"])
    ]
    assert len(matching_row) == 1, f"Expected 1 matching row for {model_name}, found {len(matching_row)}"
    target = matching_row.iloc[0]

    # 2. Derive all metrics directly from y_true, y_pred, y_proba
    y_true = df_preds["y_true"].values
    y_pred = df_preds["y_pred"].values
    y_proba = df_preds["y_proba"].values

    derived_pr_auc = round(float(average_precision_score(y_true, y_proba)), 4)
    derived_roc_auc = round(float(roc_auc_score(y_true, y_proba)), 4)
    derived_f1 = round(float(f1_score(y_true, y_pred)), 4)
    derived_prec = round(float(precision_score(y_true, y_pred)), 4)
    derived_rec = round(float(recall_score(y_true, y_pred)), 4)
    derived_acc = round(float(accuracy_score(y_true, y_pred)), 4)

    # 3. Assert exact matches against metrics_comparison.csv
    assert derived_pr_auc == round(float(target["pr_auc"]), 4), f"PR-AUC: {derived_pr_auc} != {target['pr_auc']}"
    assert derived_roc_auc == round(float(target["roc_auc"]), 4), f"ROC-AUC: {derived_roc_auc} != {target['roc_auc']}"
    assert derived_f1 == round(float(target["f1_score"]), 4), f"F1: {derived_f1} != {target['f1_score']}"
    assert derived_prec == round(float(target["precision"]), 4), f"Precision: {derived_prec} != {target['precision']}"
    assert derived_rec == round(float(target["recall"]), 4), f"Recall: {derived_rec} != {target['recall']}"
    assert derived_acc == round(float(target["accuracy"]), 4), f"Accuracy: {derived_acc} != {target['accuracy']}"

    # 4. Verify confusion matrix matches
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))

    assert tn == int(target["true_negatives"]) == 15740
    assert fp == int(target["false_positives"]) == 9763
    assert fn == int(target["false_negatives"]) == 3078
    assert tp == int(target["true_positives"]) == 3419
