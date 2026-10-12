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

Được huấn luyện trên tập Train 128.000 dòng (với không gian 180 chiều đã One-Hot) và kiểm thử trên Holdout 32.000 dòng tại ngưỡng quyết định cố định $\theta = 0.5$ (nguồn: `outputs/metrics/baseline_metrics.csv`):

| Tên mô hình (Model Name) | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Accuracy | Fit Time (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting (GB)** | **0.2758** | **0.6097** | **0.3575** | 0.2570 | 0.5873 | 0.5714 | 34.85s |
| **Random Forest (RF)** | 0.2700 | 0.6031 | 0.3488 | 0.2589 | 0.5346 | 0.5948 | 29.80s |
| **Logistic Regression (LR)** | 0.2649 | 0.5989 | 0.3473 | 0.2529 | 0.5541 | 0.5771 | 1.49s |
| **Decision Tree (DT)** | 0.2584 | 0.5851 | 0.3446 | 0.2468 | 0.5710 | 0.5590 | 10.23s |
| **SGDClassifier (log_loss)**| 0.2456 | 0.5748 | 0.3357 | 0.2404 | 0.5563 | 0.5531 | 6.66s |
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

Toàn bộ 5 thí nghiệm được đối chiếu minh bạch trên tập Holdout 32.000 dòng tại ngưỡng $\theta = 0.5$ (dữ liệu nguồn chính thức: `outputs/metrics/metrics_comparison.csv`):

| Mã TN | Mô hình & Phương án đặc trưng | Số chiều ($k$) | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Accuracy | Search Time | Fit Time | Tổng thời gian |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E1** | Baseline GB (Full Features) | 63 | 0.2730 | 0.6078 | 0.3558 | 0.2573 | 0.5766 | 0.5762 | 0.00s | 17.04s | 17.04s |
| **E2** | Baseline GB (Statistical Features) | 17 | **0.2759** | **0.6105** | 0.3557 | 0.2566 | **0.5797** | 0.5737 | 0.13s | 6.24s | **6.37s** |
| **E3** | Baseline GB (PSO Features) | 17 | 0.2601 | 0.5894 | 0.3411 | 0.2535 | 0.5209 | 0.5914 | 11.79s | 4.50s | 16.29s |
| **E4** | XGBoost (Full Features) | 63 | 0.2654 | 0.6006 | 0.3475 | **0.2594** | 0.5262 | 0.5987 | 0.00s | 4.40s | 4.40s |
| **E5** | XGBoost (PSO Features) | 17 | 0.2584 | 0.5846 | 0.3319 | 0.2515 | 0.4879 | **0.6012** | 11.79s | **2.07s** | 13.86s |

---

## 6. Phân tích ma trận nhầm lẫn và hồ sơ lỗi (Confusion Matrix & Error Analysis)

Chi tiết ma trận nhầm lẫn của mô hình chuẩn **XGBoost (Full Features)** trên 32.000 khách hàng Holdout (khớp 100% từng dòng với artifact độc lập `outputs/holdout_predictions.csv`, metadata `outputs/holdout_prediction_metadata.json` và dòng 5 của `outputs/metrics/metrics_comparison.csv`):

| Nhãn thực tế ($y$) | Dự đoán Không mua ($\hat{y}=0$) | Dự đoán Sẽ mua ($\hat{y}=1$) | Tổng thực tế |
| :--- | :---: | :---: | :---: |
| **Thực tế Không mua ($y=0$)** | **TN = 15.740** (True Negative) | **FP = 9.763** (False Positive) | 25.503 |
| **Thực tế Sẽ mua ($y=1$)** | **FN = 3.078** (False Negative) | **TP = 3.419** (True Positive) | 6.497 |
| **Tổng dự đoán** | 18.818 | 13.182 | **32.000** |

- Tỷ lệ chính xác tổng thể (Accuracy): $(15.740 + 3.419) / 32.000 = 59,87\%$.
- Precision của lớp dương: $3.419 / (3.419 + 9.763) = 25,94\%$.
- Recall của lớp dương: $3.419 / (3.419 + 3.078) = 52,62\%$.
- Specificity: $15.740 / 25.503 = 61,72\%$.
- F1-Score: $2 \times \frac{0.2594 \times 0.5262}{0.2594 + 0.5262} = 34,75\%$.

Đối chiếu với mô hình **XGBoost (PSO Features)** tại dòng 6 của `metrics_comparison.csv`:
- $\text{TN} = 16.067$, $\text{FP} = 9.436$, $\text{FN} = 3.327$, $\text{TP} = 3.170$.
- Accuracy: $60,12\%$, Precision: $25,15\%$, Recall: $48,79\%$, F1-Score: $33,19\%$.

### Đặc trưng phân biệt giữa các nhóm lỗi (Phân tích định tính trên Holdout 32k):
- Nhóm **False Positive (FP - 9.763 khách)**: Có thời lượng phiên duyệt web (`total_session_duration`) và số lần thêm vào giỏ hàng (`total_cart_additions`) cao tương đương nhóm TP, nhưng điểm trung thành (`loyalty_score`) và tần suất mở email thấp hơn đáng kể. Đây là phân khúc khách hàng tiềm năng có ý định cao nhưng gặp rào cản thanh toán hoặc đang so sánh giá.
- Nhóm **False Negative (FN - 3.078 khách)**: Có hành vi duyệt web ít (ít phiên, ít thêm giỏ hàng) nhưng vẫn phát sinh giao dịch. Đây là nhóm khách hàng trung thành vào mua trực tiếp sản phẩm quen thuộc mà không cần duyệt nhiều trang.

---

## 7. Kết luận khoa học trung thực về Binary PSO (Scientific Truthfulness)

1. **Hiệu quả giảm chiều**: Binary PSO giảm thành công **73,02%** số lượng đặc trưng đầu vào (từ 63 xuống 17 đặc trưng), loại bỏ $100\%$ các biến nhiễu nhân tạo.
2. **Hiệu quả tốc độ huấn luyện**: Thời gian huấn luyện XGBoost giảm **2,1 lần** (từ 4,40s xuống 2,07s), và Gradient Boosting giảm **3,8 lần** (từ 17,04s xuống 4,50s).
3. **Đánh đổi về chất lượng dự đoán (Trade-off)**:
   - PSO **không** vượt qua ANOVA F-test về PR-AUC (ANOVA đạt 0.2759 so với PSO 0.2601 trên mô hình Baseline; trên XGBoost, Full đạt 0.2654 so với PSO 0.2584, mức chênh lệch $\Delta = -0.0070$).
   - **Kết luận**: Binary PSO phù hợp cho các hệ sinh thái đòi hỏi độ tinh giản đặc trưng cao, loại bỏ rác tự động và giảm thiểu tài nguyên suy luận, nhưng cần cân nhắc trade-off với độ chính xác khi so với phương pháp lọc thống kê truyền thống.
