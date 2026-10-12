"""
src/features/build_point_in_time_features.py
Point-in-Time (PIT) Feature Engineering Pipeline for Controlled Benchmark.
Computes features STRICTLY on data observable on or before t_0 (2024-06-01).
Guarantees:
- Zero data leakage from the future prediction window.
- Anti-inflation joins (cardinality 1:1 on customer_id).
- Safe mathematical division with smoothing (+ 1.0).
- Clean handling of missing values.
- Attaches the verified causal point-in-time target Y_i.
"""

import sys
import os
import json
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import OUTPUTS_DIR, RANDOM_STATE, get_logger

logger = get_logger("build_pit_features")
BENCHMARK_DIR = OUTPUTS_DIR / "controlled_benchmark"


def build_point_in_time_features(cutoff_date: str = "2024-06-01") -> str:
    """
    Builds clean, point-in-time customer feature dataset from controlled benchmark.
    All features derived strictly from events <= cutoff_date.
    """
    logger.info(f"Building Point-in-Time feature dataset with Cutoff t_0 = {cutoff_date}...")
    con = duckdb.connect()

    cust_csv = (BENCHMARK_DIR / "customers.csv").as_posix()
    sess_csv = (BENCHMARK_DIR / "sessions.csv").as_posix()
    trans_csv = (BENCHMARK_DIR / "transactions.csv").as_posix()
    geo_csv = (BENCHMARK_DIR / "geo_data.csv").as_posix()
    mkt_csv = (BENCHMARK_DIR / "marketing_campaigns.csv").as_posix()
    labels_csv = (BENCHMARK_DIR / "customer_labels_pit.csv").as_posix()

    output_parquet = BENCHMARK_DIR / "customer_features_pit.parquet"

    # 1. Pre-aggregate Sessions <= t_0
    con.execute(f"""
        CREATE OR REPLACE VIEW v_pit_sessions_agg AS
        WITH filtered_sessions AS (
            SELECT * FROM read_csv_auto('{sess_csv}')
            WHERE session_timestamp <= DATE '{cutoff_date}'
        ),
        ranked_geo AS (
            SELECT customer_id, geo_ip_region,
                   ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY COUNT(*) DESC, geo_ip_region ASC) as rn
            FROM filtered_sessions
            WHERE geo_ip_region IS NOT NULL
            GROUP BY customer_id, geo_ip_region
        ),
        dominant_geo AS (
            SELECT customer_id, geo_ip_region AS dominant_geo_ip_region FROM ranked_geo WHERE rn = 1
        ),
        ranked_camp AS (
            SELECT customer_id, campaign_id,
                   ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY COUNT(*) DESC, campaign_id ASC) as rn
            FROM filtered_sessions
            WHERE campaign_id IS NOT NULL
            GROUP BY customer_id, campaign_id
        ),
        dominant_camp AS (
            SELECT customer_id, campaign_id AS dominant_campaign_id FROM ranked_camp WHERE rn = 1
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
                COALESCE(AVG(bounce_flag), 0.0) AS bounce_rate,
                AVG(CASE WHEN traffic_source = 'organic' THEN 1.0 ELSE 0.0 END) AS pct_organic_sessions,
                AVG(CASE WHEN traffic_source = 'ads' THEN 1.0 ELSE 0.0 END) AS pct_ads_sessions,
                AVG(CASE WHEN traffic_source = 'email' THEN 1.0 ELSE 0.0 END) AS pct_email_sessions,
                AVG(CASE WHEN traffic_source = 'social' THEN 1.0 ELSE 0.0 END) AS pct_social_sessions,
                AVG(CASE WHEN device_type = 'mobile' THEN 1.0 ELSE 0.0 END) AS pct_mobile_sessions,
                AVG(CASE WHEN device_type = 'desktop' THEN 1.0 ELSE 0.0 END) AS pct_desktop_sessions,
                AVG(CASE WHEN device_type = 'tablet' THEN 1.0 ELSE 0.0 END) AS pct_tablet_sessions,
                DATE_DIFF('day', MAX(CAST(session_timestamp AS DATE)), DATE '{cutoff_date}') AS days_since_last_session
            FROM filtered_sessions
            GROUP BY customer_id
        )
        SELECT m.*, g.dominant_geo_ip_region, c.dominant_campaign_id
        FROM metrics m
        LEFT JOIN dominant_geo g ON m.customer_id = g.customer_id
        LEFT JOIN dominant_camp c ON m.customer_id = c.customer_id
    """)

    # 2. Pre-aggregate Transactions <= t_0
    con.execute(f"""
        CREATE OR REPLACE VIEW v_pit_trans_agg AS
        WITH filtered_trans AS (
            SELECT * FROM read_csv_auto('{trans_csv}')
            WHERE transaction_timestamp <= DATE '{cutoff_date}'
        )
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
            DATE_DIFF('day', MAX(CAST(transaction_timestamp AS DATE)), DATE '{cutoff_date}') AS days_since_last_transaction
        FROM filtered_trans
        GROUP BY customer_id
    """)

    # 3. Build Integrated Customer Table with Target and Derived Interaction Ratios
    con.execute(f"""
        CREATE OR REPLACE TABLE t_pit_features AS
        SELECT
            c.customer_id,
            l.target,

            -- Customer Profile & Demographics
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
            DATE_DIFF('day', CAST(c.signup_date AS DATE), DATE '{cutoff_date}') AS account_age_days,

            -- Noise attributes (for PSO robustness evaluation)
            c.noise_customer_0,
            c.noise_customer_1,
            c.noise_customer_2,
            c.noise_customer_3,
            c.noise_customer_4,

            -- Observable Session Features (<= t_0)
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
            COALESCE(s.days_since_last_session, 365) AS days_since_last_session,
            CASE WHEN s.customer_id IS NOT NULL THEN 1 ELSE 0 END AS has_sessions,

            -- Observable Transaction Features (<= t_0)
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
            COALESCE(t.days_since_last_transaction, 365) AS days_since_last_transaction,

            -- Geo Features
            COALESCE(g.average_income, 55000.0) AS average_income,
            COALESCE(g.urban_ratio, 0.5) AS urban_ratio,
            COALESCE(g.internet_penetration, 0.8) AS internet_penetration,
            COALESCE(g.region_tier, 'Tier 2') AS region_tier,

            -- Safe Behavioral Ratios & Domain Interactions
            ROUND(COALESCE(s.total_cart_additions, 0) * 1.0 / (COALESCE(s.total_pages_viewed, 0) + 1.0), 4) AS cart_to_page_ratio,
            ROUND(COALESCE(s.total_session_duration, 0.0) * 1.0 / (COALESCE(s.total_pages_viewed, 0) + 1.0), 2) AS duration_per_page,
            ROUND(COALESCE(t.total_spend, 0.0) * 1.0 / (COALESCE(s.sess_count, 0) + 1.0), 2) AS spend_per_session,
            ROUND(COALESCE(t.total_spend, 0.0) * 1.0 / (COALESCE(t.total_items_count, 0) + 1.0), 2) AS spend_per_item,
            ROUND(COALESCE(c.discount_usage_rate, 0.0) * COALESCE(t.trans_discount_rate, 0.0), 4) AS discount_interaction,
            ROUND(COALESCE(c.loyalty_score, 0.0) * (COALESCE(t.total_spend, 0.0) + 1.0), 2) AS loyalty_spend_product,
            ROUND((COALESCE(c.avg_review_score, 3.0) / 5.0) * COALESCE(c.loyalty_score, 0.0), 4) AS review_loyalty_score,
            ROUND(LEAST(COALESCE(s.days_since_last_session, 365) * 1.0 / (DATE_DIFF('day', CAST(c.signup_date AS DATE), DATE '{cutoff_date}') + 1.0), 5.0), 4) AS activity_recency_ratio,
            ROUND(LN(1.0 + COALESCE(s.total_session_duration, 0.0)) + LN(1.0 + COALESCE(s.total_cart_additions, 0)) + LN(1.0 + COALESCE(s.sess_count, 0)), 4) AS engagement_score

        FROM read_csv_auto('{cust_csv}') c
        JOIN read_csv_auto('{labels_csv}') l ON c.customer_id = l.customer_id
        LEFT JOIN v_pit_sessions_agg s ON c.customer_id = s.customer_id
        LEFT JOIN v_pit_trans_agg t ON c.customer_id = t.customer_id
        LEFT JOIN read_csv_auto('{geo_csv}') g ON s.dominant_geo_ip_region = g.geo_ip_region
        ORDER BY c.customer_id
    """)

    df = con.execute("SELECT * FROM t_pit_features").fetchdf()

    # 4. Stratified Train (80%) and Holdout (20%) split
    logger.info(f"Splitting N={len(df):,} into 80% Train, 20% Holdout (Stratified by Target)...")
    indices = np.arange(len(df))
    y = df["target"].values
    train_idx, holdout_idx = train_test_split(indices, test_size=0.20, random_state=RANDOM_STATE, stratify=y)

    df["split_type"] = "train"
    df.loc[holdout_idx, "split_type"] = "holdout"

    # Persist Parquet and Sample CSV
    con.execute(f"COPY df TO '{output_parquet.as_posix()}' (FORMAT PARQUET)")
    sample_csv = BENCHMARK_DIR / "customer_features_pit_sample.csv"
    con.execute(f"COPY (SELECT * FROM df LIMIT 5000) TO '{sample_csv.as_posix()}' (HEADER, DELIMITER ',')")

    # Save Split indices
    split_npz = BENCHMARK_DIR / "split_indices_pit.npz"
    np.savez_compressed(
        split_npz,
        train_idx=train_idx,
        holdout_idx=holdout_idx,
    )

    logger.info(f"Point-in-Time Feature engineering complete: {len(df):,} customers, {df.shape[1]} columns.")
    logger.info(f"Train samples: {len(train_idx):,} (Positive: {y[train_idx].mean():.2%}), Holdout: {len(holdout_idx):,} (Positive: {y[holdout_idx].mean():.2%}).")
    con.close()
    return str(output_parquet)


if __name__ == "__main__":
    build_point_in_time_features()
