# Experiment Audit V2

Ngay audit: 2026-10-12  
Vai tro: Reviewer doc lap vong 2 sau remediation.  
Pham vi: doc code, configs, tests, artifacts va tai lieu hien tai. Khong chay full pipeline, khong xoa/sua artifact, khong sua code.

## 1. Ket luan tong quan

Trang thai tong quat: **PASS WITH ISSUES / NOT FULLY VERIFIABLE**.

Nhieu remediation ve split, preprocessing, threshold, metric metadata va PSO search-cost da duoc cai thien ro rang va co artifact khop. Tuy nhien, khong chap nhan ket luan trong `docs/EXPERIMENT_AUDIT.md` rang pipeline "hoan toan Leakage-Free". Ly do: quy tac tao `target` va prediction cutoff van **khong duoc xac lap**. Pham vi observational snapshot da duoc ghi nhan trong `docs/DECISIONS.md`, nhung README/PRD/HANDOFF van dung ngon ngu "du doan tuong lai". Voi bang chung hien tai chi co the noi: **khong thay dung `customer_id`/`target` lam feature, split holdout/inner tuning khong giao nhau, preprocessing fit tren train tuong ung; temporal leakage theo nghia prediction cutoff tuong lai la not established/unknown, khong the chung minh absent**.

## 2. Bang trang thai 11 findings cu

| Finding cu | Trang thai V2 | Nhan xet ngan |
|---|---|---|
| Critical 1: Temporal leakage/cutoff unknown | **PARTIALLY RESOLVED / NOT VERIFIABLE** | Da them metadata va scope observational, nhung target generation/cutoff van unknown; docs audit/progress con tuyen bo qua manh. |
| High 1: 180 vs 63/17 khong cung thiet ke | **VERIFIED RESOLVED** | Code dung `split_manager`; artifact split_id/evaluation_set khop; 180 va 63/17 duoc trinh bay thanh hai feature spaces rieng. |
| High 2: PSO selection bias/search cost | **PARTIALLY RESOLVED** | Holdout khong nam trong inner tuning artifact; search cost duoc ghi. Nhung metrics aggregate khong the tinh lai PR-AUC neu khong co predictions/model snapshots. |
| High 3: Preprocessing leakage | **VERIFIED RESOLVED FOR MODEL SPLITS** | `fit_transform` tren train/inner-train, `transform` tren holdout/inner-val/test. Temporal feature leakage van tach rieng o Critical 1. |
| High 4: PSO claim khong duoc ung ho | **PARTIALLY RESOLVED** | README/experiment plan da ghi trade-off va search cost, nhung van chap nhan H2/H3 voi ngon ngu hoi manh; `EXPERIMENT_AUDIT.md` van ket luan fully leakage-free. |
| Medium 1: Threshold chon tren validation | **VERIFIED RESOLVED** | `compute_metrics` mac dinh threshold 0.5 va luu `best_f1_threshold_ref` chi de tham khao. |
| Medium 2: Marketing campaign count sai | **VERIFIED RESOLVED IN TESTS/ARTIFACTS** | Data va tests xac nhan 200 rows x 6 cols; HANDOFF goc van la tai lieu ban giao cu nen con ghi 200,000. |
| Medium 3: Test coverage yeu | **PARTIALLY RESOLVED** | 18 tests pass va co them split/search/threshold checks; van chua test doc-code sync, target-generation/cutoff, hash validation trong runtime. |
| Medium 4: `export_outputs.py` import/comment | **NOT VERIFIED IN THIS PASS** | Khong thay bang chung bat buoc trong V2 vi khong doc file nay sau remediation; can check rieng neu muon dong finding. |
| Low 1: Khong co Git metadata | **VERIFIED RESOLVED** | Git repo sach, co commit history. Outputs/dataset bi ignore nen artifacts local khong versioned. |
| Low 2: Ten SVM gay nham lan | **VERIFIED RESOLVED** | Code/artifact dung `SGDClassifier (log_loss)`. |

## 3. Bang chung code va artifacts

### 3.1. Target va leakage

Da xac minh:

- `src/data/integrate_data.py` van join `tr.target` vao feature table va tinh recency theo hard-coded `DATE '2024-09-26'` cho `days_since_last_session`, `days_since_last_transaction`, `account_age_days`.
- `src/features/build_features.py` da them metadata `temporal_nature`, `cutoff_rule`, `leakage_risk` cho 67 features.
- `outputs/feature_dictionary.csv` co 67 rows va cac cot `temporal_nature`, `cutoff_rule`, `leakage_risk`.
- Phan bo `leakage_risk` trong artifact: 40 `NONE`, 27 `POTENTIAL_SNAPSHOT_OVERLAP (Full history)`.
- Metadata da danh dau dung nhieu aggregate session/transaction la potential snapshot overlap.

Khong xac lap duoc:

- Khong co code hay artifact tao `target`; `train.csv` la nguon nhan co san.
- Khong co prediction cutoff/label window co the xac minh.
- Kiem tra ty le giao dich 30 ngay cuoi gan nhau giua hai nhom target khong du de chung minh target khong leakage; no chi bac bo mot gia thuyet don gian ve label 30 ngay cuoi trong `transactions.csv`.

Bat nhat tai lieu:

- `docs/DECISIONS.md` da gioi han scope thanh observational snapshot.
- README va PRD van mo ta "du doan kha nang mua hang trong tuong lai"/"du doan hanh vi mua hang".
- `docs/PROGRESS.md` va `docs/EXPERIMENT_AUDIT.md` dung ngon ngu "chung minh" target doc lap voi 30 ngay cuoi va "hoan toan Leakage-Free"; bang chung hien co khong du cho ket luan nay.

Ket luan V2:

- **No direct feature leakage found**: khong thay `customer_id`/`target` trong feature vector cua model.
- **Temporal leakage for future prediction: not established / unknown**.
- **Leakage-free claim: not verified**.

### 3.2. Split va preprocessing

Da xac minh tu `outputs/processed/split_indices.npz` va `configs/split_metadata.json`:

- Train = 128,000; Holdout = 32,000; PSO inner train = 96,000; PSO inner val = 32,000.
- Overlap train-holdout = 0.
- Overlap inner_train-holdout = 0.
- Overlap inner_val-holdout = 0.
- Overlap inner_train-inner_val = 0.
- Positive rates: overall 0.2030375, train 0.2030391, holdout 0.2030313, inner train 0.2030417, inner val 0.2030313.
- Holdout SHA256 recomputed tu `customer_id` ordered by `customer_id`: `008236ea0d8461b4d5f58b34e973766d4a696a20c97b8d28a4b9d025c99a5da2`, khop metadata.

Code evidence:

- `split_manager.py` tao split bang `train_test_split(... stratify=y)` va tao inner split tu `train_idx`.
- `get_preprocessed_features(include_categoricals=True)` fit `ColumnTransformer` tren `X_train_raw` va transform `X_holdout_raw`.
- `get_preprocessed_features(include_categoricals=False)` fit numeric pipeline tren `X_train_raw` va transform holdout.
- `pso_optimizer.py` fit `StandardScaler` tren inner train subset va transform inner val subset.
- `feature_selection.py` fit `SelectKBest` tren `X_train`, khong tren holdout.

Residual risk:

- Khi `split_indices.npz` va `split_metadata.json` ton tai, `create_or_load_splits()` load thang artifacts ma khong validate length/hash/range/overlap truoc khi tra ve. V2 da tu xac minh artifacts hien tai hop le, nhung runtime nen tu validate de tranh stale/corrupt split artifact.

### 3.3. PSO va feature selection

Da xac minh:

- PSO fitness = `0.92 * PR-AUC + 0.08 * (1 - k / D)` tren inner validation.
- PSO dung 16 particles, 12 iterations; expected evaluations = `16 * (12 + 1) = 208`, khop `configs/pso_experiment_config.json`.
- `n_unique_masks = 208`, `search_time_seconds = 11.79`, `best_pr_auc = 0.2461`, `best_fitness = 0.2848`.
- `outputs/feature_selection/pso_convergence.csv` co 13 rows, iteration 0..12, last row elapsed_seconds = 11.79.
- PSO selected 17 features; statistical selection selected 17 features.
- Statistical selection va PSO trong `metrics_comparison.csv` dung cung candidate numeric feature space 63, cung holdout, cung threshold 0.5.

Can than khi dien giai:

- PSO search cost la offline cost; voi XGBoost, tong thoi gian PSO = 14.01s so voi XGBoost full = 4.65s, nen **PSO khong nhanh hon ve total time trong experiment hien tai**.
- Voi baseline HistGB, PSO total time = 16.31s so voi full = 16.96s, nhanh hon 0.65s neu tinh search cost, nhung PR-AUC/F1/ROC-AUC deu giam.
- Metrics CSV la aggregate; khong luu probabilities, model artifact, hay run manifest day du de tinh lai PR-AUC/ROC-AUC doc lap ma khong rerun training.

## 4. Metric doi chieu tu artifacts

### 4.1. Baseline 180 transformed features

Artifact: `outputs/metrics/baseline_metrics.csv`

| Model | Features | PR-AUC | ROC-AUC | F1 | Fit time |
|---|---:|---:|---:|---:|---:|
| Gradient Boosting | 180 | 0.2758 | 0.6097 | 0.3575 | 34.85 |
| Random Forest | 180 | 0.2700 | 0.6031 | 0.3488 | 29.80 |
| Logistic Regression | 180 | 0.2649 | 0.5989 | 0.3473 | 1.49 |
| Decision Tree | 180 | 0.2584 | 0.5851 | 0.3446 | 10.23 |
| SGDClassifier (log_loss) | 180 | 0.2456 | 0.5748 | 0.3357 | 6.66 |
| Naive Bayes | 180 | 0.2161 | 0.5177 | 0.2825 | 0.57 |
| K-Nearest Neighbors | 180 | 0.2102 | 0.5167 | 0.0685 | 17.10 |

Nhan xet: bang 180 features la transformed feature space co one-hot categorical. Khong bi tron voi bang 63/17 trong artifacts hien tai.

### 4.2. 63/17 comparison va deltas

Artifact: `outputs/metrics/metrics_comparison.csv`

| Comparison | PR-AUC delta | ROC-AUC delta | F1 delta | Fit time delta | Search delta | Total time delta |
|---|---:|---:|---:|---:|---:|---:|
| Baseline PSO - Baseline Full | -0.0129 | -0.0184 | -0.0147 | -12.44s | +11.79s | -0.65s |
| XGBoost PSO - XGBoost Full | -0.0070 | -0.0160 | -0.0156 | -2.43s | +11.79s | +9.36s |

Nhan xet:

- PSO giam fit time, nhung khi tinh search cost thi chi gan ngang/nhanh hon nhe voi baseline HistGB, va cham hon ro voi XGBoost.
- Statistical ANOVA 17 features tot hon PSO 17 features tren PR-AUC/ROC-AUC/F1 va total time trong artifacts hien tai.
- Claim "PSO nhanh hon" chi dung neu noi ve **fit time sau khi da chon feature**, khong dung neu noi ve XGBoost **total time**.

### 4.3. Tai lieu vs artifacts

Khop:

- README, EXPERIMENT_PLAN, DECISIONS va EXPERIMENT_AUDIT hien dung cac so chinh trong `metrics_comparison.csv`.
- Baseline table trong README/EXPERIMENT_PLAN khop `baseline_metrics.csv`.
- `SGDClassifier (log_loss)` da duoc doi ten dung.

Con bat nhat:

- README/PRD van dung ngon ngu "du doan tuong lai", trong khi DECISIONS gioi han observational snapshot.
- `docs/EXPERIMENT_AUDIT.md` tuyen bo "PASSED / FULLY REMEDIATED" va "hoan toan Leakage-Free"; V2 khong xac minh duoc dieu nay.
- HANDOFF la tai lieu ban giao cu va van co marketing 200,000 rows, metric cu; co the chap nhan la context lich su, nhung khong nen dung lam source hien tai.
- README tree van ghi tests `(11/11 PASSED)` trong khi pytest hien la 18 tests.

## 5. Tests va reproducibility

Lenh da chay:

- `pytest -v`: **18 passed**, 1 warning ve pytest cache path.
- `git status --short`: clean.
- `git log --oneline -n 5`: co `c7ad803`, `1cdcbca`, `d1d85ec`, `0d18885`.
- Python/DuckDB checks: split overlap, hash, target rates, feature counts, metric deltas, PSO config/convergence.

Nhan xet ve tests:

- Tests moi co gia tri hon vong 1: co check split overlap, threshold 0.5, total_time formula, PSO search-cost fields, k=17 fairness.
- Tests van chua chung minh target/cutoff hop le; `test_dataset_date_bounds` chi check max timestamp <= 2024-09-26.
- Tests metadata feature dictionary chi check cot ton tai, khong verify noi dung leakage-risk/cutoff-rule co dung voi target generation.
- Chua co test runtime validate split hash/overlap khi load cached split files.
- Chua co test doc-artifact sync cho README/EXPERIMENT_PLAN/DECISIONS.

## 6. Viec can sua uu tien

### Critical

1. Sua ket luan trong `docs/EXPERIMENT_AUDIT.md`, `docs/PROGRESS.md` va cac tai lieu lien quan: thay "chung minh target khong leakage"/"hoan toan Leakage-Free" bang "target generation/cutoff not established; scope bounded to observational snapshot; no direct ID/target leakage found".
2. Dong bo README/PRD/HANDOFF-facing narrative: neu pham vi chinh thuc la observational snapshot, khong mo ta la "du doan tuong lai" tru khi co cutoff/label-window evidence.

### High

3. Them validation trong `split_manager.create_or_load_splits()` khi load cached artifacts: check lengths, range, uniqueness, overlap, stratification rates va holdout hash khop metadata.
4. Luu run manifest cho metrics: timestamp, code commit, split hash, selected feature hash, source artifact mtimes, va optionally predictions/probabilities tren holdout de co the tinh lai metrics ma khong rerun training.
5. Sua claim "PSO nhanh hon" thanh phan biet ro fit-time vs total-time. Voi XGBoost, PSO total time hien cham hon full 9.36s.

### Medium

6. Them test doc-artifact sync: parse `outputs/metrics/*.csv` va so voi bang metric trong README/EXPERIMENT_PLAN/EXPERIMENT_AUDIT.
7. Them test noi dung feature dictionary: cac aggregate full-history phai co `POTENTIAL_SNAPSHOT_OVERLAP`; khong duoc gan `NONE` cho `total_spend`, `trans_count`, `sess_count`, `cart_to_page_ratio`, v.v.
8. Cap nhat README tree tu `11/11 PASSED` thanh 18 tests.

### Low

9. Neu muon audit artifacts theo Git, can co manifest tracked nho hoac data registry; hien `outputs/` va CSV/parquet bi `.gitignore`, nen Git commit khong bao dam artifacts local la artifacts duoc review.

## 7. Bottom line

Remediation da xu ly tot cac loi thiet ke thuc nghiem noi bo: split thong nhat, holdout co lap, preprocessing fit tren train, fixed threshold, va search cost cua PSO. Tuy nhien, remediation chua du de tuyen bo bai toan "future prediction" leakage-free. Ket luan an toan hien tai la:

> Du an co the duoc trinh bay nhu **observational purchase propensity classification** voi train/holdout evaluation noi bo cong bang hon truoc. Khong nen trinh bay nhu mot pipeline du doan tuong lai hoan toan leakage-free cho den khi quy tac target va prediction cutoff duoc xac minh.
