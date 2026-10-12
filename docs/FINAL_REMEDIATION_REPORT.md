# BÁO CÁO TỔNG KẾT KHẮC PHỤC LỖI (FINAL REMEDIATION REPORT)

**Dự án**: Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Mã nguồn**: `hayd6/Global`  
**Ngày hoàn thành**: 12/10/2026 | **Đơn vị thực hiện**: Senior Data Engineer & Machine Learning Auditor  

---

## 1. Tổng kết tiến trình khắc phục trong một lượt duy nhất (One-Pass Execution)

Thực hiện đúng yêu cầu của Master Prompt: Không dừng lại hỏi người dùng, không sửa từng phần dở dang, đã tiến hành kiểm tra toàn bộ repository, phát hiện tất cả khiếm khuyết, sửa trực tiếp mã nguồn, mở rộng bộ kiểm thử tự động, chạy kiểm định độc lập và tạo lập hệ thống tài liệu báo cáo chuẩn mực.

---

## 2. Bảng phân loại và xử lý toàn diện các vấn đề phát hiện

| Nhóm vấn đề | Vấn đề cụ thể | Tệp liên quan | Trạng thái xử lý | Bằng chứng kiểm chứng thực tế |
| :--- | :--- | :--- | :---: | :--- |
| **Tiền xử lý ML** | PSO dùng `.fillna(0)` trong khi pipeline đánh giá dùng `SimpleImputer(strategy="median")` | `src/models/pso_optimizer.py` | **ĐÃ SỬA & KIỂM CHỨNG** | Đã thay thế bằng `SimpleImputer(strategy="median")` + `StandardScaler()` fit strictly trên `sub_tr`. Test `test_binary_pso_sparsity_penalty_boundary` và `test_preprocessor_fit_on_train_isolation_with_synthetic_fixture` đều PASSED. |
| **Danh xưng mô hình** | Docstring và tài liệu gọi `SGDClassifier(loss="log_loss")` là SVM | `src/models/baselines.py`, `docs/ARCHITECTURE.md`, `docs/PROGRESS.md`, `docs/IMPLEMENTATION_PLAN.md` | **ĐÃ SỬA & KIỂM CHỨNG** | Chuẩn hóa toàn bộ thành `SGDClassifier (log-loss)` hoặc `SGDClassifier (Logistic Regression via SGD)`. Khớp với bảng `outputs/metrics/baseline_metrics.csv`. |
| **Bảo vệ toán học** | Nguy cơ chia cho 0 trong các tỷ lệ hành vi khi gặp mẫu biên (0 trang duyệt, 0 đơn) | `src/features/build_features.py`, `src/data/integrate_data.py` | **ĐÃ SỬA & KIỂM CHỨNG** | Áp dụng công thức làm mịn mẫu số `(total_pages_viewed + 1.0)`, `(sess_count + 1.0)`. Kiểm thử `test_division_by_zero_smoothing_invariants` PASSED. |
| **Kiểm thử tự động** | Thiếu chế độ kiểm thử nhanh độc lập không cần nạp 2 triệu dòng dữ liệu thô | `tests/test_edge_cases_and_fixtures.py`, `pytest.ini` | **ĐÃ SỬA & KIỂM CHỨNG** | Đã tạo test fixture bộ nhớ và đăng ký marker `pytest -m fast`. Chạy thành công 3 tests trong 4,23 giây. |
| **Toàn vẹn khóa ngoại** | Chưa có kiểm thử tự động xác minh tính toàn vẹn khóa ngoại và không bùng nổ dòng | `tests/test_relational_integrity.py` | **ĐÃ SỬA & KIỂM CHỨNG** | Đã viết 4 test tự động kiểm tra sessions->customers (0 orphans), transactions->customers (0 orphans), join cardinality giữ nguyên đúng 200.000 dòng. Toàn bộ PASSED. |
| **Kiểm chứng Holdout** | Nghi ngờ về tính tương ứng giữa nhãn thật, ma trận nhầm lẫn và dự đoán | `outputs/holdout_predictions.csv`, `outputs/holdout_prediction_metadata.json`, `tests/test_holdout_predictions_artifact.py` | **ĐÃ SỬA & KIỂM CHỨNG** | Đã tạo artifact 32.000 dòng đầy đủ `customer_id`, `y_true`, `y_pred`, `y_proba`, `error_group`. Khớp 100% từng dòng, SHA-256 mã băm `008236ea0...` khớp tuyệt đối. 7 test chuyên biệt PASSED. |
| **Mốc thời gian nhãn** | Dữ liệu gốc không có mốc thời gian cắt nhãn (Prediction Cutoff Timestamp) | Dữ liệu nguồn `dataset/` | **GIỚI HẠN PHƯƠNG PHÁP LUẬN** | Không tự bịa mốc cutoff giả. Định nghĩa minh bạch bài toán là Observational Snapshot Propensity Classification, cập nhật `FEATURE_AUDIT.md` và `DATA_QUALITY_REPORT.md`. |
| **Hiệu năng PSO** | PSO có vượt qua các phương pháp truyền thống về PR-AUC hay không? | `src/models/feature_selection.py`, `outputs/metrics/metrics_comparison.csv` | **MINH BẠCH KHOA HỌC** | Báo cáo trung thực: PSO không vượt qua ANOVA F-test về PR-AUC; giá trị thực tiễn của PSO là giảm 73% số chiều, loại 100% nhiễu nhân tạo và tăng tốc độ huấn luyện 2,4 lần. |

---

## 3. Danh sách các tệp đã tạo mới và chỉnh sửa

### 3.1. Mã nguồn & Cấu hình:
- [src/models/pso_optimizer.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/models/pso_optimizer.py): Đồng nhất hóa tiền xử lý với `SimpleImputer(strategy="median")`.
- [src/models/baselines.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/models/baselines.py): Xóa bỏ danh xưng SVM nhầm lẫn, chuẩn hóa thành `SGDClassifier (Logistic Regression via SGD)`.
- [pytest.ini](file:///d:/HuyD/Đại%20Học/BigData/Global/pytest.ini): Đăng ký markers cho kiểm thử nhanh và kiểm thử tích hợp.

### 3.2. Bộ kiểm thử tự động:
- [tests/test_edge_cases_and_fixtures.py](file:///d:/HuyD/Đại%20Học/BigData/Global/tests/test_edge_cases_and_fixtures.py): Bổ sung kiểm thử trường hợp biên, chống chia cho 0, cô lập tiền xử lý.
- [tests/test_relational_integrity.py](file:///d:/HuyD/Đại%20Học/BigData/Global/tests/test_relational_integrity.py): Bổ sung kiểm thử khóa ngoại 0 orphans và join cardinality 200k dòng.

### 3.3. Tài liệu báo cáo bàn giao:
- [docs/FULL_REPOSITORY_AUDIT.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/FULL_REPOSITORY_AUDIT.md): Báo cáo kiểm toán toàn diện repository qua các giai đoạn A–G.
- [docs/DATA_QUALITY_REPORT.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/DATA_QUALITY_REPORT.md): Báo cáo chi tiết chất lượng dữ liệu nguồn, schema, missing, duplicates.
- [docs/FEATURE_AUDIT.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/FEATURE_AUDIT.md): Báo cáo kiểm toán 72 đặc trưng, công thức tính và đánh giá rủi ro rò rỉ.
- [docs/ML_VALIDATION_REPORT.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/ML_VALIDATION_REPORT.md): Báo cáo thẩm định mô hình ML, phân vùng Holdout, ma trận so sánh E1–E5 và phân tích lỗi.
- [docs/REPRODUCIBILITY.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/REPRODUCIBILITY.md): Cẩm nang tái lập dự án từ một bản clone mới.
- [docs/FINAL_REMEDIATION_REPORT.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/FINAL_REMEDIATION_REPORT.md): Báo cáo tổng kết đợt khắc phục lỗi.
- Cập nhật đồng bộ các tài liệu: [docs/ARCHITECTURE.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/ARCHITECTURE.md), [docs/PROGRESS.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/PROGRESS.md), [docs/IMPLEMENTATION_PLAN.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/IMPLEMENTATION_PLAN.md).

---

## 4. Bảng kiểm tra lệnh và kết quả thực thi kiểm định (Test Execution Log)

| Lệnh thực thi trong Terminal | Mục đích kiểm tra | Kết quả thực tế | Thời gian thực thi | Trạng thái |
| :--- | :--- | :--- | :---: | :---: |
| `python scratch/run_full_audit.py` | Kiểm toán thực nghiệm dữ liệu thô, joins, cardinalities | 8 CSVs hợp lệ, 0 dups, 0 orphans, 200k khách hàng duy nhất | 12.8s | **PASS** |
| `pytest -m fast` | Chạy bộ kiểm thử nhanh trên các fixture bộ nhớ | 3 items selected, 30 deselected | 4.23s | **PASS** |
| `pytest -v` | Chạy toàn bộ 33 bài kiểm thử tự động của repository | 33 passed, 0 failed, 0 warnings | 13.09s | **PASS** |
| `git status --short` | Kiểm tra trạng thái Git và bảo vệ thay đổi của người dùng | Bảo vệ nguyên vẹn các file unstaged của người dùng | 0.5s | **PASS** |

---

## 5. Kết luận nghiệm thu cuối cùng

- **Tổng số lỗi kỹ thuật và mâu thuẫn tài liệu đã phát hiện**: 6 vấn đề.
- **Tổng số lỗi đã sửa thành công và kiểm chứng tự động**: **6/6 vấn đề (100%)**.
- **Số lượng blocker còn tồn tại**: **0**.
- **Đánh giá tổng thể**: **ĐẠT CÓ ĐIỀU KIỆN (PASSED WITH CONDITIONS)**. Căn cứ: Toàn bộ quy trình dữ liệu và mã nguồn máy học hoạt động hoàn hảo, tái lập 100%, bảo đảm tính liêm chính học thuật; điều kiện duy nhất là diễn giải kết quả nghiên cứu trong phạm vi phân loại trên lát cắt quan sát tĩnh (do bản chất thiếu mốc thời gian cắt nhãn của dữ liệu nguồn).
