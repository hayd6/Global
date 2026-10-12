"""
Phase 2: Data Cleaning Module using DuckDB.
Standardizes messy data formats (currency symbols, mixed boolean representations,
missing placeholders, and inconsistent categorical casing) into cleaned views.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
from src.config import (
    CUSTOMERS_CSV,
    GEO_DATA_CSV,
    MARKETING_CSV,
    SESSIONS_CSV,
    TRANSACTIONS_CSV,
    ensure_directories,
    get_logger,
)

logger = get_logger("clean_data")


def create_cleaned_views(con: duckdb.DuckDBPyConnection):
    """
    Creates normalized SQL views in DuckDB for all tables.
    Deterministic rules:
    - Currency: remove '$' and ',', cast to DOUBLE
    - Mixed Booleans: map ('1', 'true', 'yes') -> 1, ('0', 'false', 'no') -> 0
    - Text placehoders: 'unknown' -> NULL, 'N/A' -> NULL
    - Categoricals: lower() and trim()
    """
    logger.info("Creating cleaned SQL views in DuckDB...")

    # 1. Cleaned Customers View
    con.execute(
        f"""
        CREATE OR REPLACE VIEW v_cleaned_customers AS
        SELECT
            customer_id,
            TRY_CAST(NULLIF(TRIM(age), 'unknown') AS INTEGER) AS age,
            TRIM(country_code) AS country_code,
            TRIM(region) AS region,
            signup_date,
            loyalty_score,
            email_open_rate,
            discount_usage_rate,
            avg_review_score,
            NULLIF(TRIM(referral_code), '') AS referral_code,
            TRIM(customer_tier) AS customer_tier,
            TRY_CAST(REPLACE(REPLACE(TRIM(credit_limit), '$', ''), ',', '') AS DOUBLE) AS credit_limit,
            noise_customer_0,
            noise_customer_1,
            noise_customer_2,
            noise_customer_3,
            noise_customer_4
        FROM read_csv_auto('{CUSTOMERS_CSV.as_posix()}')
        """
    )
    logger.info("View 'v_cleaned_customers' created.")

    # 2. Cleaned Sessions View
    con.execute(
        f"""
        CREATE OR REPLACE VIEW v_cleaned_sessions AS
        SELECT
            session_id,
            customer_id,
            session_timestamp,
            session_duration,
            TRY_CAST(NULLIF(TRIM(pages_viewed), 'N/A') AS INTEGER) AS pages_viewed,
            cart_additions,
            CASE 
                WHEN LOWER(TRIM(bounce_flag)) IN ('1', 'true', 'yes') THEN 1
                WHEN LOWER(TRIM(bounce_flag)) IN ('0', 'false', 'no') THEN 0
                ELSE NULL
            END AS is_bounce,
            LOWER(TRIM(traffic_source)) AS traffic_source,
            LOWER(TRIM(device_type)) AS device_type,
            campaign_id,
            TRIM(geo_ip_region) AS geo_ip_region
        FROM read_csv_auto('{SESSIONS_CSV.as_posix()}')
        """
    )
    logger.info("View 'v_cleaned_sessions' created.")

    # 3. Cleaned Transactions View
    con.execute(
        f"""
        CREATE OR REPLACE VIEW v_cleaned_transactions AS
        SELECT
            transaction_id,
            customer_id,
            transaction_timestamp,
            TRY_CAST(REPLACE(REPLACE(TRIM(order_value), '$', ''), ',', '') AS DOUBLE) AS order_value,
            items_count,
            LOWER(TRIM(payment_method)) AS payment_method,
            CASE 
                WHEN LOWER(TRIM(discount_applied)) IN ('1', 'true', 'yes') THEN 1
                WHEN LOWER(TRIM(discount_applied)) IN ('0', 'false', 'no') THEN 0
                ELSE NULL
            END AS discount_applied,
            LOWER(TRIM(shipping_speed)) AS shipping_speed,
            CASE WHEN high_value_flag = true THEN 1 ELSE 0 END AS high_value_flag,
            noise_trans_0,
            noise_trans_1
        FROM read_csv_auto('{TRANSACTIONS_CSV.as_posix()}')
        """
    )
    logger.info("View 'v_cleaned_transactions' created.")

    # 4. Cleaned Marketing Campaigns View
    con.execute(
        f"""
        CREATE OR REPLACE VIEW v_cleaned_marketing AS
        SELECT
            campaign_id,
            TRIM(campaign_type) AS campaign_type,
            TRY_CAST(REPLACE(REPLACE(TRIM(campaign_budget), '$', ''), ',', '') AS DOUBLE) AS campaign_budget,
            TRIM(region_target) AS region_target,
            start_date,
            end_date
        FROM read_csv_auto('{MARKETING_CSV.as_posix()}')
        """
    )
    logger.info("View 'v_cleaned_marketing' created.")

    # 5. Cleaned Geo Data View
    con.execute(
        f"""
        CREATE OR REPLACE VIEW v_cleaned_geo AS
        SELECT
            TRIM(geo_ip_region) AS geo_ip_region,
            average_income,
            urban_ratio,
            internet_penetration,
            TRIM(region_tier) AS region_tier
        FROM read_csv_auto('{GEO_DATA_CSV.as_posix()}')
        """
    )
    logger.info("View 'v_cleaned_geo' created.")


def run_clean():
    """Runs data cleaning verification."""
    ensure_directories()
    con = duckdb.connect()
    create_cleaned_views(con)
    logger.info("Data cleaning views verified successfully.")
    return con


if __name__ == "__main__":
    run_clean()
