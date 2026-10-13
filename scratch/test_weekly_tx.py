import duckdb
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

con = duckdb.connect()
t_path = "outputs/controlled_benchmark/transactions.csv"

# Query weekly transactions
df_weekly = con.execute(f"""
    SELECT 
        DATE_TRUNC('week', CAST(transaction_timestamp AS DATE)) as week_start,
        COUNT(*) as tx_count,
        CASE 
            WHEN MAX(CAST(transaction_timestamp AS DATE)) <= DATE '2024-06-01' THEN 'Historical (<= 2024-06-01)'
            ELSE 'Prediction Window (> 2024-06-01)'
        END as period
    FROM read_csv_auto('{t_path}')
    GROUP BY 1
    ORDER BY 1
""").fetchdf()

print(df_weekly.head(10))
print(df_weekly.tail(10))
print("Weekly count:", len(df_weekly))
