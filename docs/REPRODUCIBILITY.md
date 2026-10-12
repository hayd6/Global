# HƯỚNG DẪN TÁI LẬP TOÀN BỘ DỰ ÁN (REPRODUCIBILITY GUIDE)

**Dự án**: Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử
**Mã nguồn**: `hayd6/Global`
**Ngày cập nhật**: 12/10/2026 | **Phiên bản**: v2.1-Audited

---

## 1. Yêu cầu môi trường (Environment Requirements)

- **Hệ điều hành**: Windows 10/11, Linux (Ubuntu 20.04+), hoặc macOS.
- **Phiên bản Python**: Python 3.10 trở lên (Môi trường kiểm chuẩn chính thức: **Python 3.14** trên Windows x64).
- **Phần cứng khuyến nghị**:
  - CPU: 4 cores trở lên (xử lý song song DuckDB và Scikit-Learn/XGBoost).
  - RAM: Tối thiểu 8 GB (kiến trúc DuckDB tận dụng stream dữ liệu, không ngốn RAM như Pandas thuần túy).
  - Ổ cứng: Trống tối thiểu 2 GB cho mã nguồn, dữ liệu nguồn và các artifact trung gian (`.parquet`, `.csv`).

---

## 2. Cài đặt môi trường từ một bản sao mới (Clean Clone Setup)

### Bước 2.1: Clone repository
```bash
git clone https://github.com/hayd6/Global.git
cd Global
```

### Bước 2.2: Khởi tạo môi trường ảo và cài đặt thư viện
```bash
python -m venv venv
# Trên Windows:
.\venv\Scripts\activate
# Trên Linux/macOS:
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

Các thư viện nòng cốt và phiên bản kiểm chuẩn:
- `duckdb >= 1.0.0`
- `scikit-learn >= 1.5.0`
- `xgboost >= 2.0.0`
- `pandas >= 2.2.0`
- `numpy >= 1.26.0`
- `matplotlib >= 3.8.0`
- `seaborn >= 0.13.0`
- `pytest >= 8.0.0`

---

## 3. Quản lý dữ liệu nguồn (Data Preparation)

Dự án yêu cầu 8 tệp CSV đặt trực tiếp trong thư mục `dataset/`:
1. `customers.csv` (200.000 dòng)
2. `geo_data.csv` (100 dòng)
3. `marketing_campaigns.csv` (200 dòng)
4. `sessions.csv` (2.000.000 dòng)
5. `transactions.csv` (500.000 dòng)
6. `train.csv` (160.000 dòng)
7. `test.csv` (40.000 dòng)
8. `sample_submission.csv` (40.000 dòng)

> **Lưu ý bảo vệ dữ liệu**: Thư mục `dataset/` là **READ-ONLY**. Không được sửa đổi, xóa hoặc ghi đè bất kỳ tệp nào trong thư mục này.

---

## 4. Chế độ kiểm thử nhanh không cần dữ liệu gốc (Fast Test Mode)

Để kiểm chứng tính toàn vẹn của mã nguồn và thuật toán trên máy trạm mới mà không cần nạp 2 triệu dòng dữ liệu thô:

```bash
pytest -m fast
```
Lệnh này sẽ thực thi các kiểm thử độc lập sử dụng fixture bộ nhớ trong mili-giây:
- Kiểm tra tính bất biến chia cho 0 (`test_division_by_zero_smoothing_invariants`).
- Kiểm tra tính cô lập của Preprocessor Fit-on-Train (`test_preprocessor_fit_on_train_isolation_with_synthetic_fixture`).
- Kiểm tra biên hàm thích nghi Binary PSO (`test_binary_pso_sparsity_penalty_boundary`).

---

## 5. Quy trình thực thi Pipeline hoàn chỉnh (Step-by-Step Execution)

Để tái lập toàn bộ kết quả từ dữ liệu thô đến mô hình và báo cáo, thực hiện tuần tự các lệnh sau:

### Bước 5.1: Kiểm toán dữ liệu nguồn và tính toàn vẹn khóa
```bash
python scratch/run_full_audit.py
```
*Đầu ra*: Báo cáo schema, tỷ lệ missing, tính toàn vẹn khóa ngoại (0 orphans), và xuất tệp `scratch/audit_summary.json`.

### Bước 5.2: Làm sạch và chuẩn hóa định dạng (DuckDB Views)
```bash
python -m src.data.clean_data
```
*Đầu ra*: Tạo các SQL Views chuẩn hóa: `v_cleaned_customers`, `v_cleaned_sessions`, `v_cleaned_transactions`, `v_cleaned_geo`, `v_cleaned_marketing`.

### Bước 5.3: Tích hợp đa bảng chống bùng nổ dòng (Data Integration)
```bash
python -m src.data.integrate_data
```
*Đầu ra*: `outputs/processed/clean_customer_features.parquet` (200.000 khách hàng duy nhất).

### Bước 5.4: Trích xuất đặc trưng nâng cao (Feature Engineering)
```bash
python -m src.features.build_features
```
*Đầu ra*:
- `outputs/customer_features.parquet` (72 cột, 200.000 dòng).
- `outputs/customer_features.csv`.
- `outputs/feature_dictionary.csv`.

### Bước 5.5: Phân tích khám phá dữ liệu (EDA & Biểu đồ)
```bash
python -m src.analysis.eda
```
*Đầu ra*: 9 biểu đồ phân tích chuyên sâu tại `outputs/plots/` và bảng tổng hợp `outputs/eda_customer_summary.csv`.

### Bước 5.6: Huấn luyện và đánh giá 7 mô hình cơ sở
```bash
python -m src.models.baselines
```
*Đầu ra*: `outputs/metrics/baseline_metrics.csv` (đầy đủ 9 chỉ số trên Holdout 32.000 dòng).

### Bước 5.7: Tối ưu hóa lựa chọn đặc trưng bằng Binary PSO
```bash
python -m src.models.pso_optimizer
```
*Đầu ra*:
- `outputs/feature_selection/pso_selected_features.csv` (17 đặc trưng được chọn).
- `outputs/feature_selection/pso_convergence.csv`.
- `outputs/plots/pso_convergence.png`.
- `configs/pso_experiment_config.json`.

### Bước 5.8: So sánh đối chứng 3 phương án lựa chọn đặc trưng (ANOVA vs PSO vs Full)
```bash
python -m src.models.feature_selection
```
*Đầu ra*: `outputs/metrics/feature_selection_comparison.csv`.

### Bước 5.9: Huấn luyện mô hình XGBoost & Xuất ma trận đánh giá
```bash
python -m src.models.train_xgboost
```
*Đầu ra*:
- `outputs/metrics/metrics_comparison.csv` (Ma trận so sánh E1–E5).
- `outputs/plots/roc_curve.png`, `precision_recall_curve.png`, `confusion_matrix.png`.
- `outputs/feature_selection/feature_importance.csv`.
- `outputs/test_predictions.csv` (Dự đoán trên 40.000 tập Test).

### Bước 5.10: Xuất bản dữ liệu cho Power BI và Web
```bash
python -m src.export.export_outputs
```
*Đầu ra*: 6 tệp CSV chuẩn hóa trong thư mục `outputs/powerbi/`.

---

## 6. Chạy toàn bộ bộ kiểm thử tự động (Full Test Suite)

Sau khi hoàn thành pipeline, chạy toàn bộ bộ kiểm thử tích hợp:
```bash
pytest -v
```
**Tiêu chuẩn chấp nhận (Acceptance Criteria)**:
- Toàn bộ **34/34 tests** phải đạt trạng thái `PASSED`.
- Thời gian thực thi toàn bộ test suite: dưới 15 giây.
- Bao gồm:
  - 4 bài kiểm thử dữ liệu thô (`test_data_audit.py`).
  - 4 bài kiểm thử liên kết quan hệ và khóa ngoại (`test_relational_integrity.py`).
  - 2 bài kiểm thử làm sạch và tích hợp (`test_cleaning_integration.py`).
  - 2 bài kiểm thử đặc trưng và từ điển (`test_feature_engineering.py`).
  - 8 bài kiểm thử artifact Holdout 32k (`test_holdout_predictions_artifact.py`).
  - 14 bài kiểm thử mô hình và thuật toán PSO (`test_models_and_pso.py`, `test_edge_cases_and_fixtures.py`).
