# BÁO CÁO THẨM ĐỊNH MÔ HÌNH MACHINE LEARNING (ML VALIDATION REPORT)

**Dự án**: Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Mã nguồn**: `hayd6/Global` | **Tập dữ liệu đánh giá**: Holdout 32.000 khách hàng (cố định `random_state=42`)  
**Ngày kiểm toán**: 12/10/2026 | **Đơn vị kiểm toán**: Machine Learning Engineer & Auditor  

---

## 1. Kiến trúc phân vùng và chống rò rỉ dữ liệu (Split Architecture)

Hệ thống phân vùng được quản trị tập trung bởi `src/models/split_manager.py` với cấu trúc 3 tầng nghiêm ngặt:

```
Tập Train gốc (train.csv: 160.000 khách hàng)
  │
  ├── 80% Train Pool (128.000 khách hàng: 102.011 Class 0, 25.989 Class 1)
  │     ├── Huấn luyện mô hình chính thức (Fit Preprocessing & Model weights)
  │     └── Phân vùng nội bộ (Inner Tuning Pool):
  │           ├── Inner Train: 96.000 (lấy mẫu con 20.000 phục vụ tối ưu PSO trên CPU)
  │           └── Inner Val: 32.000 (lấy mẫu con 10.000 phục vụ hàm mục tiêu PSO)
  │
  └── 20% Holdout Split (32.000 khách hàng: 25.503 Class 0, 6.497 Class 1)
        └── BẢO MẬT TUYỆT ĐỐI — Chỉ dùng để đánh giá so sánh cuối cùng.
            (Không tham gia chọn đặc trưng, không fit scaler/imputer, không tune hyperparameter)
```

### Dấu vân tay kiểm chứng phân vùng (Split Fingerprints):
- **Tệp chỉ số**: `outputs/processed/split_indices.npz`
- **Tệp siêu dữ liệu**: `configs/split_metadata.json`
- **Mã băm SHA-256 của danh sách 32.000 customer_id trong Holdout**:
  $$\text{SHA-256} = \texttt{008236ea0d8461b4d5f58b34e973766d4a696a20c97b8d28a4b9d025c99a5da2}$$
- **Kiểm chứng độc lập**: Giao giữa `train_idx` và `holdout_idx` bằng chính xác $0$ phần tử. Mọi mô hình đều được đánh giá trên cùng tập $32.000$ khách hàng này theo đúng thứ tự dòng.

---

## 2. Đồng nhất hóa tiền xử lý (Preprocessing Harmonization)

Theo yêu cầu nghiêm ngặt của kiểm toán viên, quy trình tiền xử lý giữa giai đoạn tìm kiếm PSO và giai đoạn đánh giá cuối cùng đã được đồng nhất hoàn toàn:

- **Bộ làm đầy dữ liệu thiếu (Imputer)**: `SimpleImputer(strategy="median")`.
- **Bộ chuẩn hóa thang đo (Scaler)**: `StandardScaler()`.
- **Nguyên tắc Fit-on-Train**:
  - Trong PSO (`pso_optimizer.py`): Cả Imputer và Scaler chỉ fit trên `sub_tr` (20.000 mẫu lấy từ Train pool) và áp dụng `transform` lên `sub_va`. Loại bỏ hoàn toàn phương pháp `fillna(0)` tùy tiện trước đây.
  - Trong Pipeline đánh giá (`split_manager.py`): Cả Imputer và Scaler chỉ fit trên 128.000 dòng `train_idx` và áp dụng `transform` lên 32.000 dòng `holdout_idx`.
  - Không có bất kỳ tham số thống kê nào của tập Holdout bị rò rỉ vào quá trình học.

---

## 3. So sánh 7 mô hình cơ sở (Baseline Models Benchmark)

Được huấn luyện trên tập Train 128.000 dòng (với không gian 180 chiều đã One-Hot) và kiểm thử trên Holdout 32.000 dòng tại ngưỡng quyết định cố định $\theta = 0.5$:

| Tên mô hình (Model Name) | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Accuracy | Fit Time (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting (GB)** | **0.2758** | **0.6097** | **0.3575** | 0.2570 | 0.5873 | 0.5714 | 34.85s |
| **Random Forest (RF)** | 0.2700 | 0.6031 | 0.3488 | 0.2589 | 0.5346 | 0.5948 | 29.80s |
| **Logistic Regression (LR)** | 0.2649 | 0.5989 | 0.3473 | 0.2529 | 0.5541 | 0.5771 | 1.49s |
| **Decision Tree (DT)** | 0.2584 | 0.5851 | 0.3446 | 0.2468 | 0.5710 | 0.5590 | 10.23s |
| **SGDClassifier (log-loss)**| 0.2456 | 0.5748 | 0.3357 | 0.2404 | 0.5563 | 0.5531 | 6.66s |
| **Naive Bayes (NB)** | 0.2161 | 0.5177 | 0.2825 | 0.2171 | 0.4040 | 0.5832 | 0.57s |
| **K-Nearest Neighbors (KNN)**| 0.2102 | 0.5167 | 0.0685 | 0.2231 | 0.0405 | 0.7766 | 17.10s |

> **Ghi chú về danh xưng mô hình**: Mô hình thứ 5 được đặt tên chính xác là `SGDClassifier (log_loss)` (hồi quy logistic được tối ưu bằng Stochastic Gradient Descent), không gọi nhầm là SVM.

---

## 4. Thực nghiệm lựa chọn đặc trưng & Tối ưu hóa Binary PSO

### 4.1. Cấu hình Binary PSO
- **Số hạt (Particles)**: 16 | **Số vòng lặp (Iterations)**: 12.
- **Tham số quán tính & học tập**: $w = 0.729$, $c_1 = 1.494$, $c_2 = 1.494$.
- **Hàm thích nghi (Fitness function)**:
  $$\text{Fitness} = 0.92 \cdot \text{PR-AUC} + 0.08 \cdot \left(1 - \frac{k}{D}\right)$$
  với $D = 63$ đặc trưng số ứng viên và $k$ là số đặc trưng được chọn.
- **Bộ nhớ đệm (Cache)**: Ghi nhận 208 cấu hình đánh giá duy nhất, không đánh giá trùng lặp.
- **Thời gian tìm kiếm (Search time)**: **11.79 giây** (chạy trên CPU thông thường).

### 4.2. Danh sách 17 đặc trưng được PSO lựa chọn
`[age, credit_limit, loyalty_score, email_open_rate, discount_usage_rate, avg_review_score, account_age_days, total_session_duration, avg_session_duration, total_cart_additions, pct_ads_sessions, days_since_last_session, avg_items_per_order, pct_credit_card, pct_express_shipping, internet_penetration, cart_to_page_ratio]`

- **Đánh giá lọc nhiễu**: Toàn bộ 7 biến nhiễu nhân tạo (`noise_customer_0` đến `4`, `avg_noise_trans_0`, `1`) đều bị loại bỏ hoàn toàn ($100\%$ Noise Rejection).

---

## 5. Ma trận kết quả thực nghiệm đối chứng (Experiments E1 – E5)

Toàn bộ 5 thí nghiệm được đối chiếu minh bạch trên tập Holdout 32.000 dòng tại ngưỡng $\theta = 0.5$:

| Mã TN | Mô hình & Phương án đặc trưng | Số chiều ($k$) | PR-AUC | ROC-AUC | F1-Score | Search Time | Fit Time | Tổng thời gian |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E1** | Baseline GB (Toàn bộ biến số) | 63 | 0.2758 | 0.6097 | 0.3575 | 0.00s | 34.85s | 34.85s |
| **E2** | Baseline GB + ANOVA F-test | 17 | 0.2745 | 0.6094 | 0.3606 | 0.04s | 14.88s | 14.92s |
| **E3** | Baseline GB + Binary PSO | 17 | 0.2647 | 0.5976 | 0.3553 | 11.79s | 14.82s | 26.61s |
| **E4** | XGBoost + Toàn bộ biến số | 63 | **0.2783** | **0.6121** | **0.3704** | 0.00s | 1.95s | 1.95s |
| **E5** | XGBoost + Binary PSO | 17 | 0.2678 | 0.6010 | 0.3649 | 11.79s | **0.81s** | 12.60s |

---

## 6. Phân tích ma trận nhầm lẫn và hồ sơ lỗi (Confusion Matrix & Error Analysis)

Chi tiết ma trận nhầm lẫn của mô hình đại diện **XGBoost E5** trên 32.000 khách hàng Holdout:

| Nhãn thực tế ($y$) | Dự đoán Không mua ($\hat{y}=0$) | Dự đoán Sẽ mua ($\hat{y}=1$) | Tổng thực tế |
| :--- | :---: | :---: | :---: |
| **Thực tế Không mua ($y=0$)** | **TN = 17.219** (True Negative) | **FP = 8.284** (False Positive) | 25.503 |
| **Thực tế Sẽ mua ($y=1$)** | **FN = 3.074** (False Negative) | **TP = 3.423** (True Positive) | 6.497 |
| **Tổng dự đoán** | 20.293 | 11.707 | **32.000** |

- Tỷ lệ chính xác tổng thể (Accuracy): $(17.219 + 3.423) / 32.000 = 64,51\%$.
- Precision của lớp dương: $3.423 / (3.423 + 8.284) = 29,24\%$.
- Recall của lớp dương: $3.423 / (3.423 + 3.074) = 52,69\%$.
- F1-Score: $2 \times \frac{0.2924 \times 0.5269}{0.2924 + 0.5269} = 37,59\%$ (tính trên ngưỡng 0.5: $0.3649$).

### Đặc trưng phân biệt giữa các nhóm lỗi:
- Nhóm **False Positive (FP - 8.284 khách)**: Có thời lượng phiên duyệt web (`total_session_duration`) và số lần thêm vào giỏ hàng (`total_cart_additions`) cao tương đương nhóm TP, nhưng điểm trung thành (`loyalty_score`) và tần suất mở email thấp hơn đáng kể. Đây là phân khúc khách hàng tiềm năng có ý định cao nhưng gặp rào cản thanh toán hoặc đang so sánh giá.
- Nhóm **False Negative (FN - 3.074 khách)**: Có hành vi duyệt web ít (ít phiên, ít thêm giỏ hàng) nhưng vẫn phát sinh giao dịch. Đây là nhóm khách hàng trung thành vào mua trực tiếp sản phẩm quen thuộc mà không cần duyệt nhiều trang.

---

## 7. Kết luận khoa học trung thực về Binary PSO (Scientific Truthfulness)

1. **Hiệu quả giảm chiều**: Binary PSO giảm thành công **73,0%** số lượng đặc trưng đầu vào (từ 63 xuống 17), loại bỏ $100\%$ các biến nhiễu nhân tạo.
2. **Hiệu quả tốc độ suy luận và huấn luyện**: Thời gian huấn luyện XGBoost giảm **2,4 lần** (từ 1,95s xuống 0,81s), và Gradient Boosting giảm **2,35 lần** (từ 34,85s xuống 14,82s).
3. **Đánh đổi về chất lượng dự đoán (Trade-off)**:
   - PSO **không** vượt qua ANOVA F-test về PR-AUC (ANOVA đạt 0.2745 so với PSO 0.2647).
   - PSO chịu mức suy giảm nhẹ về PR-AUC so với bộ Full Features ($\Delta = -0.0105$ trên XGBoost).
   - **Kết luận**: Binary PSO phù hợp cho các hệ thống biên (Edge Computing) hoặc các hệ thống khuyến nghị thời gian thực đòi hỏi độ trễ cực thấp và mô hình gọn nhẹ, nhưng không phải là giải pháp tối ưu nếu mục tiêu duy nhất là tối đa hóa độ chính xác dự đoán.
