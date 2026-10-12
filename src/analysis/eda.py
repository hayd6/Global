"""
Phase 4: Exploratory Data Analysis (EDA) Module.
Generates 9 high-quality, interpretable analytical charts and exports
the statistical summary table for research and dashboard consumption.
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
import matplotlib.pyplot as plt

from src.config import (
    OUTPUTS_DIR,
    EDA_DIR,
    ensure_directories,
    get_logger,
)

logger = get_logger("eda")


def run_eda():
    """Generates analytical visualizations and export summaries."""
    ensure_directories()
    con = duckdb.connect()
    parquet_path = OUTPUTS_DIR / "customer_features.parquet"

    logger.info("Starting exploratory data analysis (EDA)...")
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # Load train subset for EDA (target is present)
    train_df = con.execute(
        f"""
        SELECT * 
        FROM read_parquet('{parquet_path.as_posix()}')
        WHERE split_type = 'train'
        """
    ).df()

    logger.info(f"Loaded {len(train_df):,} training records for EDA analysis.")

    # -------------------------------------------------------------
    # 1. Target Rate by Customer Tier
    # -------------------------------------------------------------
    tier_stats = train_df.groupby("customer_tier")["target"].agg(["count", "mean"]).reset_index()
    tier_stats["pct"] = tier_stats["mean"] * 100
    tier_order = ["Bronze", "Silver", "Gold", "Platinum"]
    tier_stats["sort_idx"] = tier_stats["customer_tier"].map({t: i for i, t in enumerate(tier_order)})
    tier_stats = tier_stats.sort_values("sort_idx").dropna(subset=["sort_idx"])

    plt.figure(figsize=(8, 5))
    bars = plt.bar(tier_stats["customer_tier"], tier_stats["pct"], color=["#CD7F32", "#C0C0C0", "#FFD700", "#E5E4E2"], edgecolor="black", width=0.55)
    plt.title("Purchase Conversion Rate by Customer Tier", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Customer Loyalty Tier", fontsize=11)
    plt.ylabel("Conversion Rate (%)", fontsize=11)
    plt.ylim(0, 30)
    for bar, count in zip(bars, tier_stats["count"]):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f"{yval:.2f}%\n(N={count:,})", ha="center", va="bottom", fontsize=9, fontweight="bold")
    plt.tight_layout()
    plt.savefig(EDA_DIR / "eda_1_target_rate_by_tier.png", dpi=200)
    plt.close()
    logger.info("Saved eda_1_target_rate_by_tier.png")

    # -------------------------------------------------------------
    # 2. Loyalty Score Distribution by Target
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    buyers_loyalty = train_df[train_df["target"] == 1]["loyalty_score"].dropna()
    non_buyers_loyalty = train_df[train_df["target"] == 0]["loyalty_score"].dropna()

    plt.hist(non_buyers_loyalty, bins=40, density=True, alpha=0.55, color="#4C72B0", label="Non-Purchasers (Target=0)")
    plt.hist(buyers_loyalty, bins=40, density=True, alpha=0.55, color="#DD8452", label="Purchasers (Target=1)")
    plt.axvline(non_buyers_loyalty.mean(), color="#1f4277", linestyle="--", linewidth=1.8, label=f"Mean Non-Purchaser: {non_buyers_loyalty.mean():.3f}")
    plt.axvline(buyers_loyalty.mean(), color="#a34f1f", linestyle="--", linewidth=1.8, label=f"Mean Purchaser: {buyers_loyalty.mean():.3f}")

    plt.title("Loyalty Score Probability Density by Target", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Customer Loyalty Score [0, 1]", fontsize=11)
    plt.ylabel("Probability Density", fontsize=11)
    plt.legend(frameon=True, facecolor="white", loc="upper right")
    plt.tight_layout()
    plt.savefig(EDA_DIR / "eda_2_loyalty_score_distribution.png", dpi=200)
    plt.close()
    logger.info("Saved eda_2_loyalty_score_distribution.png")

    # -------------------------------------------------------------
    # 3. Cart Additions vs Pages Viewed by Target
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    sample_df = train_df.sample(n=min(5000, len(train_df)), random_state=42)
    plt.scatter(
        sample_df[sample_df["target"] == 0]["total_pages_viewed"],
        sample_df[sample_df["target"] == 0]["total_cart_additions"],
        alpha=0.35, color="#4C72B0", label="Non-Purchaser", s=25
    )
    plt.scatter(
        sample_df[sample_df["target"] == 1]["total_pages_viewed"],
        sample_df[sample_df["target"] == 1]["total_cart_additions"],
        alpha=0.55, color="#DD8452", label="Purchaser", s=30, marker="^"
    )
    plt.title("Shopping Intent: Cart Additions vs Pages Viewed (5,000 Sample)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Total Catalog Pages Viewed", fontsize=11)
    plt.ylabel("Total Cart Additions", fontsize=11)
    plt.legend(frameon=True, facecolor="white")
    plt.tight_layout()
    plt.savefig(EDA_DIR / "eda_3_cart_additions_vs_pages_viewed.png", dpi=200)
    plt.close()
    logger.info("Saved eda_3_cart_additions_vs_pages_viewed.png")

    # -------------------------------------------------------------
    # 4. Session Duration Density Curves
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    buyers_dur = train_df[train_df["target"] == 1]["avg_session_duration"].dropna()
    non_buyers_dur = train_df[train_df["target"] == 0]["avg_session_duration"].dropna()

    plt.hist(non_buyers_dur, bins=45, density=True, alpha=0.5, color="#55A868", label=f"Target=0 (Mean: {non_buyers_dur.mean():.1f}s)")
    plt.hist(buyers_dur, bins=45, density=True, alpha=0.5, color="#C44E52", label=f"Target=1 (Mean: {buyers_dur.mean():.1f}s)")
    plt.title("Average Session Duration Distribution by Purchase Intent", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Average Session Duration (seconds)", fontsize=11)
    plt.ylabel("Density", fontsize=11)
    plt.legend(frameon=True, facecolor="white")
    plt.tight_layout()
    plt.savefig(EDA_DIR / "eda_4_session_duration_kde.png", dpi=200)
    plt.close()
    logger.info("Saved eda_4_session_duration_kde.png")

    # -------------------------------------------------------------
    # 5. Total Monetary Spend by Target
    # -------------------------------------------------------------
    plt.figure(figsize=(7, 5))
    spend_data = [
        train_df[train_df["target"] == 0]["total_spend"].values,
        train_df[train_df["target"] == 1]["total_spend"].values
    ]
    box = plt.boxplot(spend_data, tick_labels=["Target=0 (No Purchase)", "Target=1 (Purchase)"], patch_artist=True, showfliers=False)
    colors = ["#4C72B0", "#DD8452"]
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    plt.title("Total Spend Distribution Across Purchase Targets (Excl. Outliers)", fontsize=13, fontweight="bold", pad=12)
    plt.ylabel("Historical Total Spend (USD $)", fontsize=11)
    plt.tight_layout()
    plt.savefig(EDA_DIR / "eda_5_total_spend_distribution.png", dpi=200)
    plt.close()
    logger.info("Saved eda_5_total_spend_distribution.png")

    # -------------------------------------------------------------
    # 6. Channel & Device Conversion Multi-Panel
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    device_cols = ["pct_mobile_sessions", "pct_desktop_sessions", "pct_tablet_sessions"]
    device_names = ["Mobile", "Desktop", "Tablet"]
    dev_means_0 = [train_df[train_df["target"] == 0][c].mean() * 100 for c in device_cols]
    dev_means_1 = [train_df[train_df["target"] == 1][c].mean() * 100 for c in device_cols]

    x = np.arange(len(device_names))
    width = 0.35
    ax1.bar(x - width/2, dev_means_0, width, label="Target=0", color="#4C72B0", alpha=0.85)
    ax1.bar(x + width/2, dev_means_1, width, label="Target=1", color="#DD8452", alpha=0.85)
    ax1.set_title("Device Traffic Share by Target", fontsize=12, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(device_names)
    ax1.set_ylabel("Average Session Share (%)")
    ax1.legend(frameon=True, facecolor="white")

    traffic_cols = ["pct_organic_sessions", "pct_ads_sessions", "pct_email_sessions", "pct_social_sessions"]
    traffic_names = ["Organic", "Paid Ads", "Email", "Social"]
    tr_means_0 = [train_df[train_df["target"] == 0][c].mean() * 100 for c in traffic_cols]
    tr_means_1 = [train_df[train_df["target"] == 1][c].mean() * 100 for c in traffic_cols]

    x2 = np.arange(len(traffic_names))
    ax2.bar(x2 - width/2, tr_means_0, width, label="Target=0", color="#4C72B0", alpha=0.85)
    ax2.bar(x2 + width/2, tr_means_1, width, label="Target=1", color="#DD8452", alpha=0.85)
    ax2.set_title("Traffic Acquisition Channel Share by Target", fontsize=12, fontweight="bold")
    ax2.set_xticks(x2)
    ax2.set_xticklabels(traffic_names)
    ax2.set_ylabel("Average Session Share (%)")
    ax2.legend(frameon=True, facecolor="white")

    plt.tight_layout()
    plt.savefig(EDA_DIR / "eda_6_channel_device_conversion.png", dpi=200)
    plt.close()
    logger.info("Saved eda_6_channel_device_conversion.png")

    # -------------------------------------------------------------
    # 7. Feature Correlation Heatmap with Target
    # -------------------------------------------------------------
    corr_features = [
        "target", "loyalty_score", "discount_usage_rate", "avg_review_score",
        "credit_limit", "avg_session_duration", "total_cart_additions",
        "total_spend", "bounce_rate", "cart_to_page_ratio", "engagement_score",
        "trans_discount_rate", "noise_customer_0"
    ]
    corr_df = train_df[corr_features].dropna().corr()

    plt.figure(figsize=(10, 8))
    im = plt.imshow(corr_df, cmap="coolwarm", vmin=-0.3, vmax=0.3)
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Pearson Correlation")
    plt.xticks(np.arange(len(corr_features)), corr_features, rotation=45, ha="right", fontsize=9)
    plt.yticks(np.arange(len(corr_features)), corr_features, fontsize=9)
    plt.title("Correlation Matrix of Key Behavioral Features & Target", fontsize=13, fontweight="bold", pad=12)

    for i in range(len(corr_features)):
        for j in range(len(corr_features)):
            val = corr_df.iloc[i, j]
            text_color = "white" if abs(val) > 0.2 else "black"
            plt.text(j, i, f"{val:.2f}", ha="center", va="center", color=text_color, fontsize=8)

    plt.tight_layout()
    plt.savefig(EDA_DIR / "eda_7_feature_correlation_heatmap.png", dpi=200)
    plt.close()
    logger.info("Saved eda_7_feature_correlation_heatmap.png")

    # -------------------------------------------------------------
    # 8. Recency & Frequency (RFM Behavioral Pattern)
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    plt.scatter(
        sample_df[sample_df["target"] == 0]["days_since_last_session"],
        sample_df[sample_df["target"] == 0]["sess_count"],
        alpha=0.3, color="#4C72B0", label="Target=0", s=20
    )
    plt.scatter(
        sample_df[sample_df["target"] == 1]["days_since_last_session"],
        sample_df[sample_df["target"] == 1]["sess_count"],
        alpha=0.5, color="#DD8452", label="Target=1", s=25, marker="^"
    )
    plt.title("RFM Behavioral Landscape: Recency vs Session Frequency", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Days Since Last Session (Recency)", fontsize=11)
    plt.ylabel("Total Sessions (Frequency)", fontsize=11)
    plt.legend(frameon=True, facecolor="white")
    plt.tight_layout()
    plt.savefig(EDA_DIR / "eda_8_recency_and_frequency_rfm.png", dpi=200)
    plt.close()
    logger.info("Saved eda_8_recency_and_frequency_rfm.png")

    # -------------------------------------------------------------
    # 9. Synthetic Noise Variables vs Target (Audit & Justification for PSO)
    # -------------------------------------------------------------
    noise_cols = [f"noise_customer_{i}" for i in range(5)] + ["avg_noise_trans_0", "avg_noise_trans_1"]
    noise_corrs = [train_df[["target", col]].corr().iloc[0, 1] for col in noise_cols]

    plt.figure(figsize=(9, 5))
    bars = plt.bar(noise_cols, noise_corrs, color="#8172B3", edgecolor="black", width=0.55)
    plt.axhline(0, color="black", linewidth=1.2)
    plt.title("Empirical Correlation of Injected Synthetic Noise Variables vs Target (~0.00)", fontsize=13, fontweight="bold", pad=12)
    plt.ylabel("Pearson Correlation with Target", fontsize=11)
    plt.ylim(-0.05, 0.05)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.003 if yval >= 0 else yval - 0.006, f"{yval:.4f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    plt.tight_layout()
    plt.savefig(EDA_DIR / "eda_9_synthetic_noise_audit.png", dpi=200)
    plt.close()
    logger.info("Saved eda_9_synthetic_noise_audit.png")

    # -------------------------------------------------------------
    # 10. Generate outputs/eda_customer_summary.csv
    # -------------------------------------------------------------
    numeric_summary_cols = [
        "age", "credit_limit", "loyalty_score", "email_open_rate",
        "discount_usage_rate", "avg_review_score", "sess_count",
        "avg_session_duration", "total_cart_additions", "bounce_rate",
        "trans_count", "total_spend", "avg_order_value", "trans_discount_rate",
        "engagement_score"
    ]
    summary_records = []
    for col in numeric_summary_cols:
        if col in train_df.columns:
            s0 = train_df[train_df["target"] == 0][col].dropna()
            s1 = train_df[train_df["target"] == 1][col].dropna()
            summary_records.append({
                "metric_name": col,
                "target_0_mean": round(s0.mean(), 4),
                "target_0_std": round(s0.std(), 4),
                "target_0_median": round(s0.median(), 4),
                "target_1_mean": round(s1.mean(), 4),
                "target_1_std": round(s1.std(), 4),
                "target_1_median": round(s1.median(), 4),
                "relative_difference_pct": round(((s1.mean() - s0.mean()) / (s0.mean() if s0.mean() != 0 else 1.0)) * 100, 2)
            })

    summary_df = pd.DataFrame(summary_records)
    summary_path = OUTPUTS_DIR / "eda_customer_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    logger.info(f"Saved EDA customer summary table to {summary_path}")

    logger.info("=== EDA PHASE COMPLETED SUCCESSFULLY ===")
    return summary_df


if __name__ == "__main__":
    run_eda()
