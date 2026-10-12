"""
Master Pipeline: End-to-End Orchestrator for Global E-Commerce Purchase Prediction.
Executes all phases sequentially:
1. Data Audit (inspect_data.py)
2. Cleaning & Integration (clean_data.py & integrate_data.py)
3. Feature Engineering & Dictionary (build_features.py)
4. Exploratory Data Analysis & Visualizations (eda.py)
5. Baseline Modeling (baselines.py)
6. Feature Selection & Binary PSO (feature_selection.py)
7. XGBoost Experiments & Curves (train_xgboost.py)
8. Power BI & Web Dashboard Export (export_outputs.py)
"""

import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import ensure_directories, get_logger
from src.data.inspect_data import run_audit
from src.data.clean_data import run_clean
from src.data.integrate_data import run_integration
from src.features.build_features import run_feature_engineering
from src.analysis.eda import run_eda
from src.models.baselines import run_baselines
from src.models.feature_selection import run_feature_selection_comparison
from src.models.train_xgboost import run_xgboost_experiments
from src.export.export_outputs import export_powerbi_tables

logger = get_logger("pipeline")


def run_full_pipeline():
    """Runs the entire Big Data & ML pipeline from raw CSVs to final outputs."""
    start_total_time = time.time()
    ensure_directories()
    logger.info("=" * 70)
    logger.info("STARTING COMPLETE BIG DATA & MACHINE LEARNING PIPELINE")
    logger.info("Project: Global E-Commerce Customer Purchase Prediction")
    logger.info("Research: Khai pha dac trung hanh vi va toi uu bang PSO")
    logger.info("=" * 70)

    # Phase 1: Data Audit
    t0 = time.time()
    logger.info("\n>>> [1/8] Executing Phase 1: Data Audit...")
    run_audit()
    logger.info(f">>> [1/8] Phase 1 completed in {time.time() - t0:.2f}s.")

    # Phase 2: Data Cleaning & Integration
    t0 = time.time()
    logger.info("\n>>> [2/8] Executing Phase 2: Cleaning & Integration via DuckDB...")
    run_clean()
    run_integration()
    logger.info(f">>> [2/8] Phase 2 completed in {time.time() - t0:.2f}s.")

    # Phase 3 & 4: Feature Engineering
    t0 = time.time()
    logger.info("\n>>> [3/8] Executing Phase 3 & 4: Advanced Feature Engineering...")
    run_feature_engineering()
    logger.info(f">>> [3/8] Phase 3 & 4 Feature Engineering completed in {time.time() - t0:.2f}s.")

    # Phase 4: EDA Visualizations
    t0 = time.time()
    logger.info("\n>>> [4/8] Executing Phase 4: Exploratory Data Analysis & Plots...")
    run_eda()
    logger.info(f">>> [4/8] Phase 4 EDA completed in {time.time() - t0:.2f}s.")

    # Phase 5 & 6: 7 Baseline Models
    t0 = time.time()
    logger.info("\n>>> [5/8] Executing Phase 5 & 6: Benchmarking 7 Baseline Models...")
    run_baselines()
    logger.info(f">>> [5/8] Phase 5 & 6 Baselines completed in {time.time() - t0:.2f}s.")

    # Phase 7: Feature Selection & Binary PSO
    t0 = time.time()
    logger.info("\n>>> [6/8] Executing Phase 7: Feature Selection & Binary PSO...")
    run_feature_selection_comparison()
    logger.info(f">>> [6/8] Phase 7 Feature Selection & PSO completed in {time.time() - t0:.2f}s.")

    # Phase 8: XGBoost & Comparative Experiments
    t0 = time.time()
    logger.info("\n>>> [7/8] Executing Phase 8: XGBoost Experiments & Evaluation Curves...")
    run_xgboost_experiments()
    logger.info(f">>> [7/8] Phase 8 XGBoost completed in {time.time() - t0:.2f}s.")

    # Phase 9: Power BI Export
    t0 = time.time()
    logger.info("\n>>> [8/8] Executing Phase 9: Exporting Power BI Tables...")
    export_powerbi_tables()
    logger.info(f">>> [8/8] Phase 9 Power BI export completed in {time.time() - t0:.2f}s.")

    total_duration = time.time() - start_total_time
    logger.info("\n" + "=" * 70)
    logger.info(f"ALL PIPELINE PHASES EXECUTED SUCCESSFULLY IN {total_duration:.2f}s ({total_duration/60:.2f} mins)!")
    logger.info("All reports, metrics, charts, and models persisted to outputs/.")
    logger.info("=" * 70)


if __name__ == "__main__":
    run_full_pipeline()
