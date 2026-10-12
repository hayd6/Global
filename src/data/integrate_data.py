"""
Phase 2 & Phase 3: Data Integration and Customer-Level Feature Aggregation using DuckDB.
Ensures zero cartesian-product expansion by pre-aggregating sessions and transactions
before joining with customers, geo_data, and marketing_campaigns.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
import pandas as pd
from src.config import (
    TRAIN_CSV,
    TEST_CSV,
    PROCESSED_DATA_DIR,
    OUTPUTS_DIR,
    ensure_directories,
    get_logger,
)
from src.data.clean_data import create_cleaned_views

logger = get_logger("integrate_data")


def integrate_customer_data(con: duckdb.DuckDBPyConnection) -> str:
    """
    Performs full aggregation and multi-table integration using DuckDB SQL.
    Outputs a consolidated customer-level feature dataset.
    """
    ensure_directories()
    create_cleaned_views(con)
    logger.info("Aggregating sessions and transactions by customer_id...")

    # 1. Sessions Aggregation
    con.execute(
        """
        CREATE OR REPLACE VIEW v_sessions_agg AS
        WITH ranked_geo AS (
            SELECT 
                customer_id, 
                geo_ip_region,
                COUNT(*) as region_cnt,
                ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY COUNT(*) DESC) as rn
            FROM v_cleaned_sessions
            WHERE geo_ip_region IS NOT NULL
            GROUP BY customer_id, geo_ip_region
        ),
        ranked_campaign AS (
            SELECT 
                customer_id, 
                campaign_id,
                COUNT(*) as camp_cnt,
                ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY COUNT(*) DESC) as rn
            FROM v_cleaned_sessions
            WHERE campaign_id IS NOT NULL
            GROUP BY customer_id, campaign_id
        ),
        dominant_geo AS (
            SELECT customer_id, geo_ip_region AS dominant_geo_ip_region
            FROM ranked_geo WHERE rn = 1
        ),
        dominant_camp AS (
            SELECT customer_id, campaign_id AS dominant_campaign_id
            FROM ranked_campaign WHERE rn = 1
        ),
        metrics AS (
            SELECT
                customer_id,
                COUNT(*) AS sess_count,
                COALESCE(SUM(session_duration), 0.0) AS total_session_duration,
                COALESCE(AVG(session_duration), 0.0) AS avg_session_duration,
                COALESCE(MAX(session_duration), 0.0) AS max_session_duration,
                COALESCE(SUM(pages_viewed), 0) AS total_pages_viewed,
                COALESCE(AVG(pages_viewed), 0.0) AS avg_pages_viewed,
                COALESCE(SUM(cart_additions), 0) AS total_cart_additions,
                COALESCE(AVG(cart_additions), 0.0) AS avg_cart_additions,
                COALESCE(AVG(is_bounce), 0.0) AS bounce_rate,
                AVG(CASE WHEN traffic_source = 'organic' THEN 1.0 ELSE 0.0 END) AS pct_organic_sessions,
                AVG(CASE WHEN traffic_source = 'ads' THEN 1.0 ELSE 0.0 END) AS pct_ads_sessions,
                AVG(CASE WHEN traffic_source = 'email' THEN 1.0 ELSE 0.0 END) AS pct_email_sessions,
                AVG(CASE WHEN traffic_source = 'social' THEN 1.0 ELSE 0.0 END) AS pct_social_sessions,
                AVG(CASE WHEN device_type = 'mobile' THEN 1.0 ELSE 0.0 END) AS pct_mobile_sessions,
                AVG(CASE WHEN device_type = 'desktop' THEN 1.0 ELSE 0.0 END) AS pct_desktop_sessions,
                AVG(CASE WHEN device_type = 'tablet' THEN 1.0 ELSE 0.0 END) AS pct_tablet_sessions,
                DATE_DIFF('day', MAX(session_timestamp), DATE '2024-09-26') AS days_since_last_session
            FROM v_cleaned_sessions
            GROUP BY customer_id
        )
        SELECT 
            m.*,
            g.dominant_geo_ip_region,
            c.dominant_campaign_id
        FROM metrics m
        LEFT JOIN dominant_geo g ON m.customer_id = g.customer_id
        LEFT JOIN dominant_camp c ON m.customer_id = c.customer_id
        """
    )
    logger.info("View 'v_sessions_agg' created.")

    # 2. Transactions Aggregation
    con.execute(
        """
        CREATE OR REPLACE VIEW v_transactions_agg AS
        SELECT
            customer_id,
            COUNT(*) AS trans_count,
            1 AS has_transactions,
            COALESCE(SUM(order_value), 0.0) AS total_spend,
            COALESCE(AVG(order_value), 0.0) AS avg_order_value,
            COALESCE(MAX(order_value), 0.0) AS max_order_value,
            COALESCE(MIN(order_value), 0.0) AS min_order_value,
            COALESCE(SUM(items_count), 0) AS total_items_count,
            COALESCE(AVG(items_count), 0.0) AS avg_items_per_order,
            COALESCE(AVG(discount_applied), 0.0) AS trans_discount_rate,
            COALESCE(SUM(high_value_flag), 0) AS high_value_trans_count,
            COALESCE(AVG(high_value_flag), 0.0) AS high_value_trans_ratio,
            AVG(CASE WHEN payment_method = 'credit_card' THEN 1.0 ELSE 0.0 END) AS pct_credit_card,
            AVG(CASE WHEN payment_method = 'debit_card' THEN 1.0 ELSE 0.0 END) AS pct_debit_card,
            AVG(CASE WHEN payment_method = 'paypal' THEN 1.0 ELSE 0.0 END) AS pct_paypal,
            AVG(CASE WHEN payment_method = 'crypto' THEN 1.0 ELSE 0.0 END) AS pct_crypto,
            AVG(CASE WHEN shipping_speed = 'standard' THEN 1.0 ELSE 0.0 END) AS pct_standard_shipping,
            AVG(CASE WHEN shipping_speed = 'express' THEN 1.0 ELSE 0.0 END) AS pct_express_shipping,
            AVG(CASE WHEN shipping_speed = 'overnight' THEN 1.0 ELSE 0.0 END) AS pct_overnight_shipping,
            AVG(noise_trans_0) AS avg_noise_trans_0,
            AVG(noise_trans_1) AS avg_noise_trans_1,
            DATE_DIFF('day', MAX(transaction_timestamp), DATE '2024-09-26') AS days_since_last_transaction
        FROM v_cleaned_transactions
        GROUP BY customer_id
        """
    )
    logger.info("View 'v_transactions_agg' created.")

    # 3. Full Integrated Customer Feature Table
    output_parquet_path = PROCESSED_DATA_DIR / "clean_customer_features.parquet"
    logger.info(f"Writing integrated customer dataset to {output_parquet_path}...")

    con.execute(
        f"""
        COPY (
            SELECT
                -- Identifiers
                c.customer_id,
                
                -- Split and Target
                CASE 
                    WHEN tr.customer_id IS NOT NULL THEN 'train'
                    WHEN te.customer_id IS NOT NULL THEN 'test'
                    ELSE 'unassigned'
                END AS split_type,
                tr.target,

                -- Customer Demographics & Profile
                c.age,
                c.country_code,
                c.region,
                c.customer_tier,
                c.credit_limit,
                c.loyalty_score,
                c.email_open_rate,
                c.discount_usage_rate,
                c.avg_review_score,
                CASE WHEN c.referral_code IS NOT NULL THEN 1 ELSE 0 END AS has_referral_code,
                DATE_DIFF('day', c.signup_date, DATE '2024-09-26') AS account_age_days,

                -- Synthetic noise variables (tracked for PSO testing)
                c.noise_customer_0,
                c.noise_customer_1,
                c.noise_customer_2,
                c.noise_customer_3,
                c.noise_customer_4,

                -- Aggregated Session Features
                COALESCE(s.sess_count, 0) AS sess_count,
                COALESCE(s.total_session_duration, 0.0) AS total_session_duration,
                COALESCE(s.avg_session_duration, 0.0) AS avg_session_duration,
                COALESCE(s.max_session_duration, 0.0) AS max_session_duration,
                COALESCE(s.total_pages_viewed, 0) AS total_pages_viewed,
                COALESCE(s.avg_pages_viewed, 0.0) AS avg_pages_viewed,
                COALESCE(s.total_cart_additions, 0) AS total_cart_additions,
                COALESCE(s.avg_cart_additions, 0.0) AS avg_cart_additions,
                COALESCE(s.bounce_rate, 0.0) AS bounce_rate,
                COALESCE(s.pct_organic_sessions, 0.0) AS pct_organic_sessions,
                COALESCE(s.pct_ads_sessions, 0.0) AS pct_ads_sessions,
                COALESCE(s.pct_email_sessions, 0.0) AS pct_email_sessions,
                COALESCE(s.pct_social_sessions, 0.0) AS pct_social_sessions,
                COALESCE(s.pct_mobile_sessions, 0.0) AS pct_mobile_sessions,
                COALESCE(s.pct_desktop_sessions, 0.0) AS pct_desktop_sessions,
                COALESCE(s.pct_tablet_sessions, 0.0) AS pct_tablet_sessions,
                COALESCE(s.days_since_last_session, 9999) AS days_since_last_session,

                -- Aggregated Transaction Features
                COALESCE(t.has_transactions, 0) AS has_transactions,
                COALESCE(t.trans_count, 0) AS trans_count,
                COALESCE(t.total_spend, 0.0) AS total_spend,
                COALESCE(t.avg_order_value, 0.0) AS avg_order_value,
                COALESCE(t.max_order_value, 0.0) AS max_order_value,
                COALESCE(t.min_order_value, 0.0) AS min_order_value,
                COALESCE(t.total_items_count, 0) AS total_items_count,
                COALESCE(t.avg_items_per_order, 0.0) AS avg_items_per_order,
                COALESCE(t.trans_discount_rate, 0.0) AS trans_discount_rate,
                COALESCE(t.high_value_trans_count, 0) AS high_value_trans_count,
                COALESCE(t.high_value_trans_ratio, 0.0) AS high_value_trans_ratio,
                COALESCE(t.pct_credit_card, 0.0) AS pct_credit_card,
                COALESCE(t.pct_debit_card, 0.0) AS pct_debit_card,
                COALESCE(t.pct_paypal, 0.0) AS pct_paypal,
                COALESCE(t.pct_crypto, 0.0) AS pct_crypto,
                COALESCE(t.pct_standard_shipping, 0.0) AS pct_standard_shipping,
                COALESCE(t.pct_express_shipping, 0.0) AS pct_express_shipping,
                COALESCE(t.pct_overnight_shipping, 0.0) AS pct_overnight_shipping,
                COALESCE(t.avg_noise_trans_0, 0.0) AS avg_noise_trans_0,
                COALESCE(t.avg_noise_trans_1, 0.0) AS avg_noise_trans_1,
                COALESCE(t.days_since_last_transaction, 9999) AS days_since_last_transaction,

                -- Geo Features
                g.average_income,
                g.urban_ratio,
                g.internet_penetration,
                g.region_tier,

                -- Marketing Campaign Features
                mc.campaign_type AS primary_campaign_type,
                mc.campaign_budget AS primary_campaign_budget

            FROM v_cleaned_customers c
            LEFT JOIN v_sessions_agg s ON c.customer_id = s.customer_id
            LEFT JOIN v_transactions_agg t ON c.customer_id = t.customer_id
            LEFT JOIN v_cleaned_geo g ON s.dominant_geo_ip_region = g.geo_ip_region
            LEFT JOIN v_cleaned_marketing mc ON s.dominant_campaign_id = mc.campaign_id
            LEFT JOIN read_csv_auto('{TRAIN_CSV.as_posix()}') tr ON c.customer_id = tr.customer_id
            LEFT JOIN read_csv_auto('{TEST_CSV.as_posix()}') te ON c.customer_id = te.customer_id
        ) TO '{output_parquet_path.as_posix()}' (FORMAT PARQUET)
        """
    )

    # Verification query
    total_cust = con.execute(f"SELECT COUNT(*) FROM read_parquet('{output_parquet_path.as_posix()}')").fetchone()[0]
    unique_cust = con.execute(f"SELECT COUNT(DISTINCT customer_id) FROM read_parquet('{output_parquet_path.as_posix()}')").fetchone()[0]
    train_cust = con.execute(f"SELECT COUNT(*) FROM read_parquet('{output_parquet_path.as_posix()}') WHERE split_type = 'train'").fetchone()[0]
    test_cust = con.execute(f"SELECT COUNT(*) FROM read_parquet('{output_parquet_path.as_posix()}') WHERE split_type = 'test'").fetchone()[0]
    cols = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{output_parquet_path.as_posix()}') LIMIT 0").fetchall()

    logger.info(f"Integration complete: {total_cust:,} total customers ({unique_cust:,} unique).")
    logger.info(f"Split distribution: {train_cust:,} train, {test_cust:,} test. Total columns: {len(cols)}.")

    assert total_cust == 200000, f"Expected 200,000 customers, got {total_cust}"
    assert unique_cust == 200000, f"Expected 200,000 unique customers, got {unique_cust}"
    assert train_cust == 160000, f"Expected 160,000 train customers, got {train_cust}"
    assert test_cust == 40000, f"Expected 40,000 test customers, got {test_cust}"

    # Also save a 10,000-row sample CSV for quick inspection and compatibility
    sample_csv_path = PROCESSED_DATA_DIR / "clean_customer_features_sample.csv"
    con.execute(f"COPY (SELECT * FROM read_parquet('{output_parquet_path.as_posix()}') LIMIT 10000) TO '{sample_csv_path.as_posix()}' (HEADER, DELIMITER ',')")
    logger.info(f"Saved sample CSV to {sample_csv_path}")

    return str(output_parquet_path)


def run_integration():
    """Runs data integration pipeline."""
    ensure_directories()
    con = duckdb.connect()
    parquet_path = integrate_customer_data(con)
    return parquet_path


if __name__ == "__main__":
    run_integration()
