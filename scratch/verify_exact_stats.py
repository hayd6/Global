import duckdb
import pandas as pd
from pathlib import Path

con = duckdb.connect()
t_path = "outputs/controlled_benchmark/transactions.csv"
l_path = "outputs/controlled_benchmark/customer_labels_pit.csv"
feat_path = "outputs/controlled_benchmark/customer_features_pit.parquet"

print("Transaction Date Range:")
print(con.execute(f"SELECT min(transaction_timestamp), max(transaction_timestamp) FROM read_csv_auto('{t_path}')").fetchall())

tx_pre = con.execute(f"SELECT count(*) FROM read_csv_auto('{t_path}') WHERE transaction_timestamp <= DATE '2024-06-01'").fetchone()[0]
tx_post = con.execute(f"SELECT count(*) FROM read_csv_auto('{t_path}') WHERE transaction_timestamp > DATE '2024-06-01' AND transaction_timestamp <= DATE '2024-07-01'").fetchone()[0]
tx_total = con.execute(f"SELECT count(*) FROM read_csv_auto('{t_path}')").fetchone()[0]
print(f"Transactions pre-cutoff (<= 2024-06-01): {tx_pre}")
print(f"Transactions prediction window (2024-06-01 to 2024-07-01]: {tx_post}")
print(f"Total transactions: {tx_total} (pre + post = {tx_pre + tx_post})")

future_custs = con.execute(f"SELECT count(DISTINCT customer_id) FROM read_csv_auto('{t_path}') WHERE transaction_timestamp > DATE '2024-06-01' AND transaction_timestamp <= DATE '2024-07-01'").fetchone()[0]
print(f"Distinct future buyers in window: {future_custs}")

labels_df = pd.read_csv(l_path)
print(f"Target distribution in labels: {labels_df['target'].value_counts().to_dict()}")

feat_df = pd.read_parquet(feat_path)
print(f"Feature table columns count: {len(feat_df.columns)}")
print("Check feature means by target:")
for col in ["total_cart_additions", "total_session_duration", "total_spend", "total_pages_viewed"]:
    m0 = feat_df[feat_df["target"] == 0][col].mean()
    m1 = feat_df[feat_df["target"] == 1][col].mean()
    print(f"  {col}: target 0 = {m0:.4f}, target 1 = {m1:.4f}, ratio = {m1/m0 if m0>0 else 'inf':.4f}")

print("\nCorrelations with target:")
for col in ["total_cart_additions", "total_session_duration", "total_pages_viewed", "total_spend"]:
    corr = feat_df[col].corr(feat_df["target"])
    print(f"  {col} corr with target: {corr:.4f}")

print("\nCollinearities:")
print("  total_pages_viewed vs total_session_duration:", feat_df["total_pages_viewed"].corr(feat_df["total_session_duration"]))
print("  total_spend vs trans_count:", feat_df["total_spend"].corr(feat_df["trans_count"]))
