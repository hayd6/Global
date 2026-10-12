"""
src/pipeline_controlled.py
Master End-to-End Execution Pipeline for Controlled Benchmark Dataset.
Executes the full workflow in one reproducible pass:
1. Controlled Data Generation (src/data/generate_controlled_benchmark.py)
2. Point-in-Time Feature Engineering (src/features/build_point_in_time_features.py)
3. Model Training, PSO Feature Selection & Holdout Evaluation (src/models/train_pit_models.py)
4. Comprehensive Manifest & Acceptance Summary Export
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import get_logger, OUTPUTS_DIR
from src.data.generate_controlled_benchmark import generate_controlled_benchmark_dataset
from src.features.build_point_in_time_features import build_point_in_time_features
from src.models.train_pit_models import run_point_in_time_experiments

logger = get_logger("pipeline_controlled")


def run_controlled_pipeline():
    """Runs the full reproducible pipeline from generation to evaluation."""
    start_time = time.time()
    logger.info("=================================================================")
    logger.info("STARTING CONTROLLED BENCHMARK & POINT-IN-TIME ML PIPELINE")
    logger.info("=================================================================")

    # Step 1: Generate Controlled Benchmark Dataset
    logger.info(">>> STEP 1/3: Generating Controlled Longitudinal Benchmark Dataset...")
    manifest = generate_controlled_benchmark_dataset(n_customers=25000, random_state=42)

    # Step 2: Point-in-Time Feature Engineering
    logger.info(">>> STEP 2/3: Executing Point-in-Time Feature Extraction (Cutoff t_0 = 2024-06-01)...")
    pq_path = build_point_in_time_features(cutoff_date="2024-06-01")

    # Step 3: Train Models, PSO, and Evaluate Holdout
    logger.info(">>> STEP 3/3: Running Baselines, ANOVA, Binary PSO, and Holdout Evaluation...")
    results = run_point_in_time_experiments()

    total_elapsed = round(time.time() - start_time, 2)
    logger.info("=================================================================")
    logger.info(f"CONTROLLED PIPELINE COMPLETED SUCCESSFULLY IN {total_elapsed} SECONDS")
    logger.info(f"All deliverables stored in: {OUTPUTS_DIR / 'controlled_benchmark'}")
    logger.info("=================================================================")
    return {
        "manifest": manifest,
        "parquet_path": pq_path,
        "results": results,
        "total_elapsed_seconds": total_elapsed,
    }


if __name__ == "__main__":
    run_controlled_pipeline()
