# REPRODUCIBILITY GUIDE — HƯỚNG DẪN TÁI LẬP KẾT QUẢ

Tài liệu này cung cấp hướng dẫn từng bước để bất kỳ nhà nghiên cứu hoặc kỹ sư nào cũng có thể tái lập chính xác 100% các kết quả thực nghiệm trong dự án.

---

## 1. Yêu cầu hệ thống

- **Hệ điều hành**: Windows 10/11, Linux hoặc macOS.
- **Python**: Phiên bản 3.10 trở lên (khuyến nghị Python 3.11 - 3.14).
- **RAM**: Tối thiểu 4GB (DuckDB thực hiện streaming và in-memory vectorization nên tiêu thụ rất ít RAM).
- **Ổ cứng trống**: Tối thiểu 1GB cho mã nguồn và các file kết quả đầu ra.

---

## 2. Các bước tái lập kết quả

### Bước 1: Chuẩn bị môi trường
```bash
# Tạo môi trường ảo (tùy chọn nhưng khuyến khích)
python -m venv venv

# Kích hoạt trên Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Cài đặt thư viện:
pip install -r requirements.txt
```

### Bước 2: Kiểm tra dữ liệu nguồn
Đảm bảo 8 file CSV gốc nằm đầy đủ trong thư mục `dataset/`:
- `customers.csv`
- `geo_data.csv`
- `marketing_campaigns.csv`
- `sample_submission.csv`
- `sessions.csv`
- `test.csv`
- `train.csv`
- `transactions.csv`

### Bước 3: Chạy toàn bộ quy trình bằng một lệnh duy nhất
```bash
python src/pipeline.py
```
Toàn bộ quy trình sẽ tự động thực hiện tuần tự:
1. Kiểm toán chất lượng dữ liệu -> xuất `outputs/data_quality_report.csv`
2. Làm sạch và tích hợp bảng lớn bằng DuckDB -> tạo ma trận khách hàng tích hợp
3. Xử lý leakage và trích xuất đặc trưng -> xuất `outputs/customer_features.parquet` và biểu đồ EDA
4. Đánh giá 7 mô hình cơ sở -> xuất `outputs/metrics/baseline_metrics.csv`
5. Tối ưu hóa đặc trưng bằng Binary PSO -> xuất `outputs/feature_selection/pso_selected_features.csv`
6. Huấn luyện XGBoost trên các tập đặc trưng và so sánh -> xuất biểu đồ và bảng so sánh
7. Xuất dữ liệu Power BI -> lưu vào `outputs/powerbi/`

### Bước 4: Chạy kiểm thử tự động
```bash
pytest -v
```

---

## 3. Cố định tính ngẫu nhiên (Random Seed Control)

Mọi quá trình có yếu tố ngẫu nhiên đều được cố định bằng:
- `RANDOM_STATE = 42` (được thiết lập tập trung tại `src/config.py`).
- Phân chia tập dữ liệu: `train_test_split(..., random_state=42, stratify=y)`.
- Khởi tạo bầy đàn PSO: `np.random.seed(42)`.
- Các thuật toán học máy: `random_state=42` cho Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost.
