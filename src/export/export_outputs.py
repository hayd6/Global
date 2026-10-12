"""
Phase 9: Export Outputs for Power BI Dashboard & Research Website.
Generates clean, aggregated, executive-ready analytical tables in outputs/powerbi/.
"""

import sys
import shutil
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
import pandas as pd
import numpy as np

from src.config import (
    OUTPUTS_DIR,
    METRICS_DIR,
    FEATURE_SEL_DIR,
    POWERBI_DIR,
    ensure_directories,
    get_logger,
)

logger = get_logger("export_outputs")


def export_powerbi_tables():
    """Generates all consolidated summary tables for Power BI and dashboards."""
    ensure_directories()
    con = duckdb.connect()
    parquet_path = OUTPUTS_DIR / "customer_features.parquet"

    logger.info("Exporting tables for Power BI and web dashboards...")

    # 1. Copy metrics and model results
    shutil.copy(METRICS_DIR / "metrics_comparison.csv", POWERBI_DIR / "metrics_comparison.csv")
    shutil.copy(FEATURE_SEL_DIR / "pso_selected_features.csv", POWERBI_DIR / "pso_selected_features.csv")
    shutil.copy(FEATURE_SEL_DIR / "pso_convergence.csv", POWERBI_DIR / "pso_convergence.csv")
    shutil.copy(FEATURE_SEL_DIR / "feature_importance.csv", POWERBI_DIR / "feature_importance.csv")
    logger.info("Copied metrics, PSO results, and feature importance to outputs/powerbi/.")

    # 2. Generate outputs/powerbi/dashboard_customer_summary.csv (Granular Customer Level - 200,000 rows)
    # Matches DanY6Phan.md, DATA_MODEL_SCHEMA.md, and POWER_BI_SPECIFICATION.md
    con.execute(
        f"""
        COPY (
            SELECT 
                customer_id,
                split_type AS split_group,
                target,
                age,
                country_code AS country,
                customer_tier,
                ROUND(loyalty_score, 4) AS loyalty_score,
                ROUND(total_spend, 2) AS total_spend,
                trans_count AS transaction_count,
                sess_count AS total_sessions,
                ROUND(avg_session_duration, 1) AS avg_session_duration_sec,
                ROUND(avg_pages_viewed, 2) AS avg_pages_per_session,
                total_cart_additions,
                ROUND(bounce_rate, 4) AS bounce_rate,
                COALESCE(region_tier, 'Unknown') AS marketing_campaign_tier,
                CASE 
                    WHEN pct_mobile_sessions >= 0.5 THEN 'Mobile'
                    WHEN pct_desktop_sessions >= 0.5 THEN 'Desktop'
                    WHEN pct_tablet_sessions >= 0.5 THEN 'Tablet'
                    ELSE 'Mixed'
                END AS preferred_device
            FROM read_parquet('{parquet_path.as_posix()}')
            ORDER BY customer_id
        ) TO '{(POWERBI_DIR / "dashboard_customer_summary.csv").as_posix()}' (HEADER, DELIMITER ',')
        """
    )
    logger.info("Exported outputs/powerbi/dashboard_customer_summary.csv (200,000 rows)")

    # 2b. Generate outputs/powerbi/dashboard_tier_region_summary.csv (Macro 17-row cohort aggregate)
    con.execute(
        f"""
        COPY (
            SELECT 
                customer_tier,
                COALESCE(region_tier, 'Unknown') AS region_tier,
                COUNT(*) AS total_customers,
                ROUND(AVG(target), 4) AS purchase_conversion_rate,
                ROUND(AVG(loyalty_score), 4) AS avg_loyalty_score,
                ROUND(AVG(credit_limit), 2) AS avg_credit_limit,
                ROUND(AVG(total_spend), 2) AS avg_total_spend,
                ROUND(AVG(total_cart_additions), 2) AS avg_cart_additions,
                ROUND(AVG(account_age_days), 1) AS avg_account_age_days
            FROM read_parquet('{parquet_path.as_posix()}')
            WHERE split_type = 'train'
            GROUP BY customer_tier, region_tier
            ORDER BY customer_tier, region_tier
        ) TO '{(POWERBI_DIR / "dashboard_tier_region_summary.csv").as_posix()}' (HEADER, DELIMITER ',')
        """
    )
    logger.info("Exported outputs/powerbi/dashboard_tier_region_summary.csv (17 cohort rows)")

    # 3. Generate outputs/powerbi/dashboard_behavior_summary.csv
    # Behavioral summary grouped by target, primary traffic channels and devices
    con.execute(
        f"""
        COPY (
            SELECT
                target,
                CASE 
                    WHEN pct_mobile_sessions >= 0.5 THEN 'Mobile Heavy'
                    WHEN pct_desktop_sessions >= 0.5 THEN 'Desktop Heavy'
                    ELSE 'Balanced Device'
                END AS device_persona,
                CASE 
                    WHEN pct_organic_sessions >= 0.4 THEN 'Organic'
                    WHEN pct_ads_sessions >= 0.4 THEN 'Paid Ads'
                    WHEN pct_email_sessions >= 0.4 THEN 'Email'
                    WHEN pct_social_sessions >= 0.4 THEN 'Social'
                    ELSE 'Multi-channel'
                END AS acquisition_channel,
                COUNT(*) AS customer_count,
                ROUND(AVG(sess_count), 2) AS avg_session_count,
                ROUND(AVG(avg_session_duration), 1) AS avg_session_duration_sec,
                ROUND(AVG(total_pages_viewed), 1) AS avg_pages_viewed,
                ROUND(AVG(total_cart_additions), 2) AS avg_cart_additions,
                ROUND(AVG(bounce_rate), 4) AS avg_bounce_rate,
                ROUND(AVG(total_spend), 2) AS avg_spend_usd
            FROM read_parquet('{parquet_path.as_posix()}')
            WHERE split_type = 'train'
            GROUP BY target, device_persona, acquisition_channel
            ORDER BY target, customer_count DESC
        ) TO '{(POWERBI_DIR / "dashboard_behavior_summary.csv").as_posix()}' (HEADER, DELIMITER ',')
        """
    )
    logger.info("Exported outputs/powerbi/dashboard_behavior_summary.csv")

    # 4. Export test predictions sample for Power BI consumption
    pred_path = OUTPUTS_DIR / "test_predictions.csv"
    if pred_path.exists():
        shutil.copy(pred_path, POWERBI_DIR / "test_predictions_sample.csv")
        logger.info("Exported test predictions sample to outputs/powerbi/test_predictions_sample.csv")

    logger.info("=== POWER BI EXPORT PHASE COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    export_powerbi_tables()
