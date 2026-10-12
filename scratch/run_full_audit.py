"""
Comprehensive Repository Audit Script.
Executes detailed data quality audit on all 8 raw CSVs, joins, features, splits, and models.
"""

import hashlib
import json
import os
import sys
from pathlib import Path
import duckdb
import numpy as np
import pandas as pd

PROJECT_ROOT = Path("d:/HuyD/Đại Học/BigData/Global")
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    DATA_DIR,
    OUTPUTS_DIR,
    CUSTOMERS_CSV,
    GEO_DATA_CSV,
    MARKETING_CSV,
    SESSIONS_CSV,
    TRANSACTIONS_CSV,
    TRAIN_CSV,
    TEST_CSV,
    SAMPLE_SUBMISSION_CSV,
)

con = duckdb.connect()

print("=" * 80)
print("1. RAW CSV DATA AUDIT")
print("=" * 80)

raw_files = {
    "customers": CUSTOMERS_CSV,
    "geo_data": GEO_DATA_CSV,
    "marketing_campaigns": MARKETING_CSV,
    "sessions": SESSIONS_CSV,
    "transactions": TRANSACTIONS_CSV,
    "train": TRAIN_CSV,
    "test": TEST_CSV,
    "sample_submission": SAMPLE_SUBMISSION_CSV,
}

csv_audit = {}

for name, path in raw_files.items():
    size_mb = round(os.path.getsize(path) / (1024 * 1024), 2)
    df_desc = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{path.as_posix()}')").fetchall()
    row_count = con.execute(f"SELECT COUNT(*) FROM read_csv_auto('{path.as_posix()}')").fetchone()[0]
    col_names = [col[0] for col in df_desc]
    col_types = {col[0]: col[1] for col in df_desc}
    
    # Check total duplicate rows
    dup_rows = con.execute(f"SELECT COUNT(*) - COUNT(*) FROM (SELECT DISTINCT * FROM read_csv_auto('{path.as_posix()}'))").fetchone()[0]
    total_distinct_rows = con.execute(f"SELECT COUNT(*) FROM (SELECT DISTINCT * FROM read_csv_auto('{path.as_posix()}'))").fetchone()[0]
    exact_duplicates = row_count - total_distinct_rows

    col_stats = {}
    for col in col_names:
        res = con.execute(
            f"""
            SELECT 
                COUNT(CASE WHEN "{col}" IS NULL THEN 1 END) AS null_cnt,
                COUNT(DISTINCT "{col}") AS distinct_cnt,
                COUNT(CASE WHEN CAST("{col}" AS VARCHAR) = '' THEN 1 END) AS empty_str_cnt,
                COUNT(CASE WHEN LOWER(TRIM(CAST("{col}" AS VARCHAR))) IN ('unknown', 'n/a', 'null', 'none') THEN 1 END) AS placeholder_cnt
            FROM read_csv_auto('{path.as_posix()}')
            """
        ).fetchone()
        col_stats[col] = {
            "type": col_types[col],
            "null_count": res[0],
            "null_pct": round(res[0] * 100.0 / row_count, 3) if row_count > 0 else 0,
            "distinct_count": res[1],
            "empty_str_count": res[2],
            "placeholder_count": res[3],
        }

    csv_audit[name] = {
        "path": str(path),
        "size_mb": size_mb,
        "row_count": row_count,
        "col_count": len(col_names),
        "exact_duplicates": exact_duplicates,
        "columns": col_stats,
    }
    print(f"[{name}] Rows: {row_count:,}, Cols: {len(col_names)}, Size: {size_mb} MB, Exact Dups: {exact_duplicates}")

print("\n" + "=" * 80)
print("2. RELATIONAL INTEGRITY & JOINS AUDIT")
print("=" * 80)

# Check PKs
pk_map = {
    "customers": "customer_id",
    "sessions": "session_id",
    "transactions": "transaction_id",
    "marketing_campaigns": "campaign_id",
    "geo_data": "geo_ip_region",
    "train": "customer_id",
    "test": "customer_id",
    "sample_submission": "customer_id",
}

for name, pk in pk_map.items():
    path = raw_files[name]
    res = con.execute(
        f"""
        SELECT 
            COUNT(*) - COUNT(DISTINCT "{pk}") AS pk_duplicates,
            COUNT(CASE WHEN "{pk}" IS NULL THEN 1 END) AS pk_nulls
        FROM read_csv_auto('{path.as_posix()}')
        """
    ).fetchone()
    print(f"PK [{name}.{pk}]: Duplicates = {res[0]}, Nulls = {res[1]}")

# Train / Test disjointness and coverage
overlap = con.execute(
    f"""
    SELECT COUNT(*) 
    FROM read_csv_auto('{TRAIN_CSV.as_posix()}') tr
    INNER JOIN read_csv_auto('{TEST_CSV.as_posix()}') te ON tr.customer_id = te.customer_id
    """
).fetchone()[0]
print(f"Train / Test customer_id Overlap: {overlap} (Must be 0)")

train_missing = con.execute(
    f"""
    SELECT COUNT(*) FROM read_csv_auto('{TRAIN_CSV.as_posix()}') tr
    LEFT JOIN read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c ON tr.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
    """
).fetchone()[0]
test_missing = con.execute(
    f"""
    SELECT COUNT(*) FROM read_csv_auto('{TEST_CSV.as_posix()}') te
    LEFT JOIN read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c ON te.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
    """
).fetchone()[0]
print(f"Train customers missing in customers.csv: {train_missing}, Test missing: {test_missing}")

# Check sample_submission vs test.csv
sub_test_mismatch = con.execute(
    f"""
    SELECT COUNT(*) 
    FROM read_csv_auto('{SAMPLE_SUBMISSION_CSV.as_posix()}') s
    FULL OUTER JOIN read_csv_auto('{TEST_CSV.as_posix()}') t ON s.customer_id = t.customer_id
    WHERE s.customer_id IS NULL OR t.customer_id IS NULL
    """
).fetchone()[0]
print(f"sample_submission vs test.csv customer_id mismatch: {sub_test_mismatch}")

# Sessions and transactions foreign keys
sess_orphan = con.execute(
    f"""
    SELECT COUNT(*) FROM read_csv_auto('{SESSIONS_CSV.as_posix()}') s
    LEFT JOIN read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c ON s.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
    """
).fetchone()[0]
trans_orphan = con.execute(
    f"""
    SELECT COUNT(*) FROM read_csv_auto('{TRANSACTIONS_CSV.as_posix()}') t
    LEFT JOIN read_csv_auto('{CUSTOMERS_CSV.as_posix()}') c ON t.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
    """
).fetchone()[0]
print(f"Sessions orphan customer_ids: {sess_orphan}, Transactions orphan customer_ids: {trans_orphan}")

# Sessions to geo_data & marketing
geo_orphan = con.execute(
    f"""
    SELECT COUNT(*) FROM read_csv_auto('{SESSIONS_CSV.as_posix()}') s
    LEFT JOIN read_csv_auto('{GEO_DATA_CSV.as_posix()}') g ON s.geo_ip_region = g.geo_ip_region
    WHERE g.geo_ip_region IS NULL AND s.geo_ip_region IS NOT NULL
    """
).fetchone()[0]
mkt_orphan = con.execute(
    f"""
    SELECT COUNT(*) FROM read_csv_auto('{SESSIONS_CSV.as_posix()}') s
    LEFT JOIN read_csv_auto('{MARKETING_CSV.as_posix()}') m ON s.campaign_id = m.campaign_id
    WHERE m.campaign_id IS NULL AND s.campaign_id IS NOT NULL
    """
).fetchone()[0]
print(f"Sessions orphan geo_ip_region: {geo_orphan}, Sessions orphan campaign_id: {mkt_orphan}")

# Cardinality
sess_card = con.execute(f"SELECT MIN(cnt), AVG(cnt), MAX(cnt) FROM (SELECT customer_id, count(*) cnt FROM read_csv_auto('{SESSIONS_CSV.as_posix()}') GROUP BY customer_id)").fetchone()
trans_card = con.execute(f"SELECT MIN(cnt), AVG(cnt), MAX(cnt) FROM (SELECT customer_id, count(*) cnt FROM read_csv_auto('{TRANSACTIONS_CSV.as_posix()}') GROUP BY customer_id)").fetchone()
print(f"Sessions per customer: Min={sess_card[0]}, Avg={sess_card[1]:.2f}, Max={sess_card[2]}")
print(f"Transactions per customer (for customers with trans): Min={trans_card[0]}, Avg={trans_card[1]:.2f}, Max={trans_card[2]}")

print("\n" + "=" * 80)
print("3. FEATURE ENGINEERING & PARQUET DATASET AUDIT")
print("=" * 80)

feat_parquet = OUTPUTS_DIR / "customer_features.parquet"
total_feat_rows = con.execute(f"SELECT COUNT(*) FROM read_parquet('{feat_parquet.as_posix()}')").fetchone()[0]
train_feat_rows = con.execute(f"SELECT COUNT(*) FROM read_parquet('{feat_parquet.as_posix()}') WHERE split_type = 'train'").fetchone()[0]
test_feat_rows = con.execute(f"SELECT COUNT(*) FROM read_parquet('{feat_parquet.as_posix()}') WHERE split_type = 'test'").fetchone()[0]
target_dist = con.execute(f"SELECT target, count(*), count(*)*1.0/{train_feat_rows} FROM read_parquet('{feat_parquet.as_posix()}') WHERE split_type = 'train' GROUP BY target ORDER BY target").fetchall()

print(f"Parquet Total Customers: {total_feat_rows:,} (Train: {train_feat_rows:,}, Test: {test_feat_rows:,})")
print(f"Target Distribution in Train: 0: {target_dist[0][1]:,} ({target_dist[0][2]*100:.2f}%), 1: {target_dist[1][1]:,} ({target_dist[1][2]*100:.2f}%)")

# Check all feature columns for nulls and inf
desc_feat = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{feat_parquet.as_posix()}')").fetchall()
feat_cols = [c[0] for c in desc_feat]
print(f"Total Columns in customer_features.parquet: {len(feat_cols)}")

null_cols = []
for c in feat_cols:
    nc = con.execute(f"SELECT COUNT(*) FROM read_parquet('{feat_parquet.as_posix()}') WHERE \"{c}\" IS NULL").fetchone()[0]
    if nc > 0:
        null_cols.append((c, nc, round(nc * 100.0 / total_feat_rows, 2)))

print(f"Columns with NULL in customer_features.parquet ({len(null_cols)} columns):")
for c, cnt, pct in null_cols:
    print(f"  {c}: {cnt:,} nulls ({pct}%)")

print("\n" + "=" * 80)
print("4. SPLIT INDICES & METADATA VERIFICATION")
print("=" * 80)

split_file = OUTPUTS_DIR / "processed" / "split_indices.npz"
split_meta_file = PROJECT_ROOT / "configs" / "split_metadata.json"

sp_data = np.load(split_file)
tr_idx = sp_data["train_idx"]
ho_idx = sp_data["holdout_idx"]
pso_tr_idx = sp_data["pso_inner_train_idx"]
pso_va_idx = sp_data["pso_inner_val_idx"]

print(f"train_idx len: {len(tr_idx)}, holdout_idx len: {len(ho_idx)}")
print(f"pso_inner_train_idx len: {len(pso_tr_idx)}, pso_inner_val_idx len: {len(pso_va_idx)}")
ho_tr_intersect = len(set(tr_idx).intersection(set(ho_idx)))
print(f"Intersection(train_idx, holdout_idx): {ho_tr_intersect} (Must be 0)")
pso_ho_intersect = len(set(pso_tr_idx).union(set(pso_va_idx)).intersection(set(ho_idx)))
print(f"Intersection(PSO inner tuning, holdout_idx): {pso_ho_intersect} (Must be 0)")

# Verify customer_id sha256 on actual data
df_tr = con.execute(f"SELECT customer_id, target FROM read_parquet('{feat_parquet.as_posix()}') WHERE split_type = 'train' ORDER BY customer_id").df()
cids_ho = df_tr["customer_id"].iloc[ho_idx].values.astype(np.int64)
actual_ho_sha256 = hashlib.sha256(cids_ho.tobytes()).hexdigest()

with open(split_meta_file, "r", encoding="utf-8") as f:
    meta_json = json.load(f)

print(f"Computed holdout SHA-256: {actual_ho_sha256}")
print(f"split_metadata.json SHA-256: {meta_json['holdout_sha256']}")
print(f"Match: {actual_ho_sha256 == meta_json['holdout_sha256']}")

# Summary output json
audit_summary = {
    "csv_audit": csv_audit,
    "pk_violations": {name: con.execute(f"SELECT COUNT(*) - COUNT(DISTINCT \"{pk}\") FROM read_csv_auto('{raw_files[name].as_posix()}')").fetchone()[0] for name, pk in pk_map.items()},
    "train_test_overlap": overlap,
    "total_customers": total_feat_rows,
    "train_customers": train_feat_rows,
    "test_customers": test_feat_rows,
    "target_distribution": {str(t[0]): {"count": t[1], "pct": round(t[2]*100, 2)} for t in target_dist},
    "null_columns": {c: {"count": cnt, "pct": pct} for c, cnt, pct in null_cols},
    "holdout_sha256": actual_ho_sha256,
}

with open(PROJECT_ROOT / "scratch" / "audit_summary.json", "w", encoding="utf-8") as f:
    json.dump(audit_summary, f, indent=2)

print("\nAudit summary saved to scratch/audit_summary.json.")
