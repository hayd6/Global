"""
Global Configuration and Constants for E-Commerce Purchase Prediction Project.
"""

import os
import sys
from pathlib import Path
import logging

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "dataset"
OUTPUTS_DIR = BASE_DIR / "outputs"
LOGS_DIR = BASE_DIR / "logs"
CONFIGS_DIR = BASE_DIR / "configs"

# Sub-output directories
EDA_DIR = OUTPUTS_DIR / "eda"
METRICS_DIR = OUTPUTS_DIR / "metrics"
PLOTS_DIR = OUTPUTS_DIR / "plots"
FEATURE_SEL_DIR = OUTPUTS_DIR / "feature_selection"
POWERBI_DIR = OUTPUTS_DIR / "powerbi"
PROCESSED_DATA_DIR = OUTPUTS_DIR / "processed"

# Dataset paths
CUSTOMERS_CSV = DATA_DIR / "customers.csv"
GEO_DATA_CSV = DATA_DIR / "geo_data.csv"
MARKETING_CSV = DATA_DIR / "marketing_campaigns.csv"
SESSIONS_CSV = DATA_DIR / "sessions.csv"
TRANSACTIONS_CSV = DATA_DIR / "transactions.csv"
TRAIN_CSV = DATA_DIR / "train.csv"
TEST_CSV = DATA_DIR / "test.csv"
SAMPLE_SUBMISSION_CSV = DATA_DIR / "sample_submission.csv"

# Global Random State
RANDOM_STATE = 42

# Ensure all directories exist
def ensure_directories():
    for d in [
        OUTPUTS_DIR,
        LOGS_DIR,
        CONFIGS_DIR,
        EDA_DIR,
        METRICS_DIR,
        PLOTS_DIR,
        FEATURE_SEL_DIR,
        POWERBI_DIR,
        PROCESSED_DATA_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)

# Logger setup
def get_logger(name: str = "ecommerce_ml") -> logging.Logger:
    ensure_directories()
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File handler
        fh = logging.FileHandler(LOGS_DIR / "pipeline.log", encoding="utf-8")
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger
