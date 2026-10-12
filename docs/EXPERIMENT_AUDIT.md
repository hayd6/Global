# Experiment Audit

Ngay kiem toan: 2026-10-12  
Vai tro: reviewer doc lap, doi chieu repo/artifacts thuc te voi HANDOFF.md.  
Trang thai tong quat: **FAIL / INSUFFICIENT EVIDENCE** cho ket luan thuc nghiem ML hien tai.

Ly do chinh: pipeline co artifacts day du va test hien tai pass, nhung chua chung minh duoc tinh hop le thoi gian cua feature, cac bang so sanh khong dung cung mot split/preprocessing, PSO duoc toi uu tren validation rieng roi duoc bao cao lai tren validation noi bo khac, va README/docs dang co nhieu metric cu khong khop voi artifacts moi nhat.

## 1. Pham vi da kiem tra

Da kiem tra:

- `HANDOFF.md`, `AGENTS.md`, `PRD.md`, `README.md`, cac tai lieu trong `docs/`.
- Code: `src/config.py`, `src/pipeline.py`, `src/data/*.py`, `src/features/build_features.py`, `src/models/*.py`, `src/evaluation/evaluate.py`, `src/export/export_outputs.py`.
- Tests: 4 file trong `tests/`.
- Artifacts: `outputs/customer_features.parquet`, CSV metrics, selected features, PSO config/convergence, Power BI exports, data quality reports.
- Lenh nhe: row/column counts, ID coverage, date ranges, feature counts, target rates, `pytest -v`.

Chua chay:

- Khong chay `python src/pipeline.py` vi pipeline ghi de artifacts trong `outputs/` va chua can thiet cho audit ban dau.
- Khong train lai model/PSO tu dau ngoai cac tests nhe.
- Khong xac minh bang Power BI/website vi khong co artifact Power BI report hoac website app trong repo.

## 2. Inventory da xac minh

Repo:

- Thu muc hien tai khong phai Git repository: `git status --short` tra ve `fatal: not a git repository`; `.git` khong ton tai.
- Co du 8 CSV nguon trong `dataset/`.
- Co code pipeline, tests va artifacts trong `outputs/`.
- Phan lon artifacts co timestamp 2026-10-12 07:47-07:49; `pso_selected_features.csv` va `pso_convergence.csv` goc timestamp 07:40, ban Power BI copy timestamp 07:49.

Dataset counts da xac minh:

| File | Rows | Columns | Ghi chu |
|---|---:|---:|---|
| `customers.csv` | 200,000 | 17 | Khop HANDOFF |
| `geo_data.csv` | 100 | 5 | Khop HANDOFF |
| `marketing_campaigns.csv` | 200 | 6 | **Khac HANDOFF: khong phai 200,000** |
| `sessions.csv` | 2,000,000 | 11 | Khop HANDOFF |
| `transactions.csv` | 500,000 | 11 | Khop HANDOFF |
| `train.csv` | 160,000 | 2 | Khop HANDOFF |
| `test.csv` | 40,000 | 1 | Khop HANDOFF |
| `sample_submission.csv` | 40,000 | 2 | Khop HANDOFF |

Data checks da xac minh:

- Target train: 127,514 label 0 va 32,486 label 1; positive rate = 0.2030375.
- Train/test customer overlap = 0.
- Train/test customer IDs deu co trong `customers.csv`.
- Date ranges: `sessions.session_timestamp`, `transactions.transaction_timestamp`, `customers.signup_date` deu nam tu 2022-01-01 den 2024-09-26. `marketing_campaigns.start_date` tu 2022-01-01 den 2022-12-30, `end_date` tu 2022-02-25 den 2023-04-21.
- `outputs/customer_features.parquet`: 200,000 rows x 72 columns; split `train` 160,000 rows, `test` 40,000 rows.
- `outputs/feature_dictionary.csv`: 67 rows.

## 3. Findings

### Critical 1: Chua chung minh duoc tinh hop le thoi gian; feature co nguy co leakage lon

Bang chung:

- `src/data/integrate_data.py` tinh aggregate session/transaction tren toan bo `v_cleaned_sessions` va `v_cleaned_transactions`, sau do join truc tiep voi train/test labels. Cac dong lien quan: session aggregate tai lines 33-100, transaction aggregate tai lines 104-132, join label tai lines 146-221.
- Cac recency feature dung hard-coded `DATE '2024-09-26'`: `days_since_last_session` line 90, `days_since_last_transaction` line 131, `account_age_days` line 168.
- Cac feature PSO chon gom nhieu bien hau mua/hau hanh vi: `has_transactions`, `trans_count`, `total_spend`, `avg_items_per_order`, `spend_per_session`, `loyalty_spend_product` trong `outputs/feature_selection/pso_selected_features.csv`.
- Khong tim thay tai lieu/code xac dinh prediction cutoff, label window 30 ngay, hoac quy tac loai tru event sau cutoff.

Tac dong:

- Neu `target` la "mua trong 30 ngay tiep theo", cac aggregate tu toan bo lich su den 2024-09-26 co the chua ca thong tin sau thoi diem du doan hoac trong window tao nhan.
- Metric PR-AUC/ROC-AUC hien tai co the bi thoi phong; khong the ket luan model co kha nang du doan tuong lai.

Cach sua:

- Dinh nghia ro prediction cutoff va label window trong config/tai lieu.
- Tao feature table theo logic point-in-time: chi dung event co timestamp <= cutoff; neu target la 30 ngay sau cutoff thi loai event trong `(cutoff, cutoff + 30d]` khoi features.
- Neu dataset khong cung cap cutoff/label generation, phai gioi han ket luan thanh bai toan "classification tren snapshot da cho", khong goi la du doan tuong lai.

Cach xac minh sau sua:

- Them test kiem tra max timestamp duoc dung trong feature <= cutoff cho tung customer.
- Audit feature dictionary co cot `available_at`/`cutoff_rule`.
- Chay lai pipeline vao thu muc output moi va so sanh metric tren split hop le.

### High 1: Cac bang baseline 180 features va 63/17 features khong cung mot thiet ke thuc nghiem

Bang chung:

- Baseline 180 features trong `src/models/baselines.py` dung `train_test_split(..., random_state=RANDOM_STATE, stratify=y)` lines 85-87 va ColumnTransformer one-hot categorical lines 104-122.
- Bang 63/17 trong `src/models/feature_selection.py` drop categorical columns (`country_code`, `region`, `customer_tier`, `region_tier`) lines 56-68, sau do split theo thu tu dong `X_all_raw[:split_idx]` lines 75-77.
- XGBoost comparison trong `src/models/train_xgboost.py` cung drop categorical columns lines 65-78 va split theo thu tu dong lines 84-86.
- Artifact check: baseline raw cols = 67, categorical cols = 4, transformed feature dimension = 180; XGBoost/feature-selection candidate cols = 63.

Tac dong:

- Khong the so sanh truc tiep bang 180 feature voi bang 63/17 feature nhu mot chuoi ket qua duy nhat.
- Khac biet metric co the do encoding/split/preprocessing khac nhau, khong phai do model hay PSO.

Cach sua:

- Dung mot ham split chung tra ve indices va luu indices vao artifact.
- Dung cung candidate feature set hoac giai thich ro moi bang la experiment rieng.
- Neu can so sanh PSO voi full model, full/stat/PSO phai chung target, split, preprocessing, metric va model family.

Cach xac minh sau sua:

- Metrics CSV co cot `experiment_id`, `split_id`, `feature_space_id`, `preprocessing_id`.
- Test tu dong assert cac experiment trong cung bang co cung validation customer IDs.

### High 2: PSO fitness va final evaluation dung validation khac nhau; co selection bias va khong tinh search cost

Bang chung:

- `src/models/pso_optimizer.py` lay sample 30,000 dong bang `df.sample(... random_state=42)` line 239, scale truoc split line 245, va split theo thu tu sample lines 247-249.
- Fitness la `0.92 * PR-AUC + 0.08 * sparsity` trong `evaluate_fitness` lines 78-101, dung LogisticRegression tren PSO validation.
- `src/models/feature_selection.py` neu `pso_selected_features.csv` ton tai thi load lai artifact lines 84-91, sau do danh gia bang HistGradientBoosting tren validation theo thu tu dong lines 75-77 va 124-143.
- `configs/pso_experiment_config.json`: PSO best PR-AUC = 0.2370, selected 17/63 features; `outputs/metrics/metrics_comparison.csv`: `Baseline (PSO Features)` PR-AUC = 0.2643 va `XGBoost (PSO Features)` PR-AUC = 0.2586 tren evaluation khac.
- Fit time trong metric chi la fit model sau khi co feature; khong bao gom PSO search 16 particles x 12 iterations.

Tac dong:

- Bao cao co the danh gia feature set da duoc chon bang validation noi bo khac ma khong co holdout/doc lap; selection bias chua duoc kiem soat.
- Khong the noi PSO giam thoi gian tong the neu chi do fit time.

Cach sua:

- Tach train/feature-selection-validation/final-validation hoac dung nested CV nhe.
- Luu `pso_search_time_seconds`, so lan fitness evaluation, sample IDs, split IDs.
- Bao cao PSO fitness rieng voi final model metrics; khong tron y nghia hai PR-AUC.

Cach xac minh sau sua:

- Config/convergence co `search_time_seconds`, `n_unique_masks_evaluated`, `selection_split_id`.
- Final comparison dung holdout chua tham gia PSO.

### High 3: Preprocessing trong PSO/feature selection/XGBoost khong leakage-free nhu tai lieu mo ta

Bang chung:

- `src/models/baselines.py` fit preprocessor tren train partition roi transform validation lines 120-121.
- `src/models/pso_optimizer.py` goi `scaler.fit_transform(X_raw)` truoc khi chia train/validation lines 245-249.
- `src/models/feature_selection.py` scaler fit tren `X_train_raw` lines 80-81, nhung split van theo thu tu dong va fillna tren toan bo `df[all_candidate_cols].fillna(0).values` line 71.
- `src/models/train_xgboost.py` scaler fit tren train split lines 89-90, nhung split theo thu tu dong, khong stratify nhu comment line 83 va docs `REPRODUCIBILITY.md` line 65.

Tac dong:

- PSO scaler thay duoc phan phoi validation, gay leakage preprocessing nhe.
- Tai lieu noi "stratified" nhung code XGBoost/feature-selection khong stratify; tinh tai lap va cong bang bi suy yeu.

Cach sua:

- Dung `train_test_split(..., stratify=y)` hoac split time-based co ly do, truoc moi fit scaler/selector.
- Dat imputer/scaler trong Pipeline/ColumnTransformer cho moi experiment.

Cach xac minh sau sua:

- Test monkeypatch/fixture dam bao scaler/selector chi fit tren train indices.
- Docs cap nhat dung split strategy thuc te.

### High 4: Tai lieu ket luan PSO "giu vung"/"chap nhan H2" khong duoc artifacts moi nhat ung ho

Bang chung:

- `README.md` lines 32-38 bao cao metric cu va ket luan PSO bao toan nang luc du doan, giam XGBoost time hon 50%.
- `docs/EXPERIMENT_PLAN.md` lines 11-12 chap nhan H1/H2; lines 37-41 bao cao metric cu.
- Artifact moi `outputs/metrics/metrics_comparison.csv`: XGBoost full PR-AUC 0.2723, ROC-AUC 0.6018; XGBoost PSO PR-AUC 0.2586, ROC-AUC 0.5857. Chenh lech PR-AUC = -0.0137, ROC-AUC = -0.0161. Accuracy cua XGBoost PSO trong artifact la 0.4134, khong phai cao hon full.
- `docs/DECISIONS.md` line 28 noi giam hon 70% thoi gian huan luyen, nhung khong tinh PSO search cost.

Tac dong:

- Bao cao Power BI/bao cao hoc thuat co nguy co dua ket luan sai: PSO giam feature nhung giam PR-AUC/ROC-AUC.

Cach sua:

- Cap nhat README/docs tu artifact hien tai, va ghi ro trade-off: PSO giam 73.02% feature nhung lam giam PR-AUC/ROC-AUC trong bang hien co.
- Khong "chap nhan H2" neu tieu chi tuong duong chua duoc dinh nghia va kiem dinh.

Cach xac minh sau sua:

- Script/doc test so sanh cac bang trong docs voi CSV artifact.
- Moi ket luan PSO phai kem metric, baseline, split ID va chi phi search.

### Medium 1: Threshold duoc chon tren cung validation dung de bao cao metric

Bang chung:

- `src/evaluation/evaluate.py` neu `threshold is None` thi toi uu F1 tren `precision_recall_curve(y_true, y_prob)` lines 54-58, sau do tinh F1/precision/recall/accuracy tren cung `y_true` lines 62-68.

Tac dong:

- F1/precision/recall/accuracy la optimistic cho validation da dung chon threshold. PR-AUC/ROC-AUC it bi anh huong hon vi threshold-free.

Cach sua:

- Bao cao PR-AUC/ROC-AUC la metric chinh; neu can threshold metric, chon threshold tren tuning split rieng hoac co dinh 0.5/chi phi kinh doanh.

Cach xac minh sau sua:

- Metrics CSV co cot `threshold_source` va `threshold`.
- Test dam bao final holdout khong duoc dung de chon threshold.

### Medium 2: Marketing campaign row count trong HANDOFF/documentation khong khop du lieu thuc te

Bang chung:

- Kiem tra DuckDB: `marketing_campaigns.csv` = 200 rows x 6 columns.
- HANDOFF noi 200,000 rows; `outputs/data_quality_report.csv` cung xac nhan 200 rows.

Tac dong:

- Tai lieu dataset inventory co sai so lon; anh huong dien giai quy mo du lieu marketing.

Cach sua:

- Cap nhat tai lieu inventory thanh 200 rows, 6 columns.

Cach xac minh sau sua:

- Chay lai data audit va doi chieu `outputs/data_quality_report.csv`.

### Medium 3: Tests pass nhung chua bao phu cac rui ro thuc nghiem quan trong

Bang chung:

- `pytest -v`: 11/11 pass, 1 warning cache.
- Tests hien co kiem tra file ton tai, primary key, shape, feature finite, metric bounded, PSO toy. Khong co test cho point-in-time leakage, split ID consistency, stale docs/metrics, PSO search cost, hay final holdout.

Tac dong:

- Test pass khong du de nghiem thu thuc nghiem ML.

Cach sua:

- Them tests cho split consistency, no target/customer_id in features, preprocessing fit-only-train, point-in-time cutoff, artifact-doc sync.

Cach xac minh sau sua:

- `pytest -v` pass voi cac test moi; tests fail neu doi split/candidate feature khong cap nhat metadata.

### Medium 4: `export_outputs.py` import runner co side-effect risk va comment khong dung

Bang chung:

- `src/export/export_outputs.py` lines 104-106 comment noi tao validation errors, nhung code chi import `run_xgboost_experiments` va khong dung.
- Export copy `test_predictions.csv` neu ton tai lines 110-114; khong sinh bang validation error.

Tac dong:

- Tai lieu/code comment gay nham lan ve artifact duoc export; import khong can thiet co the gay rui ro neu module thay doi side effect trong tuong lai.

Cach sua:

- Xoa import khong dung, cap nhat comment/export list dung artifact thuc te.

Cach xac minh sau sua:

- Static lint/import check; PowerBI folder co manifest ro.

### Low 1: Khong co Git metadata de truy vet thay doi

Bang chung:

- `git status --short` tra ve `fatal: not a git repository`.
- `.git` khong ton tai.

Tac dong:

- Kho truy vet artifact/code version, tac gia thay doi, va reproducibility theo commit hash.

Cach sua:

- Khoi tao Git repo hoac lam viec trong clone co `.git`; luu commit hash vao experiment metadata.

Cach xac minh sau sua:

- `git status --short` hoat dong; metrics/config co `git_commit`.

### Low 2: Ten model "Support Vector Machine" co the gay nham lan

Bang chung:

- `src/models/baselines.py` khai bao `"Support Vector Machine": SGDClassifier(loss="log_loss", ...)` lines 170-172.
- Day khong phai SVC kernel SVM; la linear classifier trained by SGD voi logistic loss.

Tac dong:

- Bao cao co the lam nguoi doc hieu nham ve loai model.

Cach sua:

- Doi ten thanh `SGDClassifier (log_loss)` hoac `Linear SGD Logistic Classifier`.

Cach xac minh sau sua:

- `baseline_metrics.csv` va docs dung ten moi.

## 4. Doi chieu metric tu artifacts

### Baseline 180 transformed features

Artifact: `outputs/metrics/baseline_metrics.csv`

| Model | Features | PR-AUC | ROC-AUC | F1 | Precision | Recall | Fit time |
|---|---:|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 180 | 0.2629 | 0.5976 | 0.3600 | 0.2381 | 0.7376 | 1.06 |
| Naive Bayes | 180 | 0.2166 | 0.5195 | 0.3381 | 0.2036 | 0.9966 | 0.42 |
| Decision Tree | 180 | 0.2536 | 0.5899 | 0.3584 | 0.2419 | 0.6920 | 7.28 |
| Random Forest | 180 | 0.2673 | 0.6018 | 0.3637 | 0.2454 | 0.7022 | 12.97 |
| Gradient Boosting | 180 | 0.2726 | 0.6106 | 0.3675 | 0.2520 | 0.6789 | 16.82 |
| K-Nearest Neighbors | 180 | 0.2117 | 0.5183 | 0.3375 | 0.2030 | 1.0000 | 6.27 |
| Support Vector Machine | 180 | 0.2534 | 0.5862 | 0.3555 | 0.2333 | 0.7468 | 3.28 |

Khac README/HANDOFF o nhieu so lieu nho; README dang stale.

### 63/17 feature comparison

Artifact: `outputs/metrics/metrics_comparison.csv`

| Model | Features | PR-AUC | ROC-AUC | F1 | Precision | Recall | Accuracy | Fit time |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline Full | 63 | 0.2787 | 0.6098 | 0.3689 | 0.2491 | 0.7110 | 0.5001 | 14.60 |
| Baseline Statistical | 17 | 0.2778 | 0.6098 | 0.3682 | 0.2504 | 0.6951 | 0.5096 | 6.21 |
| Baseline PSO | 17 | 0.2643 | 0.5917 | 0.3572 | 0.2364 | 0.7300 | 0.4599 | 4.00 |
| XGBoost Full | 63 | 0.2723 | 0.6018 | 0.3651 | 0.2413 | 0.7502 | 0.4638 | 3.18 |
| XGBoost PSO | 17 | 0.2586 | 0.5857 | 0.3556 | 0.2297 | 0.7874 | 0.4134 | 1.51 |

Da xac minh:

- 63 -> 17 la giam 73.02% so feature.
- XGBoost PSO thap hon XGBoost Full ve PR-AUC (-0.0137) va ROC-AUC (-0.0161).
- Accuracy XGBoost PSO cung thap hon artifact full (0.4134 vs 0.4638), khac voi mot so mo ta cu.

## 5. Lenh da chay va ket qua

- `Get-Content -Raw -LiteralPath HANDOFF.md`: da doc; terminal hien thi mojibake nhung noi dung chinh xac dinh duoc.
- `Get-ChildItem -Force`: liet ke root repo.
- `rg --files`: liet ke file repo/artifacts.
- `git status --short`: fail vi khong phai Git repo.
- `Get-ChildItem outputs -Recurse -File | Select-Object FullName, Length, LastWriteTime`: xac minh artifacts/timestamps.
- `Get-ChildItem dataset -File | Select-Object Name, Length, LastWriteTime`: xac minh 8 CSV nguon.
- `Get-ChildItem docs -File | Select-Object Name, Length, LastWriteTime`: xac minh docs.
- Doc static cac file code chinh bang `Get-Content -Raw`.
- `rg -n ... src tests docs README.md`: lay bang chung line-level cho split/threshold/PSO/docs.
- Python/DuckDB checks: row/column counts, target counts, ID overlap, date ranges, parquet rows/cols, feature counts, selected features.
- `pytest -v`: 11 passed, 1 warning ve pytest cache path.
- `rg -n -i "api...|secret|token|password..." .`: khong thay secret ro rang ngoai noi dung HANDOFF yeu cau audit secrets.

## 6. Ke hoach sua loi uu tien

1. Dinh nghia prediction cutoff/label window; neu khong co nguon, gioi han lai ket luan va loai/flag cac feature giao dich/session co nguy co leakage.
2. Viet split manager chung, luu split indices va metadata; dong bo baseline/full/stat/PSO/XGBoost tren cung split hop le.
3. Sua PSO workflow: selection split rieng, scaler fit sau split, luu search cost/evaluation count/sample IDs.
4. Cap nhat metric/docs tu artifacts hien tai; rut lai ket luan PSO "giu vung/tot hon" neu khong co bang chung.
5. Them tests cho leakage thoi gian, split consistency, preprocessing fit-only-train, artifact-doc sync.
6. Chuan hoa ten model `SGDClassifier (log_loss)` va cap nhat Power BI export manifest/comment.

## 7. Gioi han con lai

- Chua the ket luan dataset goc khong leakage vi khong co quy tac tao target/cutoff.
- Chua the tai lap hoan toan metric neu khong chay lai pipeline; tuy nhien artifacts hien tai da du de phat hien bat nhat.
- Khong co Git commit/version de gan code voi artifacts.
- Chua audit noi dung hinh PNG bang mat thuong; chi xac minh file ton tai/timestamp.
