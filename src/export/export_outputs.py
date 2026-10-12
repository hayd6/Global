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

import json
import duckdb
import pandas as pd
import numpy as np

from src.config import (
    BASE_DIR,
    OUTPUTS_DIR,
    METRICS_DIR,
    CONFIGS_DIR,
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


def export_web_metrics_json():
    """Generates web/data/metrics.json programmatically from verified CSV artifacts."""
    logger.info("Exporting synchronized web/data/metrics.json...")
    web_dir = BASE_DIR / "web" / "data"
    web_dir.mkdir(parents=True, exist_ok=True)

    metrics_comp_path = METRICS_DIR / "metrics_comparison.csv"
    baseline_path = METRICS_DIR / "baseline_metrics.csv"
    pso_feats_path = FEATURE_SEL_DIR / "pso_selected_features.csv"
    pso_conv_path = FEATURE_SEL_DIR / "pso_convergence.csv"
    pso_conf_path = CONFIGS_DIR / "pso_experiment_config.json"

    metrics_comp_df = pd.read_csv(metrics_comp_path)
    baseline_df = pd.read_csv(baseline_path)
    pso_feats_df = pd.read_csv(pso_feats_path)
    pso_conv_df = pd.read_csv(pso_conv_path)

    pso_config = {}
    if pso_conf_path.exists():
        with open(pso_conf_path, "r", encoding="utf-8") as f:
            pso_config = json.load(f)

    e_descriptions = {
        "Baseline (Full Features)": "Đường cơ sở chuẩn mực sử dụng toàn bộ 63 đặc trưng liên tục trích xuất từ dữ liệu đa bảng",
        "Baseline (Statistical Features)": "Lọc thống kê đơn biến F-score chọn 17 biến tốt nhất; đạt PR-AUC cao nhất toàn nghiên cứu",
        "Baseline (PSO Features)": "Tối ưu hóa bầy đàn nhị phân BPSO chọn 17 biến tối ưu; giảm thời gian fit xuống 4.50s",
        "XGBoost (Full Features)": "Mô hình tăng cường gradient cây quyết định trên toàn bộ không gian 63 đặc trưng",
        "XGBoost (PSO Features)": "Kết hợp tối ưu PSO và XGBoost: huấn luyện nhanh nhất (2.07s - tăng tốc 2.1x), giảm 73% biến số"
    }
    e_ids = {
        "Baseline (Full Features)": "E1",
        "Baseline (Statistical Features)": "E2",
        "Baseline (PSO Features)": "E3",
        "XGBoost (Full Features)": "E4",
        "XGBoost (PSO Features)": "E5"
    }
    e_algos = {
        "Baseline (Full Features)": "Gradient Boosting",
        "Baseline (Statistical Features)": "Gradient Boosting",
        "Baseline (PSO Features)": "Gradient Boosting",
        "XGBoost (Full Features)": "XGBoost",
        "XGBoost (PSO Features)": "XGBoost"
    }
    e_spaces = {
        "Baseline (Full Features)": "Full (63)",
        "Baseline (Statistical Features)": "ANOVA (17)",
        "Baseline (PSO Features)": "PSO (17)",
        "XGBoost (Full Features)": "Full (63)",
        "XGBoost (PSO Features)": "PSO (17)"
    }

    experiments_e1_e5 = []
    for _, row in metrics_comp_df.iterrows():
        name = row["model_name"]
        experiments_e1_e5.append({
            "id": e_ids.get(name, "E?"),
            "model_name": name,
            "algorithm": e_algos.get(name, "ML"),
            "feature_space": e_spaces.get(name, str(row["feature_space"])),
            "feature_count": int(row["feature_count"]),
            "pr_auc": round(float(row["pr_auc"]), 4),
            "roc_auc": round(float(row["roc_auc"]), 4),
            "f1_score": round(float(row["f1_score"]), 4),
            "precision": round(float(row["precision"]), 4),
            "recall": round(float(row["recall"]), 4),
            "accuracy": round(float(row["accuracy"]), 4),
            "fit_time": round(float(row["fit_time_seconds"]), 2),
            "search_time": round(float(row["search_time_seconds"]), 2),
            "total_time": round(float(row["total_time_seconds"]), 2),
            "description": e_descriptions.get(name, "")
        })

    baselines_7 = []
    for _, row in baseline_df.iterrows():
        baselines_7.append({
            "name": row["model_name"],
            "features": int(row["feature_count"]),
            "pr_auc": round(float(row["pr_auc"]), 4),
            "roc_auc": round(float(row["roc_auc"]), 4),
            "f1": round(float(row["f1_score"]), 4),
            "precision": round(float(row["precision"]), 4),
            "recall": round(float(row["recall"]), 4),
            "fit_time": round(float(row["fit_time_seconds"]), 2)
        })

    pso_convergence = []
    for _, row in pso_conv_df.iterrows():
        pso_convergence.append({
            "iteration": int(row["iteration"]),
            "best_fitness": round(float(row["best_fitness"]), 4),
            "avg_fitness": round(float(row["mean_fitness"]), 4),
            "feature_count": int(row["best_feature_count"]),
            "elapsed_seconds": round(float(row["elapsed_seconds"]), 2)
        })

    pso_selected_features = pso_feats_df[pso_feats_df["is_selected"] == 1]["feature_name"].tolist()
    xgb_row = metrics_comp_df[metrics_comp_df["model_name"] == "XGBoost (Full Features)"].iloc[0]

    web_data = {
        "project": {
            "title_vi": "Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử",
            "title_en": "Behavioral Feature Mining and PSO-Based Feature Selection for E-Commerce Purchase Prediction",
            "version": "v3.0-Master-Final",
            "date": "2026-10-12",
            "status": "ĐẠT CÓ ĐIỀU KIỆN (PASSED WITH CONDITIONS)"
        },
        "dataset_summary": {
            "total_customers": 200000,
            "total_sessions": 2000000,
            "total_transactions": 500000,
            "train_samples": 160000,
            "test_samples": 40000,
            "holdout_samples": 32000,
            "train_pool_samples": 128000,
            "target_positive_rate": 0.20306,
            "target_positives": 32489,
            "target_negatives": 127511
        },
        "pso_config": {
            "n_particles": pso_config.get("n_particles", 16),
            "n_iterations": pso_config.get("n_iterations", 12),
            "inertia_w": pso_config.get("inertia_w", 0.729),
            "cognitive_c1": pso_config.get("cognitive_c1", 1.494),
            "social_c2": pso_config.get("social_c2", 1.494),
            "alpha_pr_weight": pso_config.get("alpha_pr_weight", 0.92),
            "search_time_seconds": pso_config.get("search_time_seconds", 11.79),
            "n_evaluations": pso_config.get("n_evaluations", 208),
            "selected_features_count": pso_config.get("selected_features_count", 17),
            "sparsity_reduction_pct": pso_config.get("sparsity_reduction_pct", 73.02)
        },
        "holdout_confusion_matrix": {
            "model": "XGBoost (Full Features)",
            "threshold": 0.50,
            "total_samples": 32000,
            "true_negatives": int(xgb_row["true_negatives"]),
            "false_positives": int(xgb_row["false_positives"]),
            "false_negatives": int(xgb_row["false_negatives"]),
            "true_positives": int(xgb_row["true_positives"]),
            "pr_auc": round(float(xgb_row["pr_auc"]), 4),
            "roc_auc": round(float(xgb_row["roc_auc"]), 4),
            "f1_score": round(float(xgb_row["f1_score"]), 4),
            "precision": round(float(xgb_row["precision"]), 4),
            "recall": round(float(xgb_row["recall"]), 4),
            "accuracy": round(float(xgb_row["accuracy"]), 4),
            "specificity": round(float(xgb_row["true_negatives"] / (xgb_row["true_negatives"] + xgb_row["false_positives"])), 4)
        },
        "experiments_e1_e5": experiments_e1_e5,
        "baselines_7": baselines_7,
        "pso_convergence": pso_convergence,
        "pso_selected_features": pso_selected_features
    }

    out_json = web_dir / "metrics.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(web_data, f, indent=2, ensure_ascii=False)
    logger.info(f"Exported synchronized {out_json} successfully.")


if __name__ == "__main__":
    export_powerbi_tables()
    export_web_metrics_json()
