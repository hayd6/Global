"""
Phase 5 & 6: Benchmark 7 Baseline Machine Learning Models.
Implements unified stratified evaluation with leakage-free ColumnTransformer pipeline.
Models:
1. Logistic Regression
2. Gaussian Naive Bayes
3. Decision Tree
4. Random Forest
5. Gradient Boosting
6. K-Nearest Neighbors (KNN)
7. Support Vector Machine (Linear SVM with log-loss SGD)
"""

import sys
import time
from pathlib import Path

# Add project root to sys.path
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

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

from src.config import (
    OUTPUTS_DIR,
    METRICS_DIR,
    RANDOM_STATE,
    ensure_directories,
    get_logger,
)
from src.evaluation.evaluate import compute_metrics

from src.models.split_manager import get_preprocessed_features

logger = get_logger("baselines")


def prepare_data():
    """
    Loads unified leakage-free stratified train and holdout splits via split_manager.
    Preprocessors fit exclusively on the train set.
    """
    ensure_directories()
    prep = get_preprocessed_features(include_categoricals=True)
    logger.info(f"Loaded unified splits: Train={prep['X_train'].shape}, Holdout={prep['X_holdout'].shape}")
    return {
        "X_train": prep["X_train"],
        "X_val": prep["X_holdout"],
        "y_train": prep["y_train"],
        "y_val": prep["y_holdout"],
        "feature_names": prep["feature_names"],
    }


def train_and_evaluate_baselines(data_dict: dict) -> pd.DataFrame:
    """Trains 7 baseline models and records metrics on the unified holdout split."""
    X_train = data_dict["X_train"]
    X_val = data_dict["X_val"]
    y_train = data_dict["y_train"]
    y_val = data_dict["y_val"]
    n_features = X_train.shape[1]

    # Models definition
    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000, random_state=RANDOM_STATE, class_weight="balanced"
        ),
        "Naive Bayes": GaussianNB(),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=8, min_samples_leaf=50, random_state=RANDOM_STATE, class_weight="balanced"
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=12, min_samples_leaf=20, random_state=RANDOM_STATE, n_jobs=-1, class_weight="balanced"
        ),
        "Gradient Boosting": HistGradientBoostingClassifier(
            max_iter=100, max_depth=6, random_state=RANDOM_STATE, class_weight="balanced"
        ),
        "K-Nearest Neighbors": KNeighborsClassifier(
            n_neighbors=7, n_jobs=-1
        ),
        "SGDClassifier (log_loss)": SGDClassifier(
            loss="log_loss", penalty="l2", alpha=1e-4, max_iter=1000, random_state=RANDOM_STATE, class_weight="balanced"
        ),
    }

    results = []

    for name, model in models.items():
        logger.info(f"Training baseline: {name}...")
        start_time = time.time()

        if name == "K-Nearest Neighbors":
            # For KNN distance scaling on 128k samples, use a representative 25k stratified sample for CPU feasibility
            sub_idx = np.random.RandomState(RANDOM_STATE).choice(len(X_train), size=min(25000, len(X_train)), replace=False)
            model.fit(X_train[sub_idx], y_train[sub_idx])
            # Predict probabilities on validation
            y_prob = model.predict_proba(X_val)[:, 1]
        elif name == "Gradient Boosting":
            model.fit(X_train, y_train)
            y_prob = model.predict_proba(X_val)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_prob = model.predict_proba(X_val)[:, 1]

        fit_time = time.time() - start_time
        logger.info(f"Trained {name} in {fit_time:.2f}s.")

        metrics = compute_metrics(
            y_true=y_val,
            y_prob=y_prob,
            model_name=name,
            feature_count=n_features,
            fit_time=fit_time,
        )
        metrics["split_id"] = "stratified_80_20_v1"
        metrics["feature_space"] = "180_transformed"
        metrics["evaluation_set"] = "holdout_32k"
        logger.info(f"[{name}] PR-AUC: {metrics['pr_auc']:.4f} | ROC-AUC: {metrics['roc_auc']:.4f} | F1: {metrics['f1_score']:.4f}")
        results.append(metrics)

    res_df = pd.DataFrame(results)
    out_path = METRICS_DIR / "baseline_metrics.csv"
    res_df.to_csv(out_path, index=False)
    logger.info(f"Saved baseline metrics to {out_path}")
    return res_df


def run_baselines():
    """Runs Phase 5 and 6 baseline training pipeline."""
    ensure_directories()
    data = prepare_data()
    metrics_df = train_and_evaluate_baselines(data)
    return metrics_df, data


if __name__ == "__main__":
    run_baselines()
