"""
Phase 4: Feature Engineering Module.
Computes advanced behavioural ratios, RFM indices, and interaction terms.
Generates comprehensive feature dictionary and persists finalized dataset.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
import pandas as pd
import numpy as np
from src.config import (
    PROCESSED_DATA_DIR,
    OUTPUTS_DIR,
    ensure_directories,
    get_logger,
)
from src.data.integrate_data import run_integration

logger = get_logger("build_features")


def engineer_advanced_features(con: duckdb.DuckDBPyConnection, input_parquet: Path) -> str:
    """Computes advanced behavioural metrics and derived domain interactions."""
    logger.info("Computing derived behavioral features and interaction indices...")

    output_final_parquet = OUTPUTS_DIR / "customer_features.parquet"
    output_final_csv = OUTPUTS_DIR / "customer_features.csv"

    con.execute(
        f"""
        CREATE OR REPLACE TABLE t_customer_features AS
        SELECT
            *,
            -- Behavioral ratios
            ROUND(total_cart_additions * 1.0 / (total_pages_viewed + 1.0), 4) AS cart_to_page_ratio,
            ROUND(total_session_duration * 1.0 / (total_pages_viewed + 1.0), 2) AS duration_per_page,
            ROUND(total_spend * 1.0 / (sess_count + 1.0), 2) AS spend_per_session,
            ROUND(total_spend * 1.0 / (total_items_count + 1.0), 2) AS spend_per_item,
            
            -- Interaction indices
            ROUND(COALESCE(discount_usage_rate, 0.0) * trans_discount_rate, 4) AS discount_interaction,
            ROUND(COALESCE(loyalty_score, 0.0) * (total_spend + 1.0), 2) AS loyalty_spend_product,
            ROUND((COALESCE(avg_review_score, 3.0) / 5.0) * COALESCE(loyalty_score, 0.0), 4) AS review_loyalty_score,
            ROUND(days_since_last_session * 1.0 / (account_age_days + 1.0), 4) AS activity_recency_ratio,
            
            -- Engagement composite index
            ROUND(LN(1.0 + total_session_duration) + LN(1.0 + total_cart_additions) + LN(1.0 + sess_count), 4) AS engagement_score

        FROM read_parquet('{input_parquet.as_posix()}')
        """
    )

    # Persist full parquet
    logger.info(f"Saving final customer features to {output_final_parquet}...")
    con.execute(f"COPY t_customer_features TO '{output_final_parquet.as_posix()}' (FORMAT PARQUET)")

    # Also export customer_features.csv (first 20,000 sample for easy viewing, or full CSV if desired)
    # Full CSV is ~200k rows x 72 cols (~90MB), perfectly manageable!
    logger.info(f"Exporting customer_features.csv to {output_final_csv}...")
    con.execute(f"COPY t_customer_features TO '{output_final_csv.as_posix()}' (HEADER, DELIMITER ',')")

    return str(output_final_parquet)


def generate_feature_dictionary():
    """Generates the comprehensive feature dictionary with temporal cutoff and leakage metadata."""
    logger.info("Generating feature dictionary metadata...")

    feature_meta = [
        # Demographics & Account
        {"feature_name": "age", "formula": "Cleaned customer age", "source": "customers.csv", "data_type": "INTEGER", "business_meaning": "Customer chronological age", "imputation_rule": "Median by customer_tier", "leakage_risk": "NONE", "temporal_nature": "Static demographic attribute", "cutoff_rule": "Snapshot profile at dataset export"},
        {"feature_name": "country_code", "formula": "Cleaned ISO country code", "source": "customers.csv", "data_type": "VARCHAR", "business_meaning": "Country of residency", "imputation_rule": "Mode ('US')", "leakage_risk": "NONE", "temporal_nature": "Static demographic attribute", "cutoff_rule": "Snapshot profile at dataset export"},
        {"feature_name": "region", "formula": "Cleaned domestic region", "source": "customers.csv", "data_type": "VARCHAR", "business_meaning": "Domestic operational territory", "imputation_rule": "Mode", "leakage_risk": "NONE", "temporal_nature": "Static demographic attribute", "cutoff_rule": "Snapshot profile at dataset export"},
        {"feature_name": "customer_tier", "formula": "Categorical tier (Bronze/Silver/Gold/Platinum)", "source": "customers.csv", "data_type": "VARCHAR", "business_meaning": "Customer lifetime loyalty status", "imputation_rule": "Mode ('Bronze')", "leakage_risk": "NONE", "temporal_nature": "Static tier at export", "cutoff_rule": "Snapshot profile at dataset export"},
        {"feature_name": "credit_limit", "formula": "Normalized credit allowance ($ removed)", "source": "customers.csv", "data_type": "DOUBLE", "business_meaning": "Customer pre-approved purchasing credit limit", "imputation_rule": "Median", "leakage_risk": "NONE", "temporal_nature": "Static account allowance", "cutoff_rule": "Snapshot profile at dataset export"},
        {"feature_name": "loyalty_score", "formula": "Normalized score [0, 1]", "source": "customers.csv", "data_type": "DOUBLE", "business_meaning": "Platform loyalty and retention propensity", "imputation_rule": "Mean", "leakage_risk": "NONE", "temporal_nature": "Static score", "cutoff_rule": "Snapshot profile at dataset export"},
        {"feature_name": "email_open_rate", "formula": "Ratio of opened marketing emails", "source": "customers.csv", "data_type": "DOUBLE", "business_meaning": "Responsiveness to promotional email outreach", "imputation_rule": "Median (0.33)", "leakage_risk": "NONE", "temporal_nature": "Historical aggregate", "cutoff_rule": "Aggregated up to dataset export"},
        {"feature_name": "discount_usage_rate", "formula": "Historical coupon redemption frequency", "source": "customers.csv", "data_type": "DOUBLE", "business_meaning": "Sensitivity to discounts and deals", "imputation_rule": "Mean", "leakage_risk": "NONE", "temporal_nature": "Historical aggregate", "cutoff_rule": "Aggregated up to dataset export"},
        {"feature_name": "avg_review_score", "formula": "Average product review rating [1.0, 5.0]", "source": "customers.csv", "data_type": "DOUBLE", "business_meaning": "Customer post-purchase satisfaction index", "imputation_rule": "Mean (4.0)", "leakage_risk": "NONE", "temporal_nature": "Historical aggregate", "cutoff_rule": "Aggregated up to dataset export"},
        {"feature_name": "has_referral_code", "formula": "referral_code IS NOT NULL", "source": "customers.csv", "data_type": "TINYINT", "business_meaning": "Whether customer was acquired via peer referral", "imputation_rule": "0", "leakage_risk": "NONE", "temporal_nature": "Static signup attribute", "cutoff_rule": "Recorded at signup"},
        {"feature_name": "account_age_days", "formula": "2024-09-26 - signup_date", "source": "customers.csv", "data_type": "INTEGER", "business_meaning": "Customer tenure on platform in days", "imputation_rule": "Median", "leakage_risk": "NONE", "temporal_nature": "Elapsed days to max date", "cutoff_rule": "Relative to 2024-09-26"},

        # Synthetic Noise (Tracked for PSO)
        {"feature_name": "noise_customer_0", "formula": "Gaussian noise feature 0", "source": "customers.csv", "data_type": "DOUBLE", "business_meaning": "Artificial noise variable for benchmark testing", "imputation_rule": "None", "leakage_risk": "NONE", "temporal_nature": "Synthetic noise", "cutoff_rule": "Injected at generation"},
        {"feature_name": "noise_customer_1", "formula": "Gaussian noise feature 1", "source": "customers.csv", "data_type": "DOUBLE", "business_meaning": "Artificial noise variable for benchmark testing", "imputation_rule": "None", "leakage_risk": "NONE", "temporal_nature": "Synthetic noise", "cutoff_rule": "Injected at generation"},
        {"feature_name": "noise_customer_2", "formula": "Gaussian noise feature 2", "source": "customers.csv", "data_type": "DOUBLE", "business_meaning": "Artificial noise variable for benchmark testing", "imputation_rule": "None", "leakage_risk": "NONE", "temporal_nature": "Synthetic noise", "cutoff_rule": "Injected at generation"},
        {"feature_name": "noise_customer_3", "formula": "Gaussian noise feature 3", "source": "customers.csv", "data_type": "DOUBLE", "business_meaning": "Artificial noise variable for benchmark testing", "imputation_rule": "None", "leakage_risk": "NONE", "temporal_nature": "Synthetic noise", "cutoff_rule": "Injected at generation"},
        {"feature_name": "noise_customer_4", "formula": "Gaussian noise feature 4", "source": "customers.csv", "data_type": "DOUBLE", "business_meaning": "Artificial noise variable for benchmark testing", "imputation_rule": "None", "leakage_risk": "NONE", "temporal_nature": "Synthetic noise", "cutoff_rule": "Injected at generation"},
        {"feature_name": "avg_noise_trans_0", "formula": "Mean transaction noise 0", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Aggregated artificial transaction noise", "imputation_rule": "0", "leakage_risk": "NONE", "temporal_nature": "Synthetic noise", "cutoff_rule": "Injected at generation"},
        {"feature_name": "avg_noise_trans_1", "formula": "Mean transaction noise 1", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Aggregated artificial transaction noise", "imputation_rule": "0", "leakage_risk": "NONE", "temporal_nature": "Synthetic noise", "cutoff_rule": "Injected at generation"},

        # Sessions Behavioral
        {"feature_name": "sess_count", "formula": "COUNT(sessions)", "source": "sessions.csv", "data_type": "BIGINT", "business_meaning": "Total browsing sessions on the platform", "imputation_rule": "0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "total_session_duration", "formula": "SUM(session_duration)", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Total seconds spent browsing", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "avg_session_duration", "formula": "AVG(session_duration)", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Average session length in seconds", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "max_session_duration", "formula": "MAX(session_duration)", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Peak single browsing session length", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "total_pages_viewed", "formula": "SUM(pages_viewed)", "source": "sessions.csv", "data_type": "BIGINT", "business_meaning": "Total product / catalog pages viewed", "imputation_rule": "0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "avg_pages_viewed", "formula": "AVG(pages_viewed)", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Average depth of catalog browsing per session", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "total_cart_additions", "formula": "SUM(cart_additions)", "source": "sessions.csv", "data_type": "BIGINT", "business_meaning": "Cumulative items added to shopping cart", "imputation_rule": "0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "avg_cart_additions", "formula": "AVG(cart_additions)", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Average items added to cart per session", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "bounce_rate", "formula": "AVG(is_bounce)", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Proportion of single-page or immediate bounce sessions", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_organic_sessions", "formula": "AVG(traffic_source = 'organic')", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Share of visits initiated through organic search", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Session ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_ads_sessions", "formula": "AVG(traffic_source = 'ads')", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Share of visits initiated through paid search/ads", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Session ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_email_sessions", "formula": "AVG(traffic_source = 'email')", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Share of visits initiated through email marketing", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Session ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_social_sessions", "formula": "AVG(traffic_source = 'social')", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Share of visits initiated through social media", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Session ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_mobile_sessions", "formula": "AVG(device_type = 'mobile')", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Share of mobile device sessions", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Session ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_desktop_sessions", "formula": "AVG(device_type = 'desktop')", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Share of desktop device sessions", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Session ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_tablet_sessions", "formula": "AVG(device_type = 'tablet')", "source": "sessions.csv", "data_type": "DOUBLE", "business_meaning": "Share of tablet device sessions", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Session ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "days_since_last_session", "formula": "2024-09-26 - MAX(session_timestamp)", "source": "sessions.csv", "data_type": "INTEGER", "business_meaning": "Recency of last recorded session in days", "imputation_rule": "9999", "leakage_risk": "NONE", "temporal_nature": "Recency to 2024-09-26", "cutoff_rule": "Relative to 2024-09-26"},

        # Transactions Behavioral
        {"feature_name": "has_transactions", "formula": "1 if trans_count > 0 else 0", "source": "transactions.csv", "data_type": "TINYINT", "business_meaning": "Binary indicator whether customer ever purchased", "imputation_rule": "0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "trans_count", "formula": "COUNT(transactions)", "source": "transactions.csv", "data_type": "BIGINT", "business_meaning": "Historical order frequency", "imputation_rule": "0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "total_spend", "formula": "SUM(order_value)", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Cumulative historical expenditure ($)", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "avg_order_value", "formula": "AVG(order_value)", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Average ticket price per order ($)", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "max_order_value", "formula": "MAX(order_value)", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Peak monetary value of any single transaction", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "min_order_value", "formula": "MIN(order_value)", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Minimum monetary value of any single transaction", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "total_items_count", "formula": "SUM(items_count)", "source": "transactions.csv", "data_type": "BIGINT", "business_meaning": "Total physical items purchased across orders", "imputation_rule": "0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "avg_items_per_order", "formula": "AVG(items_count)", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Basket volume per transaction", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "trans_discount_rate", "formula": "AVG(discount_applied)", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Proportion of historical orders utilizing discounts", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "high_value_trans_count", "formula": "SUM(high_value_flag)", "source": "transactions.csv", "data_type": "BIGINT", "business_meaning": "Count of orders classified as high value", "imputation_rule": "0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "high_value_trans_ratio", "formula": "AVG(high_value_flag)", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Ratio of high value orders to total orders", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Aggregated over observed window", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_credit_card", "formula": "AVG(payment_method = 'credit_card')", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Preference for credit card payments", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Transaction ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_debit_card", "formula": "AVG(payment_method = 'debit_card')", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Preference for debit card payments", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Transaction ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_paypal", "formula": "AVG(payment_method = 'paypal')", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Preference for PayPal checkout", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Transaction ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_crypto", "formula": "AVG(payment_method = 'crypto')", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Preference for cryptocurrency checkout", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Transaction ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_standard_shipping", "formula": "AVG(shipping_speed = 'standard')", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Preference for standard delivery", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Transaction ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_express_shipping", "formula": "AVG(shipping_speed = 'express')", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Preference for express delivery", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Transaction ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "pct_overnight_shipping", "formula": "AVG(shipping_speed = 'overnight')", "source": "transactions.csv", "data_type": "DOUBLE", "business_meaning": "Preference for overnight courier service", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Transaction ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "days_since_last_transaction", "formula": "2024-09-26 - MAX(transaction_timestamp)", "source": "transactions.csv", "data_type": "INTEGER", "business_meaning": "Days elapsed since customer last bought", "imputation_rule": "9999", "leakage_risk": "NONE", "temporal_nature": "Recency to 2024-09-26", "cutoff_rule": "Relative to 2024-09-26"},

        # Derived Ratios & Indices
        {"feature_name": "cart_to_page_ratio", "formula": "cart_additions / (pages_viewed + 1)", "source": "Engineered", "data_type": "DOUBLE", "business_meaning": "Intent-to-buy density per page view", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Engineered ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "duration_per_page", "formula": "session_duration / (pages_viewed + 1)", "source": "Engineered", "data_type": "DOUBLE", "business_meaning": "Attention immersion depth per catalog page", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Engineered ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "spend_per_session", "formula": "total_spend / (sess_count + 1)", "source": "Engineered", "data_type": "DOUBLE", "business_meaning": "Revenue monetization efficiency per visit", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Engineered ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "spend_per_item", "formula": "total_spend / (total_items_count + 1)", "source": "Engineered", "data_type": "DOUBLE", "business_meaning": "Unit price affinity / basket value tier", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Engineered ratio", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "discount_interaction", "formula": "discount_usage_rate * trans_discount_rate", "source": "Engineered", "data_type": "DOUBLE", "business_meaning": "Cross-validated price-sensitivity propensity", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Engineered interaction", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "loyalty_spend_product", "formula": "loyalty_score * (total_spend + 1)", "source": "Engineered", "data_type": "DOUBLE", "business_meaning": "High-value loyalist composite weight", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Engineered interaction", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "review_loyalty_score", "formula": "(avg_review / 5.0) * loyalty_score", "source": "Engineered", "data_type": "DOUBLE", "business_meaning": "Sentiment-weighted brand loyalty score", "imputation_rule": "0.0", "leakage_risk": "NONE", "temporal_nature": "Engineered interaction", "cutoff_rule": "Up to 2024-09-26"},
        {"feature_name": "activity_recency_ratio", "formula": "days_since_last_sess / account_age_days", "source": "Engineered", "data_type": "DOUBLE", "business_meaning": "Relative platform dormancy coefficient", "imputation_rule": "1.0", "leakage_risk": "NONE", "temporal_nature": "Engineered ratio", "cutoff_rule": "Relative to 2024-09-26"},
        {"feature_name": "engagement_score", "formula": "ln(dur) + ln(cart) + ln(sess)", "source": "Engineered", "data_type": "DOUBLE", "business_meaning": "Non-linear aggregate customer engagement index", "imputation_rule": "0.0", "leakage_risk": "POTENTIAL_SNAPSHOT_OVERLAP (Full history)", "temporal_nature": "Engineered index", "cutoff_rule": "Up to 2024-09-26"},

        # Regional & Geo
        {"feature_name": "average_income", "formula": "Geo IP regional average income", "source": "geo_data.csv", "data_type": "DOUBLE", "business_meaning": "Regional purchasing power index", "imputation_rule": "Median", "leakage_risk": "NONE", "temporal_nature": "Macro-economic static", "cutoff_rule": "External reference"},
        {"feature_name": "urban_ratio", "formula": "Geo IP regional urban population share", "source": "geo_data.csv", "data_type": "DOUBLE", "business_meaning": "Urbanization index of customer locale", "imputation_rule": "Median", "leakage_risk": "NONE", "temporal_nature": "Macro-economic static", "cutoff_rule": "External reference"},
        {"feature_name": "internet_penetration", "formula": "Geo IP internet adoption rate", "source": "geo_data.csv", "data_type": "DOUBLE", "business_meaning": "Digital literacy and internet readiness", "imputation_rule": "Median", "leakage_risk": "NONE", "temporal_nature": "Macro-economic static", "cutoff_rule": "External reference"},
        {"feature_name": "region_tier", "formula": "Geo region development tier", "source": "geo_data.csv", "data_type": "VARCHAR", "business_meaning": "Macro-economic regional tier (Tier 1/2/3)", "imputation_rule": "Mode", "leakage_risk": "NONE", "temporal_nature": "Macro-economic static", "cutoff_rule": "External reference"},
    ]

    df_dict = pd.DataFrame(feature_meta)
    dict_csv_path = OUTPUTS_DIR / "feature_dictionary.csv"
    df_dict.to_csv(dict_csv_path, index=False)
    logger.info(f"Saved feature dictionary with {len(df_dict)} features to {dict_csv_path}")
    return df_dict


def run_feature_engineering():
    """Runs Phase 4 feature engineering pipeline."""
    ensure_directories()
    con = duckdb.connect()
    parquet_in = PROCESSED_DATA_DIR / "clean_customer_features.parquet"
    if not parquet_in.exists():
        parquet_in = Path(run_integration())

    output_parquet = engineer_advanced_features(con, parquet_in)
    generate_feature_dictionary()
    return output_parquet


if __name__ == "__main__":
    run_feature_engineering()
