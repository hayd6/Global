"""
Unified Split Manager: Guarantees Leakage-Free, Stratified Partitions Across All Experiments.
Divides the 160,000 train pool into:
- 80% Train Split (128,000 customers) for model training and preprocessing fitting.
- 20% Final Holdout Split (32,000 customers) strictly reserved for final comparative evaluation.
- Inner Tuning Partition (from Train Split only) for PSO search and hyperparameter tuning.
"""

import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, Tuple, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.config import (
    OUTPUTS_DIR,
    CONFIGS_DIR,
    RANDOM_STATE,
    ensure_directories,
    get_logger,
)

logger = get_logger("split_manager")

SPLIT_METADATA_FILE = CONFIGS_DIR / "split_metadata.json"
SPLIT_INDICES_FILE = OUTPUTS_DIR / "processed" / "split_indices.npz"


def create_or_load_splits() -> Dict:
    """
    Creates or loads standardized train/holdout splits and saves split metadata.
    Guarantees that every model evaluates on the exact same holdout customers.
    """
    ensure_directories()
    con = duckdb.connect()
    parquet_path = OUTPUTS_DIR / "customer_features.parquet"

    df = con.execute(
        f"""
        SELECT * 
        FROM read_parquet('{parquet_path.as_posix()}')
        WHERE split_type = 'train'
        ORDER BY customer_id
        """
    ).df()

    drop_cols = [
        "customer_id",
        "split_type",
        "target",
        "dominant_geo_ip_region",
        "dominant_campaign_id",
        "primary_campaign_type",
        "primary_campaign_budget",
    ]
    candidate_cols = [c for c in df.columns if c not in drop_cols]
    customer_ids = df["customer_id"].values
    y = df["target"].values.astype(int)

    # Check if split indices already saved
    if SPLIT_INDICES_FILE.exists() and SPLIT_METADATA_FILE.exists():
        logger.info(f"Loading cached split indices from {SPLIT_INDICES_FILE}...")
        data = np.load(SPLIT_INDICES_FILE)
        train_idx = data["train_idx"]
        holdout_idx = data["holdout_idx"]
        pso_inner_train_idx = data["pso_inner_train_idx"]
        pso_inner_val_idx = data["pso_inner_val_idx"]
    else:
        logger.info("Generating unified stratified splits (80% Train, 20% Holdout)...")
        indices = np.arange(len(df))
        train_idx, holdout_idx = train_test_split(
            indices, test_size=0.20, random_state=RANDOM_STATE, stratify=y
        )

        # Inner split for PSO from Train Split ONLY (never touching holdout!)
        y_train_pool = y[train_idx]
        inner_tr_sub, inner_va_sub = train_test_split(
            np.arange(len(train_idx)), test_size=0.25, random_state=RANDOM_STATE, stratify=y_train_pool
        )
        pso_inner_train_idx = train_idx[inner_tr_sub]
        pso_inner_val_idx = train_idx[inner_va_sub]

        # Save indices
        np.savez_compressed(
            SPLIT_INDICES_FILE,
            train_idx=train_idx,
            holdout_idx=holdout_idx,
            pso_inner_train_idx=pso_inner_train_idx,
            pso_inner_val_idx=pso_inner_val_idx,
        )

        # Metadata
        meta = {
            "split_id": "stratified_80_20_v1",
            "random_state": RANDOM_STATE,
            "total_train_pool_size": len(df),
            "train_size": len(train_idx),
            "holdout_size": len(holdout_idx),
            "pso_inner_train_size": len(pso_inner_train_idx),
            "pso_inner_val_size": len(pso_inner_val_idx),
            "positive_rate_overall": round(float(np.mean(y)), 5),
            "positive_rate_train": round(float(np.mean(y[train_idx])), 5),
            "positive_rate_holdout": round(float(np.mean(y[holdout_idx])), 5),
            "train_customer_id_sample": [int(x) for x in customer_ids[train_idx][:5]],
            "holdout_customer_id_sample": [int(x) for x in customer_ids[holdout_idx][:5]],
            "holdout_sha256": hashlib.sha256(customer_ids[holdout_idx].tobytes()).hexdigest(),
        }
        with open(SPLIT_METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4)
        logger.info(f"Saved split metadata to {SPLIT_METADATA_FILE}")

    return {
        "df": df,
        "candidate_cols": candidate_cols,
        "customer_ids": customer_ids,
        "y": y,
        "train_idx": train_idx,
        "holdout_idx": holdout_idx,
        "pso_inner_train_idx": pso_inner_train_idx,
        "pso_inner_val_idx": pso_inner_val_idx,
    }


def get_preprocessed_features(include_categoricals: bool = False):
    """
    Returns properly preprocessed train and holdout datasets.
    Preprocessors fit exclusively on train partition.
    """
    splits = create_or_load_splits()
    df = splits["df"]
    candidate_cols = splits["candidate_cols"]
    y = splits["y"]
    train_idx = splits["train_idx"]
    holdout_idx = splits["holdout_idx"]

    if include_categoricals:
        cat_cols = [
            c for c in candidate_cols
            if pd.api.types.is_string_dtype(df[c]) or pd.api.types.is_object_dtype(df[c])
        ]
        num_cols = [c for c in candidate_cols if c not in cat_cols]

        num_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])
        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ])
        preprocessor = ColumnTransformer([
            ("num", num_pipeline, num_cols),
            ("cat", cat_pipeline, cat_cols),
        ])

        # FIT EXCLUSIVELY ON TRAIN
        X_train_raw = df[candidate_cols].iloc[train_idx]
        X_holdout_raw = df[candidate_cols].iloc[holdout_idx]

        X_train = preprocessor.fit_transform(X_train_raw)
        X_holdout = preprocessor.transform(X_holdout_raw)

        cat_names = list(preprocessor.named_transformers_["cat"].named_steps["onehot"].get_feature_names_out(cat_cols))
        feature_names = num_cols + cat_names
    else:
        # Pure numerical feature space (63 candidate features)
        num_cols = [
            c for c in candidate_cols
            if not (pd.api.types.is_string_dtype(df[c]) or pd.api.types.is_object_dtype(df[c]))
        ]
        num_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])
        
        X_train_raw = df[num_cols].iloc[train_idx]
        X_holdout_raw = df[num_cols].iloc[holdout_idx]

        X_train = num_pipeline.fit_transform(X_train_raw)
        X_holdout = num_pipeline.transform(X_holdout_raw)
        feature_names = num_cols

    return {
        "X_train": X_train,
        "X_holdout": X_holdout,
        "y_train": y[train_idx],
        "y_holdout": y[holdout_idx],
        "feature_names": feature_names,
        "splits": splits,
        "preprocessor": preprocessor if include_categoricals else num_pipeline,
    }
