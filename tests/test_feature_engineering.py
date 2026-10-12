"""
Unit and Integration Tests: Phase 4 Feature Engineering and Dictionary Validation.
"""

import sys
from pathlib import Path
import pytest
import duckdb
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import OUTPUTS_DIR


def test_feature_dictionary_content():
    """Verify that feature_dictionary.csv exists, is non-empty, and has required metadata columns."""
    dict_path = OUTPUTS_DIR / "feature_dictionary.csv"
    assert dict_path.exists(), "feature_dictionary.csv missing!"

    df = pd.read_csv(dict_path)
    required_cols = {"feature_name", "formula", "source", "data_type", "business_meaning", "imputation_rule", "leakage_risk"}
    assert required_cols.issubset(set(df.columns)), f"Missing required columns in feature dictionary: {required_cols - set(df.columns)}"
    assert len(df) >= 60, f"Expected at least 60 documented features, got {len(df)}"


def test_derived_features_validity():
    """Verify that computed features (cart_to_page_ratio, engagement_score, etc.) are finite."""
    parquet_path = OUTPUTS_DIR / "customer_features.parquet"
    con = duckdb.connect()

    # Sample 1000 records
    df = con.execute(f"SELECT * FROM read_parquet('{parquet_path.as_posix()}') LIMIT 1000").df()

    assert "cart_to_page_ratio" in df.columns
    assert "engagement_score" in df.columns
    assert "activity_recency_ratio" in df.columns

    # No inf or -inf
    assert not np.isinf(df["cart_to_page_ratio"]).any()
    assert not np.isinf(df["engagement_score"]).any()
    assert not np.isinf(df["activity_recency_ratio"]).any()

    # Ratios non-negative
    assert (df["cart_to_page_ratio"] >= 0).all()
    assert (df["engagement_score"] >= 0).all()
