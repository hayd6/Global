# BÁO CÁO KIỂM TOÁN DỮ LIỆU VÀ KHOA HỌC DỮ LIỆU (DATA & ML SCIENTIFIC AUDIT)
**Dự án:** Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Mã kho lưu trữ:** `hayd6/Global`  
**Ngày kiểm toán:** 12/10/2026 | **Phiên bản:** v1.0-Audit-Master  
**Phương pháp kiểm toán:** Kiểm tra tĩnh và động đọc-chỉ-đọc (Read-Only Scientific Verification), sử dụng truy vấn DuckDB trực tiếp trên 8 tệp gốc và tệp Parquet dẫn xuất, đối chiếu mã nguồn và cấu hình thực nghiệm.

---

## 1. TÓM TẮT ĐÁNH GIÁ TỔNG THỂ

1. **Về tính toàn vẹn kỹ thuật (Technical Pipeline Integrity):**
   - Pipeline dữ liệu từ tầng làm sạch ([clean_data.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/data/clean_data.py)), tích hợp đa bảng ([integrate_data.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/data/integrate_data.py)), kỹ thuật đặc trưng ([build_features.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/features/build_features.py)) đến phân chia tập ([split_manager.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/models/split_manager.py)) và huấn luyện mô hình ([train_xgboost.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/models/train_xgboost.py)) được xây dựng **rất bài bản, chặt chẽ và không có rò rỉ dữ liệu trong code** (No Code-level Data Leakage).
   - Bộ tiền xử lý (Imputer, Scaler, OneHotEncoder) và bộ chọn đặc trưng (ANOVA) được huấn luyện strictly trên tập Train (128.000 mẫu); tập Holdout (32.000 mẫu) được cô lập tuyệt đối; tập Test (40.000 mẫu) hoàn toàn độc lập. Toàn bộ 38 bài kiểm thử tự động trong `tests/` đều pass.

2. **Về bản chất dữ liệu nguồn (Underlying Dataset Realities):**
   - Kiểm toán thực nghiệm phát hiện bộ dữ liệu nguồn mang bản chất **dữ liệu tổng hợp nhân tạo (Synthetic Benchmark Dataset)** với các nghịch lý thời gian nghiêm trọng:
     - **49.86% phiên duyệt web (997.299 / 2.000.000 phiên)** xảy ra *trước* ngày đăng ký tài khoản của khách hàng (`session_timestamp < signup_date`).
     - **49.88% giao dịch (249.377 / 500.000 giao dịch)** xảy ra *trước* ngày đăng ký tài khoản (`transaction_timestamp < signup_date`).
     - **92.61% phiên gắn mã chiến dịch (1.852.248 / 2.000.000 phiên)** diễn ra *ngoài* khoảng thời gian bắt đầu và kết thúc của chiến dịch marketing tương ứng.
   - Các mốc thời gian được tạo độc lập ngẫu nhiên đồng đều trong giai đoạn 2022-01-01 đến 2024-09-26, không tuân thủ thứ tự nhân quả thực tế.

3. **Về định nghĩa bài toán và nhãn mục tiêu (Target Definition & Scope):**
   - Cả hai nhóm `target = 0` và `target = 1` đều có tỷ lệ khách hàng từng có ít nhất 1 giao dịch trong lịch sử hoàn toàn đồng nhất (**91.79%**), số giao dịch trung bình (2.73 so với 2.71) và tổng chi tiêu trung bình ($327.57 so với $326.18) gần như tương đương. Tỷ lệ phát sinh giao dịch trong 30 ngày cuối cũng ngang nhau (7.58% so với 7.44%).
   - Do đó, nhãn `target` không phản ánh "khách hàng đã từng mua hàng" hay "giao dịch trong 30 ngày cuối". Việc nhóm nghiên cứu định vị đề tài là **Observational Snapshot Purchase Propensity Classification** (Phân loại độ nghiêng mua hàng trên ảnh chụp quan sát) là hoàn toàn đúng đắn và bắt buộc để bảo vệ tính hợp lệ khoa học của đồ án.

4. **Về hiệu quả của Binary PSO:**
   - PSO hoàn thành xuất sắc mục tiêu **tinh giản số chiều và tăng tốc huấn luyện**: giảm **73.02% đặc trưng** (từ 63 biến xuống 17 biến tối ưu), giúp mô hình hạ nguồn tăng tốc **2.12 lần** (XGBoost fit giảm từ 4.40s xuống 2.07s) và **3.79 lần** (Gradient Boosting fit giảm từ 17.04s xuống 4.50s).
   - Tuy nhiên, về mặt độ đo phân loại, **ANOVA 17 đặc trưng đạt PR-AUC cao hơn PSO** (0.2759 so với 0.2601 trên Gradient Boosting; XGBoost PSO đạt 0.2584) với chi phí tìm kiếm thấp hơn 90 lần (0.13s so với 11.79s). Đây là kết quả thực nghiệm khách quan cần được báo cáo trung thực dưới góc độ đánh đổi đa mục tiêu (Trade-off).

---

## 2. SƠ ĐỒ PIPELINE THỰC TẾ

```
[dataset/ (8 CSVs - READ ONLY)]
   │ (customers: 200k, sessions: 2M, transactions: 500k, mkt: 200, geo: 100, train: 160k, test: 40k)
   ▼
[src/data/clean_data.py]
   │ Normalization: $ và dấu phẩy -> DOUBLE, bounce/discount -> binary 0/1, pages_viewed 'N/A' -> NULL
   ▼
[src/data/integrate_data.py]
   │ Pre-aggregation: sessions (1 row/cust), transactions (1 row/cust), dominant geo & campaign
   │ Anti-inflation JOIN: LEFT JOIN vào 200k customers -> Bảo toàn 100% 200,000 dòng duy nhất
   ▼
[src/features/build_features.py]
   │ Derived ratios (+ 1.0 denominator smoothing), interaction indices, engagement score
   │ Output: outputs/customer_features.parquet (200k dòng, 72 cột)
   ▼
[src/models/split_manager.py]
   │ Filter split_type = 'train' (160k dòng) -> Stratified 80/20 (Seed 42)
   ├───────────────────────────────┬────────────────────────────────┐
   │                               │                                │
   ▼                               ▼                                ▼
[Train Split: 128,000 samples]   [Holdout Split: 32,000 samples]   [Test Set: 40,000 samples]
   │                               │ (Isolated Ground Truth)        │ (Strictly Unused)
   ├─────────────────────────────┐ │                                │
   │                             │ │                                │
   ▼                             ▼ │                                │
[Inner Train: 20k] [Inner Val: 10k]│                                │
   │ (Proxy LR, Alpha=0.92)      │ │                                │
   ▼                             │ │                                │
[Binary PSO (16p x 12i)]         │ │                                │
   │ -> 17 Selected Features     │ │                                │
   └──────────────┬──────────────┘ │                                │
                  ▼                │                                │
          [Model Training]         │                                │
          - E1: GB Full (63) ──────┼──> Predict -> outputs/metrics/metrics_comparison.csv
          - E2: GB ANOVA (17) ─────┼──> Predict -> outputs/holdout_predictions.csv (32k)
          - E3: GB PSO (17) ───────┼──> TN=15,740, FP=9,763, FN=3,078, TP=3,419
          - E4: XGB Full (63) ─────┤    PR-AUC=0.2654, ROC-AUC=0.6006, F1=0.3475
          - E5: XGB PSO (17) ──────┘
```

---

## 3. BẢNG CHẤT LƯỢNG DỮ LIỆU NGUỒN

| Tệp dữ liệu | Số dòng / Cột | Khóa chính | Số dòng lỗi / Bất thường | Tỷ lệ | Bản chất lỗi và Bằng chứng cụ thể | Tác động và Hướng xử lý |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `customers.csv` | 200,000 / 17 | `customer_id` (200k unique) | 10,000 dòng `age` mang chuỗi `'unknown'` | 5.00% | `TRY_CAST(age AS DOUBLE) IS NULL` | Đã xử lý tốt: `clean_data.py` ép kiểu NULL, `split_manager.py` impute trung vị. |
| `customers.csv` | 200,000 / 17 | `customer_id` | 200,000 dòng `credit_limit` có `$` và `,` | 100.0% | Định dạng tiền tệ chuỗi: `"$18,913"` | Đã xử lý tốt: bỏ `$` và `,`, cast sang DOUBLE. |
| `customers.csv` | 200,000 / 17 | `customer_id` | 22,746 dòng NULL ở `email_open_rate` | 11.37% | Missing value ngẫu nhiên | Đã xử lý tốt: SimpleImputer median khi fit trên Train. |
| `customers.csv` | 200,000 / 17 | `customer_id` | 200,000 dòng `referral_code` không NULL | 100.0% | 0 dòng NULL; 179,259 mã khác nhau | Biến phái sinh `has_referral_code` có phương sai = 0 (100% là 1). Cần loại bỏ đặc trưng này. |
| `sessions.csv` | 2,000,000 / 11 | `session_id` (2M unique) | 100,000 dòng `pages_viewed` mang `'N/A'` | 5.00% | Chuỗi `'N/A'` thay vì số nguyên | Đã xử lý tốt: `NULLIF('N/A')` rồi cast sang INTEGER. |
| `sessions.csv` | 2,000,000 / 11 | `session_id` | 2,000,000 dòng `bounce_flag` định dạng hỗn hợp | 100.0% | 6 dạng: `'1'`, `'0'`, `'Yes'`, `'No'`, `'TRUE'`, `'FALSE'` | Đã xử lý tốt: chuẩn hóa về cờ nhị phân 0/1 bằng SQL CASE. |
| `sessions.csv` | 2,000,000 / 11 | `session_id` | 997,299 phiên trước `signup_date` | 49.86% | `session_timestamp < c.signup_date` | Bất thường logic dữ liệu tổng hợp (xem mục 4). |
| `transactions.csv` | 500,000 / 11 | `transaction_id` (500k unique)| 25,059 dòng `items_count == 0` | 5.01% | `items_count = 0` nhưng `order_value` dương (TB: $118.76) | Bất thường logic thương mại (dịch vụ/giftcard hoặc lỗi ghi nhận). Mã nguồn đã an toàn nhờ mẫu số `+ 1.0`. |
| `transactions.csv` | 500,000 / 11 | `transaction_id` | 500,000 dòng `order_value` có `$` và `,` | 100.0% | Chuỗi tiền tệ: `"$170.24"` | Đã xử lý tốt: bỏ `$` và `,`, cast sang DOUBLE. |
| `transactions.csv` | 500,000 / 11 | `transaction_id` | 249,377 giao dịch trước `signup_date` | 49.88% | `transaction_timestamp < c.signup_date` | Bất thường logic dữ liệu tổng hợp (xem mục 4). |
| `marketing_campaigns.csv` | 200 / 6 | `campaign_id` (200 unique) | 1,852,248 phiên ngoài khoảng ngày chiến dịch | 92.61% | `session_timestamp` nằm ngoài `[start_date, end_date]` | Gán ngẫu nhiên `campaign_id` trong dữ liệu benchmark tổng hợp. |
| `geo_data.csv` | 100 / 5 | `geo_ip_region` (100 unique)| 0 lỗi | 0.0% | Toàn vẹn tham chiếu 100% với `sessions.csv` | Không có vấn đề. |
| `train.csv` | 160,000 / 2 | `customer_id` (160k unique)| 0 lỗi | 0.0% | Nhãn nhị phân: 79.70% âm (0), 20.30% dương (1) | Mất cân bằng lớp ~4:1; đã được xử lý bằng `class_weight='balanced'` và `scale_pos_weight=3.925`. |
| `test.csv` | 40,000 / 1 | `customer_id` (40k unique) | 0 lỗi | 0.0% | Hoàn toàn độc lập với train.csv (0 trùng lặp) | Giữ nguyên cô lập cho submission. |

---

## 4. CÁC VẤN ĐỀ VỀ TARGET VÀ DATA LEAKAGE (ƯU TIÊN CAO NHẤT)

### 4.1. Truy vết nguồn gốc nhãn Target
- **Đoạn mã tích hợp:** [src/data/integrate_data.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/data/integrate_data.py#L234-L236)
  ```sql
  LEFT JOIN read_csv_auto('dataset/train.csv') tr ON c.customer_id = tr.customer_id
  ```
- **Bằng chứng thực nghiệm:**
  - Nhóm `target = 0` (127,514 khách): 117,040 khách (91.79%) có giao dịch; số giao dịch TB: 2.730; tổng chi tiêu TB: $327.57.
  - Nhóm `target = 1` (32,486 khách): 29,820 khách (91.79%) có giao dịch; số giao dịch TB: 2.705; tổng chi tiêu TB: $326.18.
  - Tỷ lệ có giao dịch trong 30 ngày cuối (2024-08-27 đến 2024-09-26): nhóm 0 là 7.58%, nhóm 1 là 7.44%.
- **Đánh giá khoa học:**
  - Nhãn `target` trong `train.csv` **không được tạo ra từ việc lọc giao dịch trong `transactions.csv`**.
  - Không tồn tại một ngưỡng thời gian cắt nhãn (prediction cutoff timestamp) rõ ràng trong dữ liệu thô.
  - Do đó, nếu đề tài tuyên bố là "Mô hình dự báo khách hàng sẽ mua hàng trong 30 ngày tới theo chuỗi thời gian" thì sẽ **không thể bảo vệ được trước hội đồng khoa học** vì dữ liệu thực tế không hỗ trợ luận điểm này.
  - **Cách định vị hợp lệ duy nhất:** Đề tài phải được mô tả là **"Phân loại thiên hướng mua hàng của khách hàng dựa trên ảnh chụp hành vi quan sát đa bảng (Observational Snapshot Purchase Propensity Classification)"**.

### 4.2. Bằng chứng về sự đảo lộn thứ tự thời gian (Temporal Inversion)
- Truy vấn kiểm tra nhân quả thời gian:
  ```sql
  -- 49.86% phiên diễn ra trước ngày đăng ký tài khoản
  SELECT COUNT(*) FROM sessions s JOIN customers c ON s.customer_id = c.customer_id 
  WHERE s.session_timestamp < c.signup_date; -- Kết quả: 997,299 / 2,000,000 phiên

  -- 49.88% giao dịch diễn ra trước ngày đăng ký tài khoản
  SELECT COUNT(*) FROM transactions t JOIN customers c ON t.customer_id = c.customer_id 
  WHERE t.transaction_timestamp < c.signup_date; -- Kết quả: 249,377 / 500,000 giao dịch
  ```
- **Ý nghĩa khoa học:**
  Tỷ lệ chính xác ~50.0% chứng minh rằng nhà tạo lập dữ liệu Kaggle đã sinh ngẫu nhiên độc lập phân phối đều (Uniform Distribution) cho các cột ngày tháng trên cùng khoảng thời gian `[2022-01-01, 2024-09-26]`. Khi lấy hai biến ngẫu nhiên độc lập cùng phân phối, xác suất $P(T_1 < T_2) = 0.50$.
  Điều này khẳng định không thể áp dụng mô hình phân rã thời gian (Time-series train/test split) trên bộ dữ liệu này. Cách chia ngẫu nhiên phân tầng (Stratified Split) theo `customer_id` như hiện tại là cách tiếp cận duy nhất khả thi.

### 4.3. Kiểm tra rò rỉ dữ liệu trong mã nguồn (Code Leakage Audit)
- **Tập kiểm tra độc lập (`test.csv`):** Được giữ nguyên 100%, không bị đọc vào trong `split_manager.py`, không bị dùng trong fit preprocessor hay tuning threshold.
- **Tập kiểm định (`holdout_idx` - 32.000 mẫu):**
  - Trong [split_manager.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/models/split_manager.py#L173-L174):
    ```python
    X_train = preprocessor.fit_transform(X_train_raw)
    X_holdout = preprocessor.transform(X_holdout_raw)
    ```
    Bộ tiền xử lý fit strictly trên Train, chỉ transform trên Holdout.
  - Trong [pso_optimizer.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/models/pso_optimizer.py#L250-L268):
    Vòng lặp PSO chạy trên phân vùng nội bộ `pso_inner_train_idx` (20k) và `pso_inner_val_idx` (10k), được trích xuất hoàn toàn từ tập Train (128k), **tuyệt đối không chạm vào Holdout**.
  - Không có hiện tượng rò rỉ định danh (`customer_id`) hoặc nhãn (`target`) vào ma trận đặc trưng $X$ (đã được loại bỏ ở danh sách `drop_cols`).

---

## 5. CÁC VẤN ĐỀ VỀ FEATURE ENGINEERING

### 5.1. Bảng kiểm toán các đặc trưng có rủi ro cao

| Tên đặc trưng | Công thức trong mã nguồn | Vấn đề phát hiện | Bằng chứng thực nghiệm | Mức độ rủi ro & Tác động |
| :--- | :--- | :--- | :--- | :--- |
| `has_referral_code` | `CASE WHEN referral_code IS NOT NULL THEN 1 ELSE 0 END` | **Phương sai bằng 0 (Zero Variance)**. Tất cả 200,000 khách hàng đều có mã giới thiệu trong dữ liệu gốc. | `VAR_POP(has_referral_code) = 0.0`. 100% mẫu mang giá trị 1. | **LOW**: Đặc trưng vô nghĩa, bị `StandardScaler` ép về 0, không gây lỗi nhưng lãng phí chiều tính toán. |
| `activity_recency_ratio` | `ROUND(days_since_last_session / (account_age_days + 1.0), 4)` | **Đột biến ngoại lai cực đại (Extreme Outliers)**. Khi khách không có session (`days_since_last_session = 9999`) hoặc mới đăng ký (`account_age_days = 0, 1`), tỷ số vọt lên hàng trăm. | Giá trị lớn nhất đạt **432.0**, có 1,861 khách hàng có tỷ số > 10.0 (phân phối bị lệch đuôi phải nặng). | **MEDIUM**: Có thể làm méo mó trọng số trong mô hình hồi quy tuyến tính (Logistic Regression). Mô hình cây ít bị ảnh hưởng hơn. |
| `days_since_last_session` | `COALESCE(s.days_since_last_session, 9999)` | Sử dụng giá trị giả định lớn (`9999`) để đại diện cho khách hàng không có phiên duyệt web. | Có đúng 10 khách hàng nhận giá trị 9999. | **LOW**: Số lượng nhỏ (10/200,000 = 0.005%), cây quyết định dễ dàng phân tách ngưỡng. |
| `days_since_last_transaction` | `COALESCE(t.days_since_last_transaction, 9999)` | Sử dụng giá trị giả định lớn (`9999`) đại diện cho khách hàng chưa từng phát sinh giao dịch. | Có 16,459 khách hàng (8.23%) nhận giá trị 9999. | **MEDIUM**: Tỷ lệ 8.23% đáng kể. Cần đảm bảo mô hình nhận diện đây là nhóm chưa mua hàng thay vì một giá trị khoảng cách tuyến tính thực. |
| `spend_per_item` | `ROUND(total_spend / (total_items_count + 1.0), 2)` | Giao dịch gốc có 25,059 dòng `items_count == 0` nhưng `order_value > 0`. | Mẫu số được cộng làm mịn `+ 1.0` nên không bị chia cho 0. | **NONE (ĐÃ AN TOÀN)**: Công thức mã nguồn đã bảo vệ thành công tính bất biến. |
| `cart_to_page_ratio` | `ROUND(total_cart_additions / (total_pages_viewed + 1.0), 4)` | Cả hai biến thành phần đều có thể bằng 0. | Mẫu số có `+ 1.0`, giá trị chuẩn hóa an toàn trong đoạn `[0, 50]`. | **NONE (ĐÃ AN TOÀN)**: Đã được kiểm tra qua bài test `test_division_by_zero_smoothing_invariants`. |

### 5.2. Đối chiếu số lượng chiều đặc trưng qua từng bước
- Bảng Parquet tích hợp (`customer_features.parquet`): **72 cột**
  - 3 cột kỹ thuật / định danh / nhãn: `customer_id`, `split_type`, `target`.
  - 2 cột chuỗi thô của chiến dịch: `primary_campaign_type`, `primary_campaign_budget`.
  - 67 cột đặc trưng ứng viên (được ghi nhận trong `feature_dictionary.csv`).
- Không gian biến số liên tục (Pure Continuous Features): **63 đặc trưng**
  - Được lọc tự động trong `split_manager.py` khi bỏ 4 biến phân loại (`country_code`, `region`, `customer_tier`, `region_tier`).
  - Dùng cho các thuật toán: ANOVA F-test, Binary PSO, và 5 thí nghiệm cốt lõi E1–E5.
- Không gian biến đổi One-Hot (Transformed Features): **180 đặc trưng**
  - 63 biến số (Imputer median + StandardScaler) + 117 biến phân loại (Imputer mode + OneHotEncoder).
  - Dùng riêng cho bảng so sánh 7 thuật toán Machine Learning cơ sở (Baselines).

---

## 6. ĐÁNH GIÁ EDA VÀ THỐNG KÊ

1. **Về tương quan phân loại (Signal Strength):**
   - Không có bất kỳ đặc trưng nào có tương quan tuyến tính Pearson vượt quá **0.10** với nhãn `target`.
   - Ba đặc trưng có tương quan dương mạnh nhất: `loyalty_score` (r = **+0.0945**), `review_loyalty_score` (r = **+0.0918**), `discount_usage_rate` (r = **+0.0785**).
   - Đặc trưng có tương quan âm mạnh nhất: `age` (r = **-0.0715**).
   - Hầu hết các đặc trưng hành vi phiên (số trang xem, số phiên, thời gian duyệt) đều có tương quan gần bằng 0 ($r \approx 0.001 - 0.025$).
   - **Kết luận:** Tỷ số tín hiệu trên nhiễu (Signal-to-Noise Ratio) của bài toán tương đối thấp. Đây là bài toán khó, đòi hỏi mô hình phi tuyến tính tổng hợp nhiều tín hiệu yếu.

2. **Về phân tích hạng khách hàng (`customer_tier`):**
   - Tỷ lệ `target = 1` giữa các hạng: Bronze: 20.35%, Silver: 20.33%, Gold: 19.88%, Platinum: 20.66%.
   - Sự khác biệt giữa các hạng là không có ý nghĩa thống kê (chi-squared p-value > 0.05).
   - **Lưu ý:** Các tài liệu báo cáo không được kết luận rằng "Hạng Platinum mua hàng nhiều hơn rõ rệt so với Bronze", vì dữ liệu thực nghiệm cho thấy tỷ lệ mua giữa các hạng là tương đương nhau.

3. **Về 5 biến nhiễu nhân tạo (`noise_customer_0` đến `noise_customer_4`):**
   - Các biến này có tương quan với target dao động quanh 0.001 đến 0.003, đúng tính chất biến nhiễu chuẩn được đưa vào để thử thách thuật toán lựa chọn đặc trưng.

---

## 7. ĐÁNH GIÁ PREPROCESSING, SPLIT VÀ MACHINE LEARNING

### 7.1. Phân chia tập và Tránh rò rỉ
- **Tập Train:** 128,000 khách hàng (80% của 160,000 train pool).
- **Tập Holdout:** 32,000 khách hàng (20% của 160,000 train pool).
- Tỷ lệ positive được giữ nguyên hoàn hảo: Train = 20.30%, Holdout = 20.30% (Stratified Split, Seed 42).
- Khóa SHA-256 danh sách `customer_id` tập Holdout được cố định và kiểm tra tự động: `008236ea0d8461b4d5f58b34e973766d4a696a20c97b8d28a4b9d025c99a5da2`.

### 7.2. Phương pháp tính toán Metrics và Ngưỡng quyết định
- **PR-AUC:** Tính bằng `sklearn.metrics.average_precision_score(y_true, y_prob)`. Đây là chuẩn mực tối ưu cho dữ liệu mất cân bằng lớp (thay thế cho phép tính xấp xỉ hình thang thô `trapz` vốn dễ bị phóng đại).
- **Ngưỡng quyết định:** Cố định nghiêm ngặt tại $\tau = 0.50$ (`fixed_0.5`) trên toàn bộ 5 thí nghiệm để tránh hiện tượng rò rỉ tối ưu ngưỡng trên tập kiểm tra (threshold-tuning leakage).
- **Kiểm tra tính nhất quán toán học:**
  Trên tập Holdout 32,000 mẫu của mô hình chuẩn XGBoost:
  - $TN = 15,740$, $FP = 9,763$, $FN = 3,078$, $TP = 3,419$.
  - Tổng số mẫu: $15,740 + 9,763 + 3,078 + 3,419 = 32,000$ (Chính xác 100%).
  - Tổng nhãn 1: $TP + FN = 3,419 + 3,078 = 6,497$ ($6,497 / 32,000 = 20.303\%$).
  - Tổng nhãn 0: $TN + FP = 15,740 + 9,763 = 25,503$ ($25,503 / 32,000 = 79.697\%$).
  - $\text{Precision} = \frac{3,419}{3,419 + 9,763} = 0.2593688 \approx \mathbf{0.2594}$.
  - $\text{Recall} = \frac{3,419}{3,419 + 3,078} = 0.5262429 \approx \mathbf{0.5262}$.
  - $\text{Accuracy} = \frac{15,740 + 3,419}{32,000} = 0.5987188 \approx \mathbf{0.5987}$.
  - $\text{F1-score} = \frac{2 \times 0.2593688 \times 0.5262429}{0.2593688 + 0.5262429} = 0.347477 \approx \mathbf{0.3475}$.
  $\Rightarrow$ Tất cả số liệu trong `metrics_comparison.csv` và `holdout_predictions.csv` hoàn toàn trùng khớp toán học với ma trận nhầm lẫn.

---

## 8. ĐÁNH GIÁ THỰC NGHIỆM BINARY PSO

### 8.1. Cài đặt thuật toán ([src/models/pso_optimizer.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/models/pso_optimizer.py))
- **Mã hóa:** Vector nhị phân $x_i \in \{0, 1\}^D$ với số chiều $D = 63$.
- **Cập nhật vận tốc:** Vector liên tục với hệ số quán tính $w = 0.729$, hệ số nhận thức $c_1 = 1.494$, hệ số xã hội $c_2 = 1.494$, kẹp biên vận tốc $v_{\max} = 4.0$.
- **Hàm chuyển đổi:** Sigmoid $\text{Prob} = \frac{1}{1 + e^{-v}}$, vị trí cập nhật theo phép thử Bernoulli.
- **Xử lý biên rỗng:** Nếu hạt chọn 0 đặc trưng, tự động bật ngẫu nhiên 1 bit đặc trưng (`positions[i, randint] = 1`).
- **Hàm mục tiêu đa tiêu chí:**
  $$\text{Fitness} = \alpha \cdot \text{PR-AUC} + (1 - \alpha) \cdot \left(1 - \frac{k}{D}\right)$$
  với $\alpha = 0.92$, $k$ là số đặc trưng được chọn, $D = 63$.
- **Proxy model:** `LogisticRegression(class_weight='balanced')` huấn luyện trên 20,000 mẫu inner train và đánh giá trên 10,000 mẫu inner val.
- **Ngân sách tìm kiếm:** 16 hạt $\times$ 12 vòng lặp = 208 lần đánh giá objective (207 unique masks do caching 1 mask trùng). Thời gian tìm kiếm: **11.79 giây**.

### 8.2. Tiến trình hội tụ thực tế ([pso_convergence.csv](file:///d:/HuyD/Đại%20Học/BigData/Global/outputs/feature_selection/pso_convergence.csv))
- **Khởi tạo (Vòng 0):** Best Fitness = 0.2785, số đặc trưng = 22.
- **Vòng 4:** Best Fitness tăng lên 0.2810, số đặc trưng giảm xuống 20.
- **Vòng 6:** Best Fitness tăng lên 0.2835, số đặc trưng giảm xuống 18.
- **Vòng 9 – 12:** Best Fitness đạt đỉnh **0.2848**, số đặc trưng chốt ở **17**.
- Tỷ lệ tinh giản không gian đặc trưng: $1 - \frac{17}{63} = \mathbf{73.02\%}$.

### 8.3. So sánh khách quan: ANOVA vs Binary PSO vs Full Features

| Mô hình & Không gian đặc trưng | Số đặc trưng | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Thời gian tìm kiếm | Thời gian huấn luyện hạ nguồn | Tổng thời gian thực thi |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E1: Gradient Boosting (Full)** | 63 | 0.2730 | 0.6078 | 0.3558 | 0.2573 | 0.5766 | 0.00s | 17.04s | 17.04s |
| **E2: Gradient Boosting (ANOVA)** | **17** | **0.2759** | **0.6105** | **0.3557** | 0.2566 | **0.5797** | **0.13s** | 6.24s | **6.37s** |
| **E3: Gradient Boosting (PSO)** | **17** | 0.2601 | 0.5894 | 0.3411 | 0.2535 | 0.5209 | 11.79s | **4.50s** | 16.29s |
| **E4: XGBoost (Full)** | 63 | 0.2654 | 0.6006 | 0.3475 | 0.2594 | 0.5262 | 0.00s | 4.40s | 4.40s |
| **E5: XGBoost (PSO)** | **17** | 0.2584 | 0.5846 | 0.3319 | 0.2515 | 0.4879 | 11.79s | **2.07s** | 13.86s |

### 8.4. Phân tích nguyên nhân PSO có PR-AUC thấp hơn ANOVA
1. **Lệch pha giữa Proxy Model và Downstream Model:**
   PSO sử dụng mô hình hồi quy tuyến tính `LogisticRegression` làm hàm đánh giá nhanh. Mô hình tuyến tính chỉ tìm các siêu phẳng phân tách tuyến tính, trong khi Gradient Boosting và XGBoost là các thuật toán cây quyết định dựa trên quan hệ phi tuyến và phân vùng không gian.
2. **Khác biệt danh sách đặc trưng được chọn:**
   - ANOVA chọn trực tiếp các biến có tương quan đơn biến cao nhất: `loyalty_score`, `discount_usage_rate`, `total_cart_additions`, `engagement_score`.
   - PSO loại bỏ `loyalty_score` và `discount_usage_rate`, chỉ giữ lại các biến hành vi gián tiếp (`credit_limit`, `account_age_days`, `total_spend`, `pct_ads_sessions`...). Sự thiếu vắng hai biến có tương quan mạnh nhất khiến PR-AUC của PSO bị giảm 0.0158 điểm so với ANOVA.
3. **Giới hạn không gian tìm kiếm:**
   Với 63 chiều, không gian tìm kiếm là $2^{63} \approx 9.22 \times 10^{18}$ trạng thái. Việc đánh giá 208 mẫu là một xấp xỉ cục bộ.
4. **Ý nghĩa bảo vệ đồ án:**
   Việc thừa nhận ANOVA đạt PR-AUC cao hơn trong khi nhấn mạnh **PSO đạt tốc độ huấn luyện nhanh nhất (2.07s - tăng tốc 2.12x) và độ thưa thớt cao nhất (73%)** thể hiện tư duy phản biện khoa học sâu sắc, biến một kết quả "tưởng như bất lợi" thành một đóng góp thực nghiệm giá trị về sự đánh đổi giữa hiệu năng và chi phí tính toán.

---

## 9. ĐÁNH GIÁ ĐỊNH HƯỚNG VÀ TÍNH HỢP LỆ NGHIÊN CỨU

1. **Câu hỏi nghiên cứu (Research Questions):**
   - Đề tài hoàn toàn có thể bảo vệ thành công nếu định vị đúng đắn câu hỏi nghiên cứu về việc khai phá đặc trưng hành vi và tối ưu hóa đa mục tiêu (Accuracy vs Sparsity).
2. **Những tuyên bố cần tránh tuyệt đối khi báo cáo:**
   - *Không tuyên bố:* "Hệ thống dự đoán chính xác khách hàng sẽ mua hàng trong 30 ngày tới theo chuỗi thời gian thực tế".
   - *Không tuyên bố:* "Binary PSO vượt trội hơn tất cả các phương pháp về PR-AUC".
   - *Cần tuyên bố:* "Nghiên cứu đánh giá thiên hướng mua hàng của khách hàng trên ảnh chụp quan sát hành vi đa bảng; chứng minh Binary PSO mang lại lợi thế vượt trội về việc tinh giản 73% số chiều và tăng tốc huấn luyện hơn 2 lần, trong khi bộ lọc thống kê ANOVA giữ ưu thế về độ chính xác dự đoán thuần túy".

---

## 10. DANH SÁCH VẤN ĐỀ THEO MỨC ĐỘ RỦI RO

### MỨC ĐỘ 1: CRITICAL (Ảnh hưởng đến tính hợp lệ của bài toán nếu diễn giải sai)
1. **Định vị sai bài toán thời gian (Temporal Framing Risk):**
   - *Vị trí:* Khái niệm đề tài và các đoạn mô tả cũ về "cửa sổ dự đoán 30 ngày".
   - *Bằng chứng:* 49.86% sessions và 49.88% transactions diễn ra trước `signup_date`. Tỷ lệ giao dịch trong 30 ngày cuối ở hai nhóm target bằng nhau (7.5% vs 7.4%).
   - *Tác động:* Bị hội đồng phản biện bác bỏ nếu tuyên bố đây là mô hình chuỗi thời gian point-in-time.
   - *Đề xuất:* Giữ vững định nghĩa chuẩn **Observational Snapshot Purchase Propensity Classification** đã đưa vào [docs/DATA_DICTIONARY.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/DATA_DICTIONARY.md) và [docs/BaoCao_NghienCuu_Global_6Phan.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/BaoCao_NghienCuu_Global_6Phan.md).

### MỨC ĐỘ 2: HIGH (Có khả năng gây kết luận sai về thuật toán)
2. **Tuyên bố quá mức về ưu thế của PSO so với ANOVA (PSO Over-claiming Risk):**
   - *Vị trí:* Phần tóm tắt hoặc slide thuyết trình nếu ghi "PSO đạt kết quả dự đoán tốt nhất".
   - *Bằng chứng:* ANOVA đạt PR-AUC **0.2759** (tìm kiếm 0.13s), PSO đạt **0.2601** (tìm kiếm 11.79s).
   - *Tác động:* Sai lệch sự thật thực nghiệm.
   - *Đề xuất:* Trình bày trung thực dưới góc độ Pareto Multi-Objective: ANOVA thắng về PR-AUC, PSO thắng về Sparsity (73%) và Tốc độ huấn luyện hạ nguồn (2.07s).

### MỨC ĐỘ 3: MEDIUM (Ảnh hưởng đến phân phối đặc trưng)
3. **Ngoại lai nặng ở đặc trưng `activity_recency_ratio`:**
   - *Vị trí:* [src/features/build_features.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/features/build_features.py#L51).
   - *Bằng chứng:* Giá trị max vọt lên 432.0; 1,861 khách hàng có tỷ số > 10.0 do `days_since_last_session = 9999` hoặc `account_age_days` nhỏ.
   - *Tác động:* Làm lệch phân phối chuẩn hóa của `StandardScaler`.
   - *Đề xuất:* Trong các phiên bản tương lai, nên áp dụng `np.clip(ratio, 0.0, 5.0)` hoặc RobustScaler.

4. **Giá trị gán mặc định `9999` cho ngày giao dịch cuối:**
   - *Vị trí:* [src/data/integrate_data.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/data/integrate_data.py#L217).
   - *Bằng chứng:* 16,459 khách hàng (8.23%) nhận giá trị 9999 ở `days_since_last_transaction`.
   - *Tác động:* Có thể gây phi tuyến tính giả tạo đối với các mô hình tuyến tính.

### MỨC ĐỘ 4: LOW (Vấn đề kỹ thuật nhỏ)
5. **Đặc trưng phương sai bằng 0 `has_referral_code`:**
   - *Vị trí:* [src/data/integrate_data.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/data/integrate_data.py#L167).
   - *Bằng chứng:* 100% khách hàng mang giá trị 1. Phương sai = 0.
   - *Tác động:* Không gây lỗi vì `StandardScaler` ép về 0, nhưng dư thừa 1 chiều trong 63 biến.

6. **Thiếu tie-breaker trong chọn dominant region / campaign:**
   - *Vị trí:* [src/data/integrate_data.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/data/integrate_data.py#L48).
   - *Bằng chứng:* `ORDER BY COUNT(*) DESC` không có cột phụ (như `ORDER BY COUNT(*) DESC, geo_ip_region ASC`).
   - *Tác động:* Nếu khách hàng có 2 vùng bằng nhau, việc chọn phụ thuộc vào thứ tự quét của DuckDB.

---

## 11. TOP 10 VIỆC ƯU TIÊN CẦN THỰC HIỆN ĐỂ BẢO VỆ ĐỒ ÁN

1. **Thống nhất tuyệt đối định nghĩa bài toán:** Sử dụng thuật ngữ chính thức: *"Phân loại độ nghiêng mua hàng trên ảnh chụp quan sát hành vi đa bảng"* trong toàn bộ báo cáo, slide thuyết trình và lời bảo vệ.
2. **Minh bạch hóa kết quả thực nghiệm PSO vs ANOVA:** Trình bày rõ bảng so sánh E1–E5, giải thích tại sao ANOVA đạt PR-AUC cao hơn (0.2759 vs 0.2601) và định vị giá trị của PSO ở khía cạnh rút gọn chiều (73%) và tăng tốc huấn luyện (2.1x).
3. **Làm rõ 2 không gian đặc trưng:** Phân biệt rõ giữa 180 đặc trưng đã biến đổi One-Hot (dùng cho 7 mô hình Baseline tổng quan) và 63 đặc trưng số liên tục (dùng cho PSO, ANOVA và E1–E5).
4. **Không phóng đại ý nghĩa của các biến nhân khẩu học:** Giữ phân tích EDA khách quan, nêu rõ `customer_tier` và `country_code` có tỷ lệ target gần như đồng đều; các biến mang tín hiệu tốt nhất là `loyalty_score`, `discount_usage_rate`, `cart_to_page_ratio` và `age`.
5. **Bảo toàn tính toàn vẹn của Holdout Artifact:** Tiếp tục duy trì bộ số liệu chuẩn xác 100% trên 32,000 mẫu Holdout ($TN=15,740, FP=9,763, FN=3,078, TP=3,419$) và file metadata `holdout_prediction_metadata.json`.
6. **Giải thích cơ chế chống rò rỉ dữ liệu:** Chuẩn bị sẵn sơ đồ pipeline chứng minh toàn bộ Imputer, Scaler, OneHotEncoder và ANOVA selector chỉ được fit trên 128,000 mẫu Train.
7. **Làm rõ 25,059 giao dịch có items_count = 0:** Chuẩn bị câu trả lời về nghiệp vụ: đây là các giao dịch số/dịch vụ/thẻ quà tặng hoặc lỗi ghi nhận log từ dữ liệu gốc, và pipeline đã xử lý an toàn bằng kỹ thuật cộng 1 ở mẫu số.
8. **Giải thích về 5 biến nhiễu nhân tạo:** Trình bày rõ vai trò của `noise_customer_0` đến `noise_customer_4` như một bài kiểm tra tính vững chắc (Robustness check) để chứng minh thuật toán chọn đặc trưng có loại bỏ được nhiễu hay không.
9. **Kiểm tra độ đồng bộ của Website và Power BI:** Đảm bảo dữ liệu hiển thị trên Web (`web/data/metrics.json`) và Power BI (`outputs/powerbi/`) luôn được sinh tự động từ các tệp CSV chuẩn thông qua script `export_outputs.py`.
10. **Lưu trữ các kịch bản kiểm thử tự động:** Giữ vững bộ test 38 bài trong `tests/` như bằng chứng bảo vệ chất lượng phần mềm và tính tái lập khoa học.

---

## 12. PHẠM VI ĐÃ KIỂM TRA VÀ GIỚI HẠN XÁC MINH

1. **Phạm vi đã kiểm tra toàn diện 100% (Full Verification):**
   - Đọc và kiểm tra schema, kiểu dữ liệu, phân phối, giá trị null, trùng lặp và tính toàn vẹn khóa ngoại trên toàn bộ 8 tệp gốc trong `dataset/` (2,700,300 dòng dữ liệu tổng cộng).
   - Kiểm tra toàn bộ 200,000 dòng và 72 cột trong tệp `outputs/customer_features.parquet`.
   - Kiểm tra toàn bộ 160,000 dòng nhãn `train.csv` và tương quan với 63 đặc trưng số liên tục.
   - Kiểm tra logic 100% các file mã nguồn chính: `clean_data.py`, `integrate_data.py`, `build_features.py`, `split_manager.py`, `pso_optimizer.py`, `feature_selection.py`, `baselines.py`, `train_xgboost.py`, `evaluate.py`, `export_outputs.py`.
   - Kiểm tra toàn bộ ma trận nhầm lẫn và các chỉ số của 32,000 dòng trong `outputs/holdout_predictions.csv`.
   - Chạy kiểm thử thành công toàn bộ 38/38 unit test với `pytest`.

2. **Giới hạn xác minh (Audit Scope Limitations):**
   - Không thể xác minh thuật toán sinh dữ liệu nội bộ ban đầu của tác giả tạo bộ dữ liệu trên Kaggle (nguyên nhân sinh ra các mốc ngày ngẫu nhiên và nhãn target cụ thể của cuộc thi).
   - Tuân thủ quy tắc Read-Only, kiểm toán viên không sửa đổi mã nguồn hoặc tái sinh lại các artifact thực nghiệm hiện có.
