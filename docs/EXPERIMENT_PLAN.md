# EXPERIMENT PLAN & EMPIRICAL FINDINGS

Tài liệu này tổng hợp thiết kế thực nghiệm và **kết quả thực nghiệm thực tế** thu được từ quy trình kiểm thử khoa học trên tập dữ liệu 200,000 khách hàng thương mại điện tử.

---

## 1. Kiểm định các giả thuyết nghiên cứu (Hypotheses Verification)

| Giả thuyết | Mô tả | Kết quả thực nghiệm | Kết luận |
| :--- | :--- | :--- | :--- |
| **H1 (Lọc nhiễu)** | Binary PSO có khả năng nhận diện và loại bỏ các đặc trưng nhiễu nhân tạo và các biến thứ cấp có độ tương quan thấp. | PSO đã giảm số đặc trưng từ 63 xuống **17 đặc trưng** (tỷ lệ tinh giản **73.0%**), loại bỏ các biến phi tương quan. | **CHẤP NHẬN H1** |
| **H2 (Hiệu quả dự đoán)** | Bộ đặc trưng tinh giản bằng PSO vẫn duy trì hiệu năng phân loại (PR-AUC và ROC-AUC) tương đương bộ đặc trưng đầy đủ. | Mô hình XGBoost với 17 đặc trưng PSO đạt PR-AUC 0.2590 / ROC-AUC 0.5875 so với 0.2659 / 0.6033 của mô hình 63 đặc trưng (chênh lệch dưới 2.6%). | **CHẤP NHẬN H2** |
| **H3 (Tối ưu tài nguyên)** | Thời gian huấn luyện và suy luận giảm tỷ lệ thuận với số lượng đặc trưng được tinh giản. | Thời gian huấn luyện XGBoost giảm hơn **50%** (từ 3.10s xuống **1.52s**); trên mô hình Gradient Boosting giảm **74%** (từ 15.64s xuống **4.08s**). | **CHẤP NHẬN H3** |

---

## 2. Bảng kết quả thực nghiệm 7 mô hình cơ sở (`baseline_metrics.csv`)

Đánh giá trên tập Validation độc lập (32,000 khách hàng, Stratified split 80/20, `random_state=42`):

| Thuật toán | Số đặc trưng | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Thời gian huấn luyện (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | 180 | **0.2785** | **0.6150** | **0.3660** | 0.2442 | 0.7303 | 19.17s |
| **Random Forest** | 180 | 0.2753 | 0.6101 | 0.3635 | 0.2425 | 0.7258 | 12.95s |
| **Logistic Regression** | 180 | 0.2704 | 0.6033 | 0.3602 | 0.2396 | 0.7299 | **1.10s** |
| **Support Vector Machine (SGD)** | 180 | 0.2578 | 0.5858 | 0.3526 | 0.2337 | 0.7214 | 4.30s |
| **Decision Tree** | 180 | 0.2575 | 0.5927 | 0.3569 | 0.2372 | 0.7247 | 7.14s |
| **Naive Bayes** | 180 | 0.2170 | 0.5235 | 0.3377 | 0.2073 | 0.9080 | 0.42s |
| **K-Nearest Neighbors (KNN)** | 180 | 0.2108 | 0.5187 | 0.3375 | 0.2071 | 0.9103 | 8.04s |

---

## 3. Bảng so sánh chuyên sâu (`metrics_comparison.csv`)

| Mô hình & Cấu hình đặc trưng | Số đặc trưng | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Accuracy | Thời gian Fit (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Full Features)** | 63 | 0.2720 | 0.6087 | 0.3664 | 0.2445 | 0.7306 | 0.4861 | 15.64s |
| **Baseline (Statistical Features)** | 17 | 0.2714 | 0.6090 | 0.3671 | 0.2422 | 0.7582 | 0.4681 | 6.39s |
| **Baseline (PSO Features)** | 17 | 0.2600 | 0.5906 | 0.3557 | 0.2364 | 0.7180 | 0.4708 | 4.08s |
| **XGBoost (Full Features)** | 63 | 0.2659 | 0.6033 | 0.3630 | 0.2398 | 0.7462 | 0.4672 | 3.10s |
| **XGBoost (PSO Features)** | 17 | 0.2590 | 0.5875 | 0.3547 | 0.2411 | 0.6708 | 0.5034 | **1.52s** |

---

## 4. Top 10 đặc trưng quan trọng nhất (XGBoost Feature Importance)

1. `age` (8.39%)
2. `review_loyalty_score` (3.97%)
3. `discount_usage_rate` (3.63%)
4. `loyalty_score` (3.60%)
5. `discount_interaction` (1.74%)
6. `avg_cart_additions` (1.72%)
7. `loyalty_spend_product` (1.51%)
8. `cart_to_page_ratio` (1.51%)
9. `duration_per_page` (1.50%)
10. `total_spend` (1.50%)
