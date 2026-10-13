import duckdb
con = duckdb.connect()
t_path = "outputs/controlled_benchmark/transactions.csv"
print(con.execute(f"""
    SELECT 
        CASE 
            WHEN transaction_timestamp <= DATE '2024-06-01' THEN 'Historical (<= 2024-06-01)'
            ELSE 'Prediction Window (2024-06-02 to 2024-07-01)'
        END as period,
        count(*) as tx_count,
        min(transaction_timestamp) as min_date,
        max(transaction_timestamp) as max_date
    FROM read_csv_auto('{t_path}')
    GROUP BY 1
""").fetchdf())

print("\nJune 2024 transactions daily breakdown:")
print(con.execute(f"""
    SELECT transaction_timestamp, count(*)
    FROM read_csv_auto('{t_path}')
    WHERE transaction_timestamp >= DATE '2024-05-25'
    GROUP BY 1
    ORDER BY 1
""").fetchdf())
