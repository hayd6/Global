# EXPERIMENT PLAN & EMPIRICAL FINDINGS

Tài liệu này tổng hợp thiết kế thực nghiệm và **kết quả thực nghiệm thực tế** thu được từ quy trình kiểm thử khoa học trên tập dữ liệu 200,000 khách hàng thương mại điện tử với tập Holdout độc lập (32,000 khách hàng, Stratified split 80/20, `random_state=42`).

---

## 1. Kiểm định các giả thuyết nghiên cứu (Hypotheses Verification)

| Giả thuyết | Mô tả | Kết quả thực nghiệm | Kết luận |
| :--- | :--- | :--- | :--- |
| **H1 (Lọc nhiễu & Tinh giản chiều)** | Binary PSO có khả năng nhận diện và loại bỏ các đặc trưng dư thừa/nhiễu để tối ưu hóa không gian biểu diễn. | PSO đã giảm số đặc trưng từ 63 xuống **17 đặc trưng** (tỷ lệ tinh giản **73.02%**), tập trung vào các tín hiệu cốt lõi. | **CHẤP NHẬN H1** |
| **H2 (Đánh đổi hiệu năng & Tinh giản)** | Bộ đặc trưng tinh giản bằng PSO vẫn duy trì hiệu năng phân loại (PR-AUC và ROC-AUC) trong giới hạn chấp nhận được so với bộ đặc trưng đầy đủ. | Mô hình XGBoost với 17 đặc trưng PSO đạt PR-AUC 0.2584 / ROC-AUC 0.5846 so với 0.2654 / 0.6006 của mô hình 63 đặc trưng (đánh đổi nhẹ 0.0070 PR-AUC để đổi lấy giảm 73% số chiều). | **CHẤP NHẬN H2 (CÓ ĐÁNH ĐỔI)** |
| **H3 (Tối ưu tài nguyên hạ nguồn)** | Thời gian huấn luyện mô hình hạ nguồn giảm mạnh khi áp dụng bộ đặc trưng rút gọn. | Thời gian fit XGBoost giảm hơn **52%** (từ 4.65s xuống **2.22s**); trên mô hình HistGradientBoosting giảm **73%** (từ 16.96s xuống **4.52s**). Tổng chi phí tìm kiếm PSO là 11.79s (đầu tư một lần ở pha offline). | **CHẤP NHẬN H3** |

---

## 2. Bảng kết quả thực nghiệm 7 mô hình cơ sở (`baseline_metrics.csv`)

Đánh giá trên tập Holdout độc lập (`split_id: stratified_80_20_v1`, 32,000 khách hàng, ngưỡng cố định 0.5):

| Thuật toán | Số đặc trưng | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Thời gian Fit (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | 180 | **0.2758** | **0.6097** | **0.3575** | 0.2570 | 0.5873 | 34.85s |
| **Random Forest** | 180 | 0.2700 | 0.6031 | 0.3488 | 0.2589 | 0.5346 | 29.80s |
| **Logistic Regression** | 180 | 0.2649 | 0.5989 | 0.3473 | 0.2529 | 0.5541 | **1.49s** |
| **Decision Tree** | 180 | 0.2584 | 0.5851 | 0.3446 | 0.2468 | 0.5710 | 10.23s |
| **SGDClassifier (log_loss)** | 180 | 0.2456 | 0.5748 | 0.3357 | 0.2404 | 0.5563 | 6.66s |
| **Naive Bayes** | 180 | 0.2161 | 0.5177 | 0.2825 | 0.2171 | 0.4040 | **0.57s** |
| **K-Nearest Neighbors (KNN)** | 180 | 0.2102 | 0.5167 | 0.0685 | 0.2231 | 0.0405 | 17.10s |

---

## 3. Bảng so sánh chuyên sâu (`metrics_comparison.csv`)

| Mô hình & Cấu hình đặc trưng | Số đặc trưng | PR-AUC | ROC-AUC | F1-Score | Fit Time (s) | Search Cost (s) | Total Time (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Full Features)** | 63 | 0.2730 | 0.6078 | 0.3558 | 16.96s | 0.00s | 16.96s |
| **Baseline (Statistical Features)** | 17 | **0.2759** | **0.6105** | 0.3557 | 6.35s | 0.13s | **6.48s** |
| **Baseline (PSO Features)** | 17 | 0.2601 | 0.5894 | 0.3411 | 4.52s | 11.79s | 16.31s |
| **XGBoost (Full Features)** | 63 | 0.2654 | 0.6006 | 0.3475 | 4.65s | 0.00s | 4.65s |
| **XGBoost (PSO Features)** | 17 | 0.2584 | 0.5846 | 0.3319 | **2.22s** | 11.79s | 14.01s |

---

## 4. Top 10 đặc trưng quan trọng nhất (XGBoost Feature Importance)

1. `age` (6.60%)
2. `loyalty_score` (4.25%)
3. `discount_usage_rate` (3.64%)
4. `review_loyalty_score` (3.31%)
5. `discount_interaction` (1.72%)
6. `avg_cart_additions` (1.64%)
7. `cart_to_page_ratio` (1.59%)
8. `spend_per_item` (1.57%)
9. `pct_express_shipping` (1.55%)
10. `pct_standard_shipping` (1.55%)
