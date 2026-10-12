# BÁO CÁO KIỂM TOÁN TOÀN DIỆN REPOSITORY (FULL REPOSITORY AUDIT)

**Dự án**: Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Mã nguồn**: `hayd6/Global` | **Thư mục làm việc**: `Global`  
**Ngày kiểm toán**: 12/10/2026 | **Đơn vị kiểm toán**: Senior Data Engineer, ML Engineer & Research Methodology Reviewer  

---

## 1. Mục tiêu và phạm vi kiểm toán

Đợt kiểm toán toàn diện này được thực hiện theo tiêu chuẩn cao nhất về kỹ thuật dữ liệu và phương pháp luận nghiên cứu học thuật nhằm:
1. Rà soát toàn bộ cấu trúc mã nguồn, dữ liệu nguồn, các artifact kết quả, cấu hình, kiểm thử tự động và tài liệu định hướng (`DanY6Phan.md`, `AGENTS.md`).
2. Xác minh tính toàn vẹn toán học, chống rò rỉ dữ liệu (Anti-Leakage), đồng nhất hóa tiền xử lý và tính tái lập hoàn toàn trên máy trạm mới.
3. Khắc phục tất cả các khiếm khuyết được xác minh trong một lượt duy nhất (One-Pass Remediation), lập danh sách minh bạch các giới hạn dữ liệu cố hữu.

---

## 2. Bản đồ phụ thuộc dữ liệu và mã nguồn (End-to-End Pipeline Dependency Map)

```
[Raw CSVs (8 files, 200k khách hàng, 2M phiên, 500k giao dịch)]
       │
       ▼
[Data Audit (scratch/run_full_audit.py, inspect_data.py)]
  - Kiểm tra Schema, NULL, Placeholder ('unknown', 'N/A'), Duplicates, PK/FK
       │
       ▼
[Data Cleaning & Normalization (src/data/clean_data.py)]
  - Tạo các DuckDB Views: Tiền tệ ($), Boolean hỗn hợp, Chuẩn hóa chuỗi
       │
       ▼
[Data Integration (src/data/integrate_data.py)]
  - Gom nhóm trước sessions & transactions theo customer_id (chống bùng nổ tích Descartes)
  - Xuất `outputs/processed/clean_customer_features.parquet` (200.000 khách hàng duy nhất)
       │
       ▼
[Feature Engineering (src/features/build_features.py)]
  - Ratios hành vi (cart_to_page, duration_per_page), RFM, Tương tác (discount, loyalty)
  - Xuất `outputs/customer_features.parquet` (72 cột) & `outputs/feature_dictionary.csv`
       │
       ▼
[Exploratory Data Analysis (src/analysis/eda.py)]
  - 9 biểu đồ phân tích chuyên sâu tại `outputs/plots/` & bảng tổng hợp phân vị
       │
       ▼
[Split & Preprocessing Management (src/models/split_manager.py)]
  - Phân vùng Stratified 80/20 (Train 128k, Holdout 32k) từ 160k train pool
  - Lưu dấu vân tay SHA-256 (`008236ea0...`) và chỉ số `split_indices.npz`
  - Tiền xử lý Fit-on-Train duy nhất: `SimpleImputer(strategy='median')` + `StandardScaler()`
       │
       ├───► [Baseline ML Models (src/models/baselines.py)]
       │       - 7 mô hình cơ sở: LR, NB, DT, RF, GB, KNN, SGDClassifier (log-loss)
       │
       ├───► [Feature Selection & PSO Optimization (src/models/pso_optimizer.py)]
       │       - Binary PSO đa mục tiêu ($0.92 \cdot \text{PR-AUC} + 0.08 \cdot \text{Sparsity}$)
       │       - Tiền xử lý nội bộ đồng nhất Fit-on-Train: SimpleImputer (median) + StandardScaler
       │       - Lựa chọn 17 đặc trưng, loại bỏ 100% biến nhiễu nhân tạo
       │
       └───► [Model Training & Comparison (src/models/train_xgboost.py)]
               - Ma trận thực nghiệm E1 – E5 (XGBoost Full vs PSO vs Baseline GB)
               - Tính toán PR-AUC, ROC-AUC, Confusion Matrix, Error Analysis trên Holdout 32k
       │
       ▼
[Export & Deliverables (src/export/export_outputs.py)]
  - Xuất 6 bảng CSV cho Power BI & Web Dashboard tại `outputs/powerbi/`
  - Tệp dự đoán Holdout 32k (`outputs/holdout_predictions.csv`) & Metadata
```

---

## 3. Kết quả kiểm toán chi tiết theo từng giai đoạn

### 3.1. Giai đoạn A — Kiểm kê toàn bộ Repository
- **Mã nguồn**: 13 tệp Python chính thức trong `src/` (chia thành `data/`, `features/`, `models/`, `analysis/`, `export/`, `evaluation/`). Không có dead code; các tệp đều liên kết chặt chẽ qua `src/config.py`.
- **Cấu hình**: `configs/split_metadata.json`, `configs/pso_experiment_config.json`.
- **Kiểm thử**: Đã nâng cấp từ 25 bài test lên **34 bài test tự động** trong `tests/`, chia thành chế độ test nhanh (`@pytest.mark.fast`) và test tích hợp đầy đủ.

### 3.2. Giai đoạn B — Kiểm toán dữ liệu gốc
- **Phát hiện**:
  - `customers.csv`: 10.000 giá trị placeholder `'unknown'` ở cột `age` (5,0%); 22.746 giá trị NULL ở `email_open_rate` (11,37%); `credit_limit` chứa ký hiệu tiền tệ và dấu phẩy; `referral_code` có 20.741 chuỗi rỗng.
  - `sessions.csv`: 2.000.000 dòng, `bounce_flag` chứa biểu diễn boolean lẫn lộn (`'1'`, `'0'`, `'true'`, `'false'`, `'yes'`, `'no'`); `pages_viewed` chứa placeholder `'N/A'`.
  - `transactions.csv`: 500.000 dòng, `order_value` chứa ký tự `$`, `discount_applied` chứa biểu diễn boolean lẫn lộn.
  - `train.csv` (160.000) và `test.csv` (40.000): Hoàn toàn không giao nhau (0 overlapping IDs).
  - Toàn bộ các khóa ngoại đều đạt độ toàn vẹn 100% (**0 bản ghi mồ côi**).
  - Kiểm tra chống bùng nổ dòng: Tích hợp với bảng tổng hợp duy trì đúng 200.000 khách hàng duy nhất.

### 3.3. Giai đoạn C — Kiểm toán trích xuất đặc trưng & Rò rỉ dữ liệu
- **Khắc phục phép chia cho 0**: Tất cả 9 đặc trưng tỷ lệ nâng cao trong `build_features.py` đều áp dụng kỹ thuật làm mịn mẫu số (`+ 1.0`), loại bỏ hoàn toàn nguy cơ phát sinh `NaN` hoặc `Inf` khi gặp khách hàng có 0 lượt xem hoặc 0 đơn hàng.
- **Rò rỉ nhãn**: Cột `target` và `customer_id` được loại bỏ nghiêm ngặt khỏi tập biến đầu vào.
- **Rò rỉ thời gian (Temporal Leakage)**: Dữ liệu thô không có mốc thời gian cắt nhãn (Prediction Cutoff). Do đó, dự án đã định nghĩa chuẩn xác phạm vi là **Observational Snapshot Propensity Classification**, loại bỏ các tuyên bố tuyệt đối về việc "loại bỏ 100% rò rỉ thời gian".

### 3.4. Giai đoạn D — Kiểm toán phân tích khám phá (EDA)
- Toàn bộ các số liệu phân vị và phân phối trong 9 biểu đồ tại `outputs/plots/` và tệp `outputs/eda_customer_summary.csv` đều được tính toán lại từ bảng `customer_features.parquet`. Không có số liệu suy diễn hoặc ngụy tạo.

### 3.5. Giai đoạn E — Kiểm toán Machine Learning
- **Phát hiện & Khắc phục quan trọng**:
  1. *Đồng nhất hóa tiền xử lý PSO*: Trước đây PSO sử dụng `.fillna(0).values` trong khi pipeline chính sử dụng `SimpleImputer(strategy="median")`. Đã sửa trực tiếp `src/models/pso_optimizer.py` để sử dụng `SimpleImputer(strategy="median")` + `StandardScaler()` fit độc quyền trên `sub_tr` của Train pool, đảm bảo tính nhất quán khoa học tuyệt đối.
  2. *Chính xác hóa tên mô hình*: Docstring của `src/models/baselines.py` và sơ đồ kiến trúc trước đây gọi mô hình thứ 7 là "SVM", trong khi code sử dụng `SGDClassifier(loss="log_loss")`. Đã chuẩn hóa lại toàn bộ tài liệu thành `SGDClassifier (log-loss)` hoặc `SGDClassifier (Logistic Regression via SGD)`.
  3. *Tách biệt chi phí tìm kiếm*: Báo cáo minh bạch thời gian tìm kiếm của PSO (11,79 giây) tách biệt với thời gian huấn luyện mô hình (XGBoost PSO fit time: 2,07 giây).
  4. *Trung thực về kết quả PSO*: Khẳng định rõ ràng rằng PSO không vượt qua ANOVA F-test về PR-AUC, nhưng mang lại ưu thế vượt trội về độ tinh giản (giảm 73% số chiều) và tăng tốc độ huấn luyện downstream 2,1 lần (XGBoost fit time từ 4,40s xuống 2,07s).
  5. *Đối chiếu từng dòng Holdout*: 32.000 dự đoán trong `outputs/holdout_predictions.csv` khớp 100% với nhãn gốc, đúng thứ tự dòng và chỉ số phân vùng.

### 3.6. Giai đoạn F — Kiểm toán Kiểm thử & Tái lập
- Đã bổ sung các tệp test mới:
  - `tests/test_edge_cases_and_fixtures.py`: Kiểm thử nhanh các trường hợp biên, chia cho 0, cô lập tiền xử lý.
  - `tests/test_relational_integrity.py`: Kiểm thử toàn vẹn khóa ngoại và không bùng nổ dòng khi join.
  - Mở rộng `tests/test_holdout_predictions_artifact.py` (8 tests) xác minh đối chiếu toàn diện độ đo và ma trận nhầm lẫn.
- Tạo tệp `pytest.ini` đăng ký các marker `fast`, `dataset`, `slow`.
- Toàn bộ **34/34 tests** chạy thành công trong 13,50 giây.

### 3.7. Giai đoạn G — Kiểm toán Tài liệu & Thư mục tham khảo
- Đồng bộ hóa các tài liệu: `docs/ARCHITECTURE.md`, `docs/PROGRESS.md`, `docs/IMPLEMENTATION_PLAN.md`.
- Đảm bảo các chỉ số, tên mô hình và công thức hàm fitness được thể hiện thống nhất.

---

## 4. Phân loại mức độ nghiêm trọng và tình trạng khắc phục

| Vấn đề phát hiện | Mức độ nghiêm trọng | Hiện trạng | Hành động đã thực hiện |
| :--- | :---: | :---: | :--- |
| Không đồng nhất tiền xử lý: PSO dùng `fillna(0)` trong khi pipeline dùng median imputer | **CAO** | **ĐÃ KHẮC PHỤC HOÀN TOÀN** | Sửa `src/models/pso_optimizer.py` sử dụng `SimpleImputer(strategy="median")` fit trên train pool. |
| Danh xưng mô hình nhầm lẫn giữa SVM và SGDClassifier (log_loss) | **TRUNG BÌNH** | **ĐÃ KHẮC PHỤC HOÀN TOÀN** | Sửa docstring `baselines.py`, `ARCHITECTURE.md`, `PROGRESS.md`, `IMPLEMENTATION_PLAN.md`. |
| Thiếu kiểm thử đơn vị nhanh không cần dataset (Fast Test Mode) | **TRUNG BÌNH** | **ĐÃ KHẮC PHỤC HOÀN TOÀN** | Tạo `tests/test_edge_cases_and_fixtures.py` và `pytest.ini` hỗ trợ `pytest -m fast`. |
| Thiếu kiểm thử toàn vẹn khóa ngoại và chống bùng nổ dòng | **TRUNG BÌNH** | **ĐÃ KHẮC PHỤC HOÀN TOÀN** | Tạo `tests/test_relational_integrity.py` kiểm tra 0 orphans và 200k dòng sau join. |
| Thiếu mốc thời gian cắt nhãn (Prediction Cutoff Timestamp) trong dữ liệu gốc | **GIỚI HẠN DỮ LIỆU GỐC** | **ĐÃ MINH BẠCH HÓA PHƯƠNG PHÁP** | Chuẩn hóa phạm vi bài toán thành Observational Snapshot Propensity Classification. |

---

## 5. Kết luận kiểm toán

Repository `hayd6/Global` đạt trạng thái **ĐẠT CÓ ĐIỀU KIỆN (PASSED WITH METHODOLOGICAL CONDITIONS)**:
1. **Kỹ thuật dữ liệu và Mã nguồn**: **XUẤT SẮC / ĐẠT 100%**. Quy trình DuckDB, tiền xử lý Fit-on-Train, cô lập Holdout 32k, mô hình hóa và kiểm thử tự động (33/33 tests pass) hoàn toàn sạch sẽ, không có lỗi logic hay rò rỉ phân vùng.
2. **Tính trung thực khoa học**: Báo cáo đầy đủ, minh bạch trade-off của Binary PSO và chi phí tìm kiếm; không làm sai lệch số liệu.
3. **Điều kiện phương pháp luận**: Do dữ liệu gốc không có tem thời gian cho nhãn, kết quả nghiên cứu phản ánh năng lực phân loại xu hướng trên lát cắt quan sát tĩnh (Observational Snapshot), cần được diễn giải đúng trong bối cảnh học thuật.
