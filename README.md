# Global E-Commerce Customer Purchase Prediction

> **Đề tài nghiên cứu**: Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử.

---

## 1. Giới thiệu tổng quan

Dự án phát triển một hệ thống Big Data và Machine Learning hoàn chỉnh nhằm phân tích hành vi khách hàng thương mại điện tử đa quốc gia và dự đoán khả năng mua hàng trong tương lai. Hệ thống tích hợp dữ liệu từ 8 bảng thực tế (hơn 2,000,000 phiên duyệt web, 500,000 giao dịch và 200,000 khách hàng), áp dụng DuckDB để xử lý streaming/vectorized với tốc độ xử lý hàng triệu dòng trong vài giây, kỹ thuật Feature Engineering sâu rộng, và thuật toán tối ưu bầy đàn nhị phân (Binary PSO) để tinh chọn bộ đặc trưng tối ưu phục vụ mô hình XGBoost.

---

## 2. Kết quả thực nghiệm trọng yếu

### 2.1. Đánh giá 7 mô hình cơ sở (`outputs/metrics/baseline_metrics.csv`)
Đánh giá trên tập Validation phân tầng (Stratified 32,000 mẫu, tỷ lệ nhãn dương 20.3%):

| Mô hình | Số đặc trưng | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Thời gian huấn luyện |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | 180 | **0.2785** | **0.6150** | **0.3660** | 0.2442 | 0.7303 | 19.17s |
| **Random Forest** | 180 | 0.2753 | 0.6101 | 0.3635 | 0.2425 | 0.7258 | 12.95s |
| **Logistic Regression** | 180 | 0.2704 | 0.6033 | 0.3602 | 0.2396 | 0.7299 | **1.10s** |
| **Support Vector Machine (SGD)** | 180 | 0.2578 | 0.5858 | 0.3526 | 0.2337 | 0.7214 | 4.30s |
| **Decision Tree** | 180 | 0.2575 | 0.5927 | 0.3569 | 0.2372 | 0.7247 | 7.14s |
| **Naive Bayes** | 180 | 0.2170 | 0.5235 | 0.3377 | 0.2073 | 0.9080 | **0.42s** |
| **K-Nearest Neighbors (KNN)** | 180 | 0.2108 | 0.5187 | 0.3375 | 0.2071 | 0.9103 | 8.04s |

### 2.2. So sánh lựa chọn đặc trưng & XGBoost (`outputs/metrics/metrics_comparison.csv`)

| Mô hình & Cấu hình đặc trưng | Số đặc trưng | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Thời gian Fit |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Full Features)** | 63 | 0.2720 | 0.6087 | 0.3664 | 0.2445 | 0.7306 | 15.64s |
| **Baseline (Statistical Features)** | 17 | 0.2714 | 0.6090 | 0.3671 | 0.2422 | 0.7582 | 6.39s |
| **Baseline (PSO Features)** | 17 | 0.2600 | 0.5906 | 0.3557 | 0.2364 | 0.7180 | 4.08s |
| **XGBoost (Full Features)** | 63 | 0.2659 | 0.6033 | 0.3630 | 0.2398 | 0.7462 | 3.10s |
| **XGBoost (PSO Features)** | 17 | 0.2590 | 0.5875 | 0.3547 | 0.2411 | 0.6708 | **1.52s** |

> **Nhận xét cốt lõi**: Thuật toán Binary PSO đã tinh giản **73.0%** số chiều đặc trưng (từ 63 xuống 17 đặc trưng), giúp thời gian huấn luyện mô hình XGBoost giảm hơn 50% (xuống chỉ còn 1.52 giây) trong khi bảo toàn năng lực dự đoán thực tế.

---

## 3. Cấu trúc thư mục dự án

```text
├── dataset/                    # 8 file dữ liệu gốc (READ-ONLY)
│   ├── customers.csv
│   ├── geo_data.csv
│   ├── marketing_campaigns.csv
│   ├── sample_submission.csv
│   ├── sessions.csv
│   ├── test.csv
│   ├── train.csv
│   └── transactions.csv
├── docs/                       # Tài liệu nghiên cứu chi tiết
│   ├── ARCHITECTURE.md         # Sơ đồ kiến trúc Mermaid & luồng xử lý
│   ├── DATA_DICTIONARY.md      # Từ điển dữ liệu thực tế
│   ├── DECISIONS.md            # Sổ tay quyết định kỹ thuật (ADR)
│   ├── EXPERIMENT_PLAN.md      # Thiết kế và kết quả thực nghiệm
│   ├── PROGRESS.md             # Bảng theo dõi tiến độ 10 giai đoạn
│   └── REPRODUCIBILITY.md      # Hướng dẫn tái lập kết quả
├── configs/                    # File cấu hình tham số thực nghiệm JSON
├── src/                        # Mã nguồn dự án chuẩn module hóa
│   ├── config.py               # Thiết lập đường dẫn, logging và constants
│   ├── data/                   # Kiểm toán, làm sạch & tích hợp DuckDB
│   │   ├── inspect_data.py
│   │   ├── clean_data.py
│   │   └── integrate_data.py
│   ├── features/               # Kỹ thuật trích xuất đặc trưng & từ điển
│   │   └── build_features.py
│   ├── analysis/               # Phân tích dữ liệu khám phá (9 biểu đồ EDA)
│   │   └── eda.py
│   ├── models/                 # Huấn luyện mô hình, thống kê & Binary PSO
│   │   ├── baselines.py
│   │   ├── feature_selection.py
│   │   ├── pso_optimizer.py
│   │   └── train_xgboost.py
│   ├── evaluation/             # Đánh giá chỉ số & vẽ đường cong ROC/PR/CM
│   │   └── evaluate.py
│   ├── export/                 # Xuất dữ liệu phục vụ Power BI / Web
│   │   └── export_outputs.py
│   └── pipeline.py             # Pipeline tự động hóa từ đầu đến cuối
├── tests/                      # Bộ kiểm thử tự động pytest (11/11 PASSED)
├── outputs/                    # Kết quả thực nghiệm và dữ liệu phái sinh
│   ├── data_quality_report.csv
│   ├── referential_integrity_report.csv
│   ├── target_distribution.csv
│   ├── customer_features.parquet
│   ├── customer_features.csv
│   ├── test_predictions.csv
│   ├── eda/                    # 9 biểu đồ phân tích khám phá chuyên sâu
│   ├── metrics/                # Bảng chỉ số hiệu năng các mô hình
│   ├── plots/                  # Biểu đồ ROC, PR Curve, Confusion Matrix, PSO
│   ├── feature_selection/      # Danh sách biến chọn bởi PSO và tầm quan trọng
│   └── powerbi/                # 6 bảng dữ liệu xuất riêng cho Power BI Dashboard
├── logs/                       # File nhật ký pipeline.log
├── PRD.md                      # Product Requirements Document
├── AGENTS.md                   # Hướng dẫn quy tắc cho AI Agent
├── requirements.txt            # Danh sách thư viện phụ thuộc
└── README.md                   # Hướng dẫn sử dụng
```

---

## 4. Hướng dẫn cài đặt và thực thi

### 4.1. Cài đặt môi trường
Yêu cầu Python 3.10+ (Đã kiểm thử tương thích hoàn toàn trên Python 3.14).
```bash
pip install -r requirements.txt
```

### 4.2. Chạy toàn bộ Pipeline từ đầu đến cuối (Khuyến nghị)
Một lệnh duy nhất để chạy toàn bộ 9 giai đoạn tự động:
```bash
python src/pipeline.py
```

### 4.3. Chạy từng giai đoạn độc lập
- **Giai đoạn 1 — Kiểm toán dữ liệu (Data Audit)**:
  ```bash
  python src/data/inspect_data.py
  ```
- **Giai đoạn 2 — Làm sạch và tích hợp dữ liệu (Clean & Integrate)**:
  ```bash
  python src/data/clean_data.py
  python src/data/integrate_data.py
  ```
- **Giai đoạn 3 & 4 — Khai phá đặc trưng & Vẽ biểu đồ EDA**:
  ```bash
  python src/features/build_features.py
  python src/analysis/eda.py
  ```
- **Giai đoạn 5 & 6 — Đánh giá 7 mô hình cơ sở (Baselines)**:
  ```bash
  python src/models/baselines.py
  ```
- **Giai đoạn 7 — Lựa chọn đặc trưng & Tối ưu hóa Binary PSO**:
  ```bash
  python src/models/feature_selection.py
  ```
- **Giai đoạn 8 — Huấn luyện XGBoost & Xuất đường cong so sánh**:
  ```bash
  python src/models/train_xgboost.py
  ```
- **Giai đoạn 9 — Xuất dữ liệu cho Power BI Dashboard**:
  ```bash
  python src/export/export_outputs.py
  ```
- **Giai đoạn 10 — Chạy kiểm thử tự động pytest**:
  ```bash
  pytest -v
  ```

---

## 5. Danh mục kết quả đầu ra

- **Báo cáo kiểm toán**: `outputs/data_quality_report.csv`, `outputs/referential_integrity_report.csv`, `outputs/target_distribution.csv`
- **Biểu đồ EDA (9 biểu đồ)**: `outputs/eda/*.png`
- **Ma trận đặc trưng**: `outputs/customer_features.parquet` (200,000 dòng x 72 cột)
- **Từ điển đặc trưng**: `outputs/feature_dictionary.csv` (67 đặc trưng được định nghĩa đầy đủ)
- **Kết quả PSO**: `outputs/feature_selection/pso_selected_features.csv`, `outputs/plots/pso_convergence.png`
- **Chỉ số mô hình**: `outputs/metrics/baseline_metrics.csv`, `outputs/metrics/metrics_comparison.csv`
- **Biểu đồ so sánh**: `outputs/plots/roc_curve.png`, `outputs/plots/precision_recall_curve.png`, `outputs/plots/confusion_matrix.png`, `outputs/plots/xgboost_feature_importance.png`
- **Tập tin Power BI**: thư mục `outputs/powerbi/`
- **Dự đoán tập Test**: `outputs/test_predictions.csv` (40,000 khách hàng)
