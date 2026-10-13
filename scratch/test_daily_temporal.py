import duckdb
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

con = duckdb.connect()
t_path = "outputs/controlled_benchmark/transactions.csv"

df_daily = con.execute(f"""
    SELECT 
        CAST(transaction_timestamp AS DATE) as tx_date,
        COUNT(*) as tx_count
    FROM read_csv_auto('{t_path}')
    GROUP BY 1
    ORDER BY 1
""").fetchdf()

df_daily["tx_date"] = pd.to_datetime(df_daily["tx_date"])
df_daily = df_daily.set_index("tx_date").asfreq("D", fill_value=0).reset_index()
df_daily["rolling_7d"] = df_daily["tx_count"].rolling(7, min_periods=1).mean()

cutoff_dt = pd.Timestamp("2024-06-01")

hist_df = df_daily[df_daily["tx_date"] <= cutoff_dt]
future_df = df_daily[df_daily["tx_date"] > cutoff_dt]

print(f"Historical days: {len(hist_df)}, Future days: {len(future_df)}")
print(f"Hist sum: {hist_df['tx_count'].sum()}, Future sum: {future_df['tx_count'].sum()}")

plt.figure(figsize=(10, 4.5), dpi=200)
plt.plot(hist_df["tx_date"], hist_df["rolling_7d"], color="#4C72B0", linewidth=1.8, label=f"Historical Observation (<= 2024-06-01, N={hist_df['tx_count'].sum():,})")
plt.plot(future_df["tx_date"], future_df["rolling_7d"], color="#E24A33", linewidth=2.0, label=f"Prediction Window (2024-06-02 to 2024-07-01, N={future_df['tx_count'].sum():,})")
plt.axvline(x=cutoff_dt, color="#222222", linestyle="--", linewidth=1.5, label="Cutoff t0 (2024-06-01)")
plt.axvspan(cutoff_dt, pd.Timestamp("2024-07-01"), color="#E24A33", alpha=0.15)
plt.title("Daily Transaction Timeline (7-Day Moving Avg) with Explicit Point-in-Time Cutoff", fontsize=11, fontweight="bold", pad=10)
plt.xlabel("Date", fontsize=10)
plt.ylabel("Transactions / Day (7d MA)", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(frameon=True, facecolor="white", loc="upper left", fontsize=8.5)
plt.tight_layout()
plt.savefig("outputs/controlled_benchmark/eda/eda_7_temporal_activity.png", dpi=200)
plt.close()
print("Saved eda_7_temporal_activity.png successfully!")
