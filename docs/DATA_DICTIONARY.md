# DATA DICTIONARY — TỪ ĐIỂN DỮ LIỆU THỰC TẾ

Tài liệu này phản ánh cấu trúc schema và ý nghĩa từng trường dựa trên việc kiểm tra trực tiếp 8 tệp dữ liệu CSV trong thư mục `dataset/`.

---

## 1. Bảng `customers.csv` (200,000 dòng, 17 cột)

| Tên trường | Kiểu dữ liệu gốc | Ý nghĩa nghiệp vụ | Trạng thái xác minh & Ghi chú |
| :--- | :--- | :--- | :--- |
| `customer_id` | BIGINT | Định danh duy nhất của khách hàng | Đã xác minh. Khóa chính. |
| `age` | VARCHAR | Độ tuổi khách hàng | Đã xác minh. Có giá trị bất thường: `'unknown'` và số nguyên dạng chuỗi. Cần làm sạch chuyển sang kiểu số, xử lý missing. |
| `country_code` | VARCHAR | Mã quốc gia khách hàng | Đã xác minh. Mã ISO 2 ký tự. |
| `region` | VARCHAR | Vùng địa lý nội bộ | Đã xác minh. |
| `signup_date` | DATE | Ngày đăng ký tài khoản | Đã xác minh. Khoảng thời gian: 2022-01-01 đến 2024-09-26. |
| `loyalty_score` | DOUBLE | Điểm tích lũy lòng trung thành | Đã xác minh. Phân phối liên tục [0, 1]. |
| `email_open_rate` | DOUBLE | Tỷ lệ mở email tiếp thị | Đã xác minh. Phân phối liên tục [0, 1]. |
| `discount_usage_rate` | DOUBLE | Tỷ lệ sử dụng voucher / giảm giá | Đã xác minh. Phân phối liên tục [0, 1]. |
| `avg_review_score` | DOUBLE | Điểm đánh giá trung bình của khách hàng | Đã xác minh. Điểm từ 1.0 đến 5.0. |
| `referral_code` | VARCHAR | Mã giới thiệu khi đăng ký | Đã xác minh. Có nhiều giá trị thiếu/trống. |
| `customer_tier` | VARCHAR | Phân hạng khách hàng | Đã xác minh. Giá trị: Bronze, Silver, Gold, Platinum. |
| `credit_limit` | DOUBLE | Hạn mức tín dụng mua sắm | Đã xác minh. Giá trị số liên tục. |
| `noise_customer_0` | DOUBLE | Biến nhiễu nhân tạo 0 | Đã xác minh. Đặc trưng nhiễu ngẫu nhiên đưa vào nhằm thử thách thuật toán Feature Selection. |
| `noise_customer_1` | DOUBLE | Biến nhiễu nhân tạo 1 | Đã xác minh. Biến nhiễu ngẫu nhiên. |
| `noise_customer_2` | DOUBLE | Biến nhiễu nhân tạo 2 | Đã xác minh. Biến nhiễu ngẫu nhiên. |
| `noise_customer_3` | DOUBLE | Biến nhiễu nhân tạo 3 | Đã xác minh. Biến nhiễu ngẫu nhiên. |
| `noise_customer_4` | DOUBLE | Biến nhiễu nhân tạo 4 | Đã xác minh. Biến nhiễu ngẫu nhiên. |

---

## 2. Bảng `geo_data.csv` (100 dòng, 5 cột)

| Tên trường | Kiểu dữ liệu gốc | Ý nghĩa nghiệp vụ | Trạng thái xác minh & Ghi chú |
| :--- | :--- | :--- | :--- |
| `geo_ip_region` | VARCHAR | Định danh vùng địa lý IP | Đã xác minh. Khóa liên kết với `sessions.csv`. |
| `average_income` | DOUBLE | Thu nhập bình quân của vùng | Đã xác minh. Giá trị kinh tế vĩ mô. |
| `urban_ratio` | DOUBLE | Tỷ lệ dân cư đô thị | Đã xác minh. Giá trị [0, 1]. |
| `internet_penetration`| DOUBLE | Tỷ lệ phủ sóng Internet | Đã xác minh. Giá trị [0, 1]. |
| `region_tier` | VARCHAR | Phân cấp phát triển khu vực | Đã xác minh. Giá trị phân loại (Tier 1, Tier 2, Tier 3). |

---

## 3. Bảng `marketing_campaigns.csv` (200 dòng, 6 cột)

| Tên trường | Kiểu dữ liệu gốc | Ý nghĩa nghiệp vụ | Trạng thái xác minh & Ghi chú |
| :--- | :--- | :--- | :--- |
| `campaign_id` | BIGINT | Mã chiến dịch marketing | Đã xác minh. Khóa liên kết với `sessions.csv`. |
| `campaign_type` | VARCHAR | Hình thức chiến dịch | Đã xác minh. Search, Social, Email, Display... |
| `campaign_budget` | VARCHAR | Ngân sách chiến dịch | Đã xác minh. Chuỗi ký tự có định dạng tiền tệ kèm dấu phẩy (vd: `"$46,187"`). Cần chuẩn hóa sang kiểu số. |
| `region_target` | VARCHAR | Khu vực mục tiêu của chiến dịch | Đã xác minh. |
| `start_date` | DATE | Ngày khởi động chiến dịch | Đã xác minh. |
| `end_date` | DATE | Ngày kết thúc chiến dịch | Đã xác minh. |

---

## 4. Bảng `sessions.csv` (2,000,000 dòng, 11 cột)

| Tên trường | Kiểu dữ liệu gốc | Ý nghĩa nghiệp vụ | Trạng thái xác minh & Ghi chú |
| :--- | :--- | :--- | :--- |
| `session_id` | BIGINT | Khóa chính phiên truy cập | Đã xác minh. |
| `customer_id` | BIGINT | Định danh khách hàng sở hữu phiên | Đã xác minh. Khóa ngoại liên kết `customers.csv`. |
| `session_timestamp` | DATE | Thời điểm diễn ra phiên | Đã xác minh. Khoảng thời gian: 2022-01-01 đến 2024-09-26. |
| `session_duration` | DOUBLE | Thời gian phiên duyệt web (giây) | Đã xác minh. |
| `pages_viewed` | VARCHAR | Số trang web đã xem | Đã xác minh. Chứa chuỗi `'N/A'` và số nguyên dạng chuỗi. Cần làm sạch sang số. |
| `cart_additions` | BIGINT | Số lần bấm thêm vào giỏ hàng | Đã xác minh. |
| `bounce_flag` | VARCHAR | Cờ báo hiệu người dùng thoát ngay | Đã xác minh. Dữ liệu hỗn hợp: `'Yes'`, `'No'`, `'1'`, `'0'`, `'TRUE'`, `'FALSE'`. Cần chuẩn hóa về nhị phân 0/1. |
| `traffic_source` | VARCHAR | Kênh chuyển đổi người dùng | Đã xác minh. Organic, Paid, Direct, Referral. |
| `device_type` | VARCHAR | Thiết bị sử dụng | Đã xác minh. Mobile, Desktop, Tablet. |
| `campaign_id` | BIGINT | Chiến dịch tiếp thị dẫn người dùng tới | Đã xác minh. Khóa ngoại liên kết `marketing_campaigns.csv`. |
| `geo_ip_region` | VARCHAR | Vùng IP phát hiện khi truy cập | Đã xác minh. Khóa ngoại liên kết `geo_data.csv`. |

---

## 5. Bảng `transactions.csv` (500,000 dòng, 11 cột)

| Tên trường | Kiểu dữ liệu gốc | Ý nghĩa nghiệp vụ | Trạng thái xác minh & Ghi chú |
| :--- | :--- | :--- | :--- |
| `transaction_id` | BIGINT | Khóa chính giao dịch | Đã xác minh. |
| `customer_id` | BIGINT | Mã khách hàng thực hiện giao dịch | Đã xác minh. Khóa ngoại liên kết `customers.csv`. |
| `transaction_timestamp`| DATE | Thời điểm hoàn tất giao dịch | Đã xác minh. Khoảng thời gian: 2022-01-01 đến 2024-09-26. |
| `order_value` | VARCHAR | Giá trị thanh toán của đơn hàng | Đã xác minh. Chuỗi định dạng ký hiệu tiền tệ (vd: `"$20.39"`). Cần chuẩn hóa sang kiểu số. |
| `items_count` | BIGINT | Số sản phẩm trong đơn | Đã xác minh. |
| `payment_method` | VARCHAR | Phương thức thanh toán | Đã xác minh. `credit_card`, `debit_card`, `paypal`, `crypto`. |
| `discount_applied` | VARCHAR | Đơn hàng có áp dụng giảm giá không | Đã xác minh. Dữ liệu hỗn hợp: `'Yes'`, `'No'`, `'1'`, `'0'`, `'TRUE'`, `'FALSE'`. Cần chuẩn hóa về nhị phân 0/1. |
| `shipping_speed` | VARCHAR | Phương thức vận chuyển đã chọn | Đã xác minh. `standard`, `express`, `overnight`. |
| `high_value_flag` | BOOLEAN | Cờ đánh dấu đơn hàng giá trị cao | Đã xác minh. Cờ nhị phân boolean. Kiểm tra kỹ nguy cơ data leakage. |
| `noise_trans_0` | DOUBLE | Biến nhiễu nhân tạo giao dịch 0 | Đã xác minh. Biến nhiễu ngẫu nhiên. |
| `noise_trans_1` | DOUBLE | Biến nhiễu nhân tạo giao dịch 1 | Đã xác minh. Biến nhiễu ngẫu nhiên. |

---

## 6. Bảng `train.csv`, `test.csv`, `sample_submission.csv`

| Bảng | Tên trường | Kiểu dữ liệu | Ý nghĩa | Ghi chú |
| :--- | :--- | :--- | :--- | :--- |
| `train.csv` (160,000 dòng) | `customer_id` | BIGINT | Khóa khách hàng | Khớp tập khách hàng huấn luyện. |
| | `target` | BIGINT | Nhãn mục tiêu nhị phân | Nhãn 1 chiếm 20.30% (32,486 dòng), nhãn 0 chiếm 79.70% (127,514 dòng). Mất cân bằng lớp. |
| `test.csv` (40,000 dòng) | `customer_id` | BIGINT | Khóa khách hàng | 40,000 khách hàng trong tập kiểm tra độc lập. |
| `sample_submission.csv` | `customer_id`, `target` | BIGINT | Định dạng mẫu nộp bài | Mẫu dự đoán cho tập test. |

---

## 7. Xác minh định nghĩa bài toán, Cutoff thời gian và Giới hạn nghiên cứu

### 7.1. Kết quả kiểm toán thực nghiệm về Target và Cửa sổ 30 ngày
- Kiểm toán dữ liệu thực nghiệm cho thấy: Tỷ lệ khách hàng phát sinh giao dịch trong 30 ngày cuối (từ 2024-08-27 đến 2024-09-26) ở nhóm `target = 1` là **7.44%** (2,418 / 32,486 khách), trong khi ở nhóm `target = 0` là **7.58%** (9,666 / 127,514 khách). Đồng thời, tỷ lệ khách hàng từng có ít nhất 1 giao dịch ở cả hai nhóm là hoàn toàn đồng nhất (**91.79%**).
- **Kết luận khoa học**: Nhãn `target` **không** được sinh ra từ các giao dịch trong 30 ngày cuối của bảng `transactions.csv`.

### 7.2. Định nghĩa phạm vi bài toán phù hợp
- Do bộ dữ liệu nguồn không cung cấp mốc thời gian chốt dự đoán (prediction cutoff) hay tài liệu sinh nhãn chính thức, nghiên cứu xác định chuẩn xác phạm vi bài toán là:
  > **"Phân loại thiên hướng mua hàng của khách hàng (Customer Purchase Propensity Classification) dựa trên snapshot dữ liệu hành vi thương mại điện tử đa bảng."**
- Không tuyên bố hệ thống là mô hình chuỗi thời gian dự báo tương lai point-in-time nếu không có bằng chứng cutoff nguồn. Các đặc trưng tổng hợp từ `sessions.csv` và `transactions.csv` được hiểu là đặc trưng tóm lược hành vi quan sát trên toàn bộ snapshot.
- Toàn bộ pipeline loại bỏ hoàn toàn `customer_id` và `target` khỏi ma trận đầu vào để đảm bảo tính hợp lệ.

