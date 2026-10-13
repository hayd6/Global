import pandas as pd

feat_df = pd.read_parquet("outputs/controlled_benchmark/customer_features_pit.parquet")
print("Sum of trans_count in feature store:", feat_df["trans_count"].sum())
print("Sum of sess_count in feature store:", feat_df["sess_count"].sum())
