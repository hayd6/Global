# Global E-Commerce Customer Purchase Prediction

> **Đề tài nghiên cứu**: Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử.

---

## 1. Giới thiệu tổng quan

Dự án phát triển một hệ thống Big Data và Machine Learning hoàn chỉnh nhằm phân tích hành vi khách hàng thương mại điện tử đa quốc gia và dự đoán khả năng mua hàng trong tương lai. Hệ thống tích hợp dữ liệu từ 8 bảng thực tế (hơn 2,000,000 phiên duyệt web, 500,000 giao dịch và 200,000 khách hàng), áp dụng DuckDB để xử lý streaming/vectorized với tốc độ xử lý hàng triệu dòng trong vài giây, kỹ thuật Feature Engineering sâu rộng, và thuật toán tối ưu bầy đàn nhị phân (Binary PSO) để tinh chọn bộ đặc trưng tối ưu phục vụ mô hình XGBoost.

---

## 2. Kết quả thực nghiệm trọng yếu

### 2.1. Đánh giá 7 mô hình cơ sở (`outputs/metrics/baseline_metrics.csv`)
Đánh giá trên tập Holdout phân tầng chuẩn hóa (`split_id: stratified_80_20_v1`, 32,000 khách hàng độc lập, tỷ lệ nhãn dương 20.31%, ngưỡng cố định 0.5):

| Mô hình | Số đặc trưng | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Thời gian Fit |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | 180 | **0.2758** | **0.6097** | **0.3575** | 0.2570 | 0.5873 | 34.85s |
| **Random Forest** | 180 | 0.2700 | 0.6031 | 0.3488 | 0.2589 | 0.5346 | 29.80s |
| **Logistic Regression** | 180 | 0.2649 | 0.5989 | 0.3473 | 0.2529 | 0.5541 | **1.49s** |
| **Decision Tree** | 180 | 0.2584 | 0.5851 | 0.3446 | 0.2468 | 0.5710 | 10.23s |
| **SGDClassifier (log_loss)** | 180 | 0.2456 | 0.5748 | 0.3357 | 0.2404 | 0.5563 | 6.66s |
| **Naive Bayes** | 180 | 0.2161 | 0.5177 | 0.2825 | 0.2171 | 0.4040 | **0.57s** |
| **K-Nearest Neighbors (KNN)** | 180 | 0.2102 | 0.5167 | 0.0685 | 0.2231 | 0.0405 | 17.10s |

### 2.2. So sánh lựa chọn đặc trưng & XGBoost (`outputs/metrics/metrics_comparison.csv`)
Đánh giá so sánh trực tiếp trên cùng tập Holdout 32,000 khách hàng độc lập (ngưỡng 0.5):

| Mô hình & Cấu hình đặc trưng | Số đặc trưng | PR-AUC | ROC-AUC | F1-Score | Fit Time | Search Cost | Total Time |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Full Features)** | 63 | 0.2730 | 0.6078 | 0.3558 | 16.96s | 0.00s | 16.96s |
| **Baseline (Statistical Features)** | 17 | **0.2759** | **0.6105** | 0.3557 | 6.35s | 0.13s | **6.48s** |
| **Baseline (PSO Features)** | 17 | 0.2601 | 0.5894 | 0.3411 | 4.52s | 11.79s | 16.31s |
| **XGBoost (Full Features)** | 63 | 0.2654 | 0.6006 | 0.3475 | 4.65s | 0.00s | 4.65s |
| **XGBoost (PSO Features)** | 17 | 0.2584 | 0.5846 | 0.3319 | **2.22s** | 11.79s | 14.01s |

> **Phân tích đánh đổi khách quan (Trade-off Analysis)**:
> 1. **Mức độ tinh giản chiều (Feature Sparsity)**: Thuật toán Binary PSO giảm thành công **73.02%** số chiều đặc trưng (từ 63 xuống 17 đặc trưng), giúp rút ngắn thời gian huấn luyện mô hình hạ nguồn đáng kể (Fit time của Baseline giảm từ 16.96s xuống 4.52s; XGBoost giảm từ 4.65s xuống 2.22s - nhanh hơn 2.1x).
> 2. **Chi phí tìm kiếm (Search Overhead)**: Quá trình tìm kiếm của bầy đàn (16 hạt x 12 vòng lặp) trên phân vùng inner tuning tiêu tốn 11.79s (tính toán 208 mặt nạ nhị phân).
> 3. **Hiệu năng phân loại (Performance Trade-off)**: Trên tập Holdout 32k độc lập chưa từng tham gia tìm kiếm, PSO chấp nhận đánh đổi một phần khả năng phân biệt (-0.0129 PR-AUC so với Baseline Full; -0.0070 PR-AUC so với XGBoost Full). Chọn lọc thống kê ANOVA F-score (k=17) đạt PR-AUC 0.2759 với chi phí tìm kiếm gần như tức thì (0.13s).

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
├── docs/                       # Tài liệu nghiên cứu và báo cáo kiểm toán chi tiết
│   ├── FULL_REPOSITORY_AUDIT.md# Báo cáo kiểm toán toàn diện repository
│   ├── DATA_QUALITY_REPORT.md  # Báo cáo kiểm toán chất lượng dữ liệu nguồn
│   ├── FEATURE_AUDIT.md        # Báo cáo kiểm toán 72 đặc trưng & rò rỉ dữ liệu
│   ├── ML_VALIDATION_REPORT.md # Báo cáo thẩm định mô hình ML & Holdout 32k
│   ├── REPRODUCIBILITY.md      # Hướng dẫn tái lập dự án từ clean clone
│   ├── FINAL_REMEDIATION_REPORT.md # Tổng kết đợt khắc phục lỗi One-Pass
│   ├── ARCHITECTURE.md         # Sơ đồ kiến trúc Mermaid & luồng xử lý
│   ├── DECISIONS.md            # Sổ tay quyết định kỹ thuật (ADR)
│   ├── EXPERIMENT_PLAN.md      # Thiết kế và kết quả thực nghiệm
│   └── PROGRESS.md             # Bảng theo dõi tiến độ các giai đoạn
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
├── tests/                      # Bộ kiểm thử tự động pytest (38/38 PASSED)
├── web/                        # Cổng thông tin nghiên cứu web 6 trang + Demo dự đoán
├── scripts/                    # Scripts xuất bản báo cáo Word .docx và Markdown
├── docs/                       # Toàn văn báo cáo khoa học 6 phần, đặc tả Power BI, kiểm toán
│   ├── BaoCao_NghienCuu_Global_6Phan.docx # Luận văn hoàn chỉnh dạng Word
│   ├── BaoCao_NghienCuu_Global_6Phan.md   # Luận văn hoàn chỉnh dạng Markdown
│   ├── FINAL_PROJECT_ACCEPTANCE.md        # Báo cáo nghiệm thu dự án tổng thể
│   ├── FINAL_ACCEPTANCE_MATRIX.md         # Ma trận nghiệm thu 45 tiểu mục DanY6Phan
│   └── POWER_BI_SPECIFICATION.md          # Đặc tả 4 trang Power BI & công thức DAX
├── outputs/                    # Kết quả thực nghiệm và dữ liệu phái sinh
│   ├── data_quality_report.csv
│   ├── referential_integrity_report.csv
│   ├── target_distribution.csv
│   ├── customer_features.parquet
│   ├── customer_features.csv
│   ├── holdout_predictions.csv
│   ├── holdout_prediction_metadata.json
│   ├── test_predictions.csv
│   ├── eda/                    # 12 biểu đồ phân tích khám phá chuyên sâu
│   ├── metrics/                # Bảng chỉ số hiệu năng các mô hình
│   ├── plots/                  # Biểu đồ ROC, PR Curve, Confusion Matrix, PSO
│   ├── feature_selection/      # Danh sách biến chọn bởi PSO và tầm quan trọng
│   └── powerbi/                # 6 bảng dữ liệu xuất riêng cho Power BI Dashboard
├── logs/                       # File nhật ký pipeline.log
├── PRD.md                      # Product Requirements Document
├── AGENTS.md                   # Hướng dẫn quy tắc cho AI Agent
├── DanY6Phan.md                # Chuẩn yêu cầu và dàn ý phân công 6 phần
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
  # Chế độ kiểm thử nhanh với fixture (không cần dataset):
  pytest -m fast

  # Chế độ kiểm thử toàn diện toàn bộ 38 bài test:
  pytest -v
  ```
- **Giai đoạn 11 — Khởi chạy Cổng thông tin Nghiên cứu Web (6 trang)**:
  ```bash
  python -m http.server 3000 --directory web
  # Mở trình duyệt tại: http://localhost:3000
  ```
- **Giai đoạn 12 — Xuất bản lại Luận văn Word (.docx) & Markdown (.md)**:
  ```bash
  python scripts/build_full_report.py
  ```

---

## 5. Danh mục kết quả đầu ra

- **Báo cáo nghiên cứu học thuật hoàn chỉnh (6 phần)**:
  - `docs/BaoCao_NghienCuu_Global_6Phan.docx` (Bản Word chính thức)
  - `docs/BaoCao_NghienCuu_Global_6Phan.md` (Bản Markdown đầy đủ 54k từ)
  - `docs/FINAL_PROJECT_ACCEPTANCE.md` (Báo cáo nghiệm thu dự án tổng thể)
  - `docs/FINAL_ACCEPTANCE_MATRIX.md` (Ma trận nghiệm thu 45 tiểu mục)
- **Cổng thông tin Web**: thư mục `web/` (6 trang độc lập + Prediction Demo)
- **Đặc tả Power BI**: `docs/POWER_BI_SPECIFICATION.md` & `outputs/powerbi/` (6 bảng CSV)
- **Báo cáo kiểm toán dữ liệu**: `outputs/data_quality_report.csv`, `outputs/referential_integrity_report.csv`, `outputs/target_distribution.csv`
- **Biểu đồ EDA (12 biểu đồ)**: `outputs/eda/*.png`
- **Ma trận đặc trưng**: `outputs/customer_features.parquet` (200,000 dòng x 72 cột)
- **Từ điển đặc trưng**: `outputs/feature_dictionary.csv` (63 đặc trưng số + biến phân loại)
- **Artifact kiểm định Holdout**: `outputs/holdout_predictions.csv` & `outputs/holdout_prediction_metadata.json` (32,000 mẫu)
- **Kết quả PSO**: `outputs/feature_selection/pso_selected_features.csv`, `outputs/plots/pso_convergence.png`
- **Chỉ số mô hình**: `outputs/metrics/baseline_metrics.csv`, `outputs/metrics/metrics_comparison.csv`
- **Biểu đồ so sánh**: `outputs/plots/roc_curve.png`, `outputs/plots/precision_recall_curve.png`, `outputs/plots/confusion_matrix.png`, `outputs/plots/xgboost_feature_importance.png`
- **Tập tin Power BI**: thư mục `outputs/powerbi/`
- **Dự đoán tập Test**: `outputs/test_predictions.csv` (40,000 khách hàng)
