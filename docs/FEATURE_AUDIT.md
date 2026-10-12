# BÁO CÁO KIỂM TOÁN ĐẶC TRƯNG VÀ RÒ RỈ DỮ LIỆU (FEATURE AUDIT & LEAKAGE REPORT)

**Dự án**: Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Mã nguồn**: `hayd6/Global` | **Tệp dữ liệu đầu ra**: `outputs/customer_features.parquet` (72 cột, 200.000 dòng)  
**Ngày kiểm toán**: 12/10/2026 | **Đơn vị kiểm toán**: Machine Learning Engineer & Research Methodology Reviewer  

---

## 1. Bản đồ tổng hợp các nhóm đặc trưng (Feature Taxonomy)

Tập dữ liệu sau bước kỹ thuật đặc trưng gồm **72 cột**, được phân cấp thành các nhóm chức năng rõ ràng:

1. **Khóa nhận dạng & Phân vùng (3 biến)**:
   - `customer_id`: Khóa định danh khách hàng (tuyệt đối bị loại bỏ khỏi mọi ma trận huấn luyện $X$).
   - `split_type`: Chỉ báo `train` (160.000) hoặc `test` (40.000) của dữ liệu thi đấu ban đầu.
   - `target`: Nhãn nhị phân ($0/1$), chỉ có ở 160.000 bản ghi `train`, là biến mục tiêu cần dự đoán.
2. **Nhân khẩu học & Tài khoản (11 biến)**: `age`, `country_code`, `region`, `customer_tier`, `credit_limit`, `loyalty_score`, `email_open_rate`, `discount_usage_rate`, `avg_review_score`, `has_referral_code`, `account_age_days`.
3. **Biến nhiễu nhân tạo kiểm soát (7 biến)**: `noise_customer_0` đến `4`, `avg_noise_trans_0`, `avg_noise_trans_1`.
4. **Hành vi duyệt web tổng hợp (17 biến)**: `sess_count`, `total_session_duration`, `avg_session_duration`, `max_session_duration`, `total_pages_viewed`, `avg_pages_viewed`, `total_cart_additions`, `avg_cart_additions`, `bounce_rate`, 4 biến tỷ lệ nguồn truy cập (`pct_organic_sessions`, `pct_ads_sessions`, `pct_email_sessions`, `pct_social_sessions`), 3 biến tỷ lệ thiết bị (`pct_mobile_sessions`, `pct_desktop_sessions`, `pct_tablet_sessions`), `days_since_last_session`.
5. **Hành vi giao dịch tổng hợp (19 biến)**: `has_transactions`, `trans_count`, `total_spend`, `avg_order_value`, `max_order_value`, `min_order_value`, `total_items_count`, `avg_items_per_order`, `trans_discount_rate`, `high_value_trans_count`, `high_value_trans_ratio`, 4 biến phương thức thanh toán (`pct_credit_card`, `pct_debit_card`, `pct_paypal`, `pct_crypto`), 3 biến tốc độ giao hàng (`pct_standard_shipping`, `pct_express_shipping`, `pct_overnight_shipping`), `days_since_last_transaction`.
6. **Địa lý kinh tế & Chiến dịch (6 biến)**: `average_income`, `urban_ratio`, `internet_penetration`, `region_tier`, `primary_campaign_type`, `primary_campaign_budget`.
7. **Đặc trưng nâng cao & Tương tác hành vi (9 biến)**: `cart_to_page_ratio`, `duration_per_page`, `spend_per_session`, `spend_per_item`, `discount_interaction`, `loyalty_spend_product`, `review_loyalty_score`, `activity_recency_ratio`, `engagement_score`.

---

## 2. Kiểm toán chi tiết từng đặc trưng (Feature-by-Feature Audit)

| Tên đặc trưng | Cấp độ dữ liệu | Bảng & Cột nguồn | Công thức / Quy tắc tính | Quy tắc xử lý NULL | Miền giá trị | Rủi ro rò rỉ (Leakage Risk) |
| :--- | :---: | :---: | :--- | :--- | :---: | :---: |
| `age` | Customer | `customers.age` | Làm sạch chuỗi `'unknown'` $\to$ Integer | Điền trung vị theo `customer_tier` | $[18, 75]$ | Không có |
| `country_code` | Customer | `customers.country_code` | Chuỗi 2 ký tự ISO chuẩn hóa | Không có NULL | 10 giá trị | Không có |
| `region` | Customer | `customers.region` | Tên vùng chuẩn hóa | Không có NULL | 100 giá trị | Không có |
| `customer_tier` | Customer | `customers.customer_tier` | Bronze, Silver, Gold, Platinum | Không có NULL | 4 giá trị | Không có |
| `credit_limit` | Customer | `customers.credit_limit` | Tách bỏ `$` và `,` $\to$ DOUBLE | Không có NULL | $[500, 25000]$ | Không có |
| `loyalty_score` | Customer | `customers.loyalty_score` | Điểm tích lũy chuẩn hóa | Không có NULL | $[0.0, 1.0]$ | Không có |
| `email_open_rate` | Customer | `customers.email_open_rate` | Tỷ lệ mở email tiếp thị | Median Imputation | $[0.0, 1.0]$ | Không có |
| `discount_usage_rate`| Customer | `customers.discount_usage_rate`| Tần suất sử dụng mã giảm giá | Không có NULL | $[0.0, 1.0]$ | Không có |
| `avg_review_score` | Customer | `customers.avg_review_score` | Đánh giá trung bình | Không có NULL | $[1.0, 5.0]$ | Không có |
| `has_referral_code` | Customer | `customers.referral_code` | `referral_code IS NOT NULL` | Gán 0 | $\{0, 1\}$ | Không có |
| `account_age_days` | Customer | `customers.signup_date` | `2024-09-26 - signup_date` | Không có NULL | $[0, 1000]$ | Không có |
| `sess_count` | Aggregated | `sessions.session_id` | `COUNT(*)` theo `customer_id` | Coalesce(0) | $[1, 27]$ | Snapshot Overlap |
| `total_session_duration`| Aggregated| `sessions.session_duration`| `SUM(session_duration)` | Coalesce(0.0) | $\ge 0$ | Snapshot Overlap |
| `avg_session_duration`| Aggregated | `sessions.session_duration`| `AVG(session_duration)` | Coalesce(0.0) | $\ge 0$ | Snapshot Overlap |
| `total_pages_viewed` | Aggregated | `sessions.pages_viewed` | `SUM(TRY_CAST pages_viewed)` | Coalesce(0) | $\ge 0$ | Snapshot Overlap |
| `total_cart_additions`| Aggregated | `sessions.cart_additions`| `SUM(cart_additions)` | Coalesce(0) | $\ge 0$ | Snapshot Overlap |
| `bounce_rate` | Aggregated | `sessions.bounce_flag` | `AVG(is_bounce)` | Coalesce(0.0) | $[0.0, 1.0]$ | Snapshot Overlap |
| `days_since_last_session`| Aggregated| `sessions.session_timestamp`| `2024-09-26 - MAX(timestamp)`| Coalesce(9999) | $[0, 9999]$ | Temporal Limitation |
| `trans_count` | Aggregated | `transactions.transaction_id`| `COUNT(*)` theo `customer_id` | Coalesce(0) | $[0, 12]$ | Snapshot Overlap |
| `has_transactions` | Aggregated | `transactions.transaction_id`| `trans_count > 0` | Coalesce(0) | $\{0, 1\}$ | Snapshot Overlap |
| `total_spend` | Aggregated | `transactions.order_value` | `SUM(order_value)` | Coalesce(0.0) | $\ge 0$ | Snapshot Overlap |
| `avg_order_value` | Aggregated | `transactions.order_value` | `AVG(order_value)` | Coalesce(0.0) | $\ge 0$ | Snapshot Overlap |
| `trans_discount_rate`| Aggregated | `transactions.discount_applied`| `AVG(discount_applied)` | Coalesce(0.0) | $[0.0, 1.0]$ | Snapshot Overlap |
| `high_value_trans_ratio`| Aggregated| `transactions.high_value_flag`| `AVG(high_value_flag)` | Coalesce(0.0) | $[0.0, 1.0]$ | Snapshot Overlap |
| `days_since_last_transaction`| Aggregated| `transactions.transaction_timestamp`| `2024-09-26 - MAX(timestamp)`| Coalesce(9999) | $[0, 9999]$ | Temporal Limitation |
| `cart_to_page_ratio` | Derived | `sessions` (derived) | `cart_additions / (pages + 1.0)`| 0.0 | $\ge 0$ | Không có phép chia 0 |
| `duration_per_page` | Derived | `sessions` (derived) | `duration / (pages + 1.0)` | 0.0 | $\ge 0$ | Không có phép chia 0 |
| `spend_per_session` | Derived | `sessions & trans` | `total_spend / (sess_count + 1.0)`| 0.0 | $\ge 0$ | Không có phép chia 0 |
| `spend_per_item` | Derived | `transactions` (derived) | `total_spend / (items + 1.0)` | 0.0 | $\ge 0$ | Không có phép chia 0 |
| `discount_interaction`| Derived | `customers & trans` | `discount_usage * trans_discount`| 0.0 | $[0.0, 1.0]$ | Không có |
| `loyalty_spend_product`| Derived| `customers & trans` | `loyalty_score * (spend + 1.0)` | 0.0 | $\ge 0$ | Không có |
| `review_loyalty_score`| Derived | `customers` (derived) | `(review / 5.0) * loyalty_score`| 0.0 | $[0.0, 1.0]$ | Không có |
| `activity_recency_ratio`| Derived| `sessions & customers` | `recency / (account_age + 1.0)` | Coalesce | $\ge 0$ | Không có |
| `engagement_score` | Derived | `sessions` (derived) | `LN(1+dur) + LN(1+cart) + LN(1+sess)`| 0.0 | $\ge 0$ | Không có |

---

## 3. Thẩm định rủi ro rò rỉ dữ liệu (Data Leakage Risk Assessment)

### 3.1. Rò rỉ nhãn trực tiếp (Direct Target Leakage)
- **Kiểm chứng**: Cột `target` chỉ xuất hiện ở tập `train.csv`.
- Trong `split_manager.py`, danh sách `drop_cols` loại trừ rõ ràng: `customer_id`, `split_type`, `target`.
- Các kiểm thử `test_target_and_customer_id_strictly_excluded_from_candidate_features` trong `tests/test_edge_cases_and_fixtures.py` đã xác minh rằng `target` và `customer_id` **hoàn toàn vắng mặt** trong không gian đặc trưng đầu vào ($X$).

### 3.2. Rò rỉ qua các phân vùng (Cross-Split Preprocessing Leakage)
- **Nguyên tắc**: Không được dùng dữ liệu của tập Validation/Holdout để tính toán giá trị thống kê của Scaler hoặc Imputer.
- **Hiện trạng đã khắc phục**:
  - `split_manager.py`: Bộ tiền xử lý `SimpleImputer(strategy="median")` và `StandardScaler()` chỉ được gọi phương thức `.fit_transform()` trên `train_idx` (128.000 dòng). Đối với `holdout_idx` (32.000 dòng), pipeline chỉ gọi `.transform()`.
  - `pso_optimizer.py`: Trong quá trình tìm kiếm PSO, đã được đồng nhất để sử dụng `SimpleImputer(strategy="median")` và `StandardScaler()` fit độc quyền trên `sub_tr` (tập con 20k lấy từ Train pool). Holdout 32k không hề bị can thiệp.

### 3.3. Rủi ro rò rỉ thời gian (Temporal Leakage Evaluation)
- Dữ liệu thô không có cột nhãn đi kèm tem thời gian cụ thể (chỉ có nhãn nhị phân $0/1$ cho mỗi khách hàng).
- **Thực tế kiểm chứng**:
  - Các biến giao dịch và phiên truy cập được tính toán dựa trên toàn bộ lịch sử ghi nhận đến ngày `2024-09-26`.
  - Nếu nhãn $target=1$ đại diện cho hành vi mua hàng xảy ra trong quá khứ, các giao dịch trong `transactions.csv` có thể đồng thời là nguyên nhân hoặc là chính giao dịch tạo nên nhãn đó.
  - **Kết luận phương pháp luận**: Dự án **không** khẳng định đã triệt tiêu hoàn toàn temporal leakage vì không thể tạo ra mốc cutoff nhân tạo thiếu căn cứ. Thay vào đó, dự án định nghĩa phạm vi thực nghiệm là **Observational Snapshot Propensity Classification** và khuyến nghị hướng phát triển khi có dữ liệu log thời gian thực.
