# BÁO CÁO KIỂM TOÁN CHẤT LƯỢNG DỮ LIỆU GỐC (DATA QUALITY REPORT)

**Dự án**: Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Mã nguồn**: `hayd6/Global` | **Môi trường thực thi**: Windows Python 3.14 + DuckDB  
**Ngày kiểm toán**: 12/10/2026 | **Đơn vị kiểm toán**: Senior Data Quality Auditor  

---

## 1. Tổng quan kho dữ liệu nguồn (Source Inventory)

Kiểm tra toàn bộ 8 tệp CSV tại `dataset/`. Thư mục này tuân thủ nguyên tắc **READ-ONLY** theo `AGENTS.md`.

| Tên bảng CSV | Kích thước vật lý | Số dòng (Rows) | Số cột (Cols) | Khóa chính (PK) | Số dòng trùng hoàn toàn |
| :--- | :---: | :---: | :---: | :--- | :---: |
| `customers.csv` | 42.08 MB | 200,000 | 17 | `customer_id` | 0 |
| `geo_data.csv` | 0.01 MB | 100 | 5 | `geo_ip_region` | 0 |
| `marketing_campaigns.csv` | 0.01 MB | 200 | 6 | `campaign_id` | 0 |
| `sessions.csv` | 148.78 MB | 2,000,000 | 11 | `session_id` | 0 |
| `transactions.csv` | 46.71 MB | 500,000 | 11 | `transaction_id` | 0 |
| `train.csv` | 1.29 MB | 160,000 | 2 | `customer_id` | 0 |
| `test.csv` | 0.25 MB | 40,000 | 1 | `customer_id` | 0 |
| `sample_submission.csv` | 0.32 MB | 40,000 | 2 | `customer_id` | 0 |

---

## 2. Kiểm toán chi tiết từng bảng dữ liệu (Table-Level Audit)

### 2.1. Bảng `customers.csv` (200.000 dòng, 17 cột)
- **Khóa chính**: `customer_id` — Đơn nhất 200.000 giá trị, 0 NULL, 0 trùng lặp.
- **Phân tích thuộc tính**:
  - `age`: Kiểu vật lý thô `VARCHAR`. Có chính xác **10.000 giá trị placeholder (`unknown`)** (chiếm 5.00%). Trong pipeline `clean_data.py`, được chuẩn hóa bằng `TRY_CAST(NULLIF(TRIM(age), 'unknown') AS INTEGER)` chuyển thành `NULL` và sau đó được điền giá trị trung vị theo phân nhóm (`customer_tier`).
  - `country_code`: 10 quốc gia phân biệt, 0 NULL. Phổ biến nhất: `US`.
  - `region`: 100 khu vực phân biệt, 0 NULL.
  - `signup_date`: 1.000 ngày phân biệt (từ 2022-01-01 đến 2024-09-26), 0 NULL.
  - `loyalty_score`: Giá trị thực trong khoảng $[0.0, 1.0]$, 0 NULL.
  - `email_open_rate`: Tỷ lệ mở email thực tế có **22.746 giá trị NULL** (chiếm 11.373%). Không chứa placeholder chuỗi. Được gán trung vị (median) khi chuẩn hóa mô hình.
  - `discount_usage_rate`, `avg_review_score`: Phân phối liên tục chuẩn, 0 NULL.
  - `referral_code`: Có 20.741 chuỗi rỗng (`''`), đại diện cho khách hàng đăng ký tự nhiên (không qua mã giới thiệu). Được chuyển đổi an toàn thành biến chỉ báo nhị phân `has_referral_code` (0 hoặc 1).
  - `customer_tier`: 4 phân hạng (`Bronze`, `Silver`, `Gold`, `Platinum`), 0 NULL.
  - `credit_limit`: Định dạng chuỗi chứa ký tự tiền tệ và dấu phẩy ngăn cách hàng nghìn (ví dụ `$1,500.00`). Được làm sạch bằng `REPLACE` loại bỏ `$` và `,` rồi ép kiểu sang `DOUBLE` (200.000 giá trị hợp lệ, min = $500, max = $25.000).
  - `noise_customer_0` đến `noise_customer_4`: 5 biến nhiễu Gaussian nhân tạo được đưa vào để thẩm định năng lực lọc nhiễu của PSO.

### 2.2. Bảng `sessions.csv` (2.000.000 dòng, 11 cột)
- **Khóa chính**: `session_id` — 2.000.000 giá trị đơn nhất, 0 NULL.
- **Khóa ngoại**: `customer_id` — Đối chiếu với `customers.csv`: **0 khách hàng mồ côi (Zero orphan records)**.
- **Phân tích thuộc tính**:
  - `session_duration`: Thời lượng phiên tính bằng giây, giá trị dương hợp lệ.
  - `pages_viewed`: Chứa chuỗi placeholder `'N/A'`, được chuyển đổi an toàn bằng `TRY_CAST(NULLIF(TRIM(pages_viewed), 'N/A') AS INTEGER)`.
  - `bounce_flag`: Dữ liệu thô biểu diễn lẫn lộn (`'1'`, `'0'`, `'true'`, `'false'`, `'yes'`, `'no'`). Được chuẩn hóa về số nhị phân $0/1$ trong view `v_cleaned_sessions`.
  - `traffic_source`: Phân loại nguồn (`organic`, `ads`, `email`, `social`), chuẩn hóa chữ thường.
  - `device_type`: Phân loại thiết bị (`mobile`, `desktop`, `tablet`), chuẩn hóa chữ thường.
  - `geo_ip_region`: 100 khu vực phân biệt, khớp 100% với `geo_data.csv`.
  - `campaign_id`: Khóa chiến dịch tiếp thị, khớp 100% với `marketing_campaigns.csv`.

### 2.3. Bảng `transactions.csv` (500.000 dòng, 11 cột)
- **Khóa chính**: `transaction_id` — 500.000 giá trị đơn nhất, 0 NULL.
- **Khóa ngoại**: `customer_id` — Khớp 100% với `customers.csv`, 0 khách hàng mồ côi.
- **Phân tích thuộc tính**:
  - `order_value`: Chứa ký tự `$` và `,`, được chuẩn hóa thành số thực `DOUBLE` không âm.
  - `items_count`: Số lượng sản phẩm mỗi đơn hàng (từ 1 đến 20).
  - `discount_applied`: Biểu diễn hỗn hợp boolean, được chuẩn hóa về $0/1$.
  - `shipping_speed`: Chuẩn hóa chữ thường (`standard`, `express`, `overnight`).
  - `payment_method`: Phương thức thanh toán (`credit_card`, `debit_card`, `paypal`, `crypto`).
  - `noise_trans_0`, `noise_trans_1`: Biến nhiễu giao dịch nhân tạo.

### 2.4. Bảng `geo_data.csv` (100 dòng, 5 cột)
- Khóa chính: `geo_ip_region` — 100 mã vùng duy nhất.
- Thuộc tính kinh tế xã hội: `average_income`, `urban_ratio`, `internet_penetration`, `region_tier` (Tier 1 đến Tier 3). 0 NULL, 0 dị biệt.

### 2.5. Bảng `marketing_campaigns.csv` (200 dòng, 6 cột)
- Khóa chính: `campaign_id` — 200 chiến dịch duy nhất.
- Thuộc tính: `campaign_type`, `campaign_budget` (loại bỏ `$`), `region_target`, `start_date`, `end_date`. 0 NULL.

### 2.6. Bảng nhãn và phân chia thi đấu (`train.csv`, `test.csv`, `sample_submission.csv`)
- `train.csv`: 160.000 dòng.
  - Tỷ lệ nhãn: Class 0 = 127.514 (79,70%), Class 1 = 32.486 (20,30%).
  - Tỷ lệ mất cân bằng lớp (Imbalance Ratio): $127.514 / 32.486 \approx 3,925$.
- `test.csv`: 40.000 dòng, chỉ chứa `customer_id`.
- **Độc lập phân vùng**: Giao giữa `train.csv` và `test.csv` là **chính xác 0 khách hàng**.
- `sample_submission.csv`: 40.000 dòng, thứ tự và định dạng `customer_id` khớp 100% với `test.csv`.

---

## 3. Kiểm toán quan hệ và tính toàn vẹn liên kết (Referential Integrity)

| Cặp liên kết (Join Keys) | Loại quan hệ | Số bản ghi mồ côi (Orphans) | Trạng thái toàn vẹn |
| :--- | :---: | :---: | :---: |
| `sessions.customer_id` $\to$ `customers.customer_id` | N : 1 | 0 | ĐẠT 100% |
| `transactions.customer_id` $\to$ `customers.customer_id` | N : 1 | 0 | ĐẠT 100% |
| `sessions.geo_ip_region` $\to$ `geo_data.geo_ip_region` | N : 1 | 0 | ĐẠT 100% |
| `sessions.campaign_id` $\to$ `marketing_campaigns.campaign_id` | N : 1 | 0 | ĐẠT 100% |
| `train.customer_id` $\to$ `customers.customer_id` | 1 : 1 | 0 | ĐẠT 100% |
| `test.customer_id` $\to$ `customers.customer_id` | 1 : 1 | 0 | ĐẠT 100% |
| `sample_submission.customer_id` $\to$ `test.customer_id` | 1 : 1 | 0 | ĐẠT 100% |

---

## 4. Kiểm toán phân tán hành vi (Behavioral Distribution & Cardinality)

- **Phiên duyệt web (`sessions`) theo khách hàng**:
  - Số phiên tối thiểu: 1 phiên.
  - Số phiên trung bình: **10,00 phiên/khách hàng**.
  - Số phiên tối đa: 27 phiên.
  - Toàn bộ 200.000 khách hàng đều có ít nhất 1 phiên truy cập.
- **Giao dịch mua sắm (`transactions`) theo khách hàng**:
  - Số khách hàng có phát sinh giao dịch: **184.000 khách hàng** (chiếm 92,0%).
  - Số khách hàng chưa có giao dịch (0 đơn hàng): **16.000 khách hàng** (chiếm 8,0%).
  - Đối với nhóm có giao dịch: Trung bình 2,72 đơn hàng/khách hàng (tối thiểu 1, tối đa 12).
- **Phòng chống nhân bản trọng số (Anti-Inflation Proof)**:
  - Nếu thực hiện phép `LEFT JOIN` trực tiếp giữa `customers` và `sessions`/`transactions`, số dòng sẽ bùng nổ theo tích Descartes ($200.000 \times 10 \times 2,72$), làm méo mó phân phối xác suất và vi phạm tính độc lập mẫu.
  - **Quy tắc bắt buộc đã thực thi**: Toàn bộ dữ liệu `sessions` và `transactions` được tổng hợp trước theo `GROUP BY customer_id` trong DuckDB (`v_sessions_agg`, `v_transactions_agg`) trước khi liên kết 1:1 với `customers.csv`.
  - Kết quả kiểm chứng: Bảng hợp nhất có đúng **200.000 dòng**, tương ứng đúng 200.000 khách hàng duy nhất.

---

## 5. Giới hạn cố hữu của dữ liệu nguồn (Source Data Inherent Limitations)

1. **Khuyết thiếu mốc thời gian cắt nhãn (Missing Prediction Cutoff Timestamp)**:
   - Dữ liệu thô không cung cấp thời điểm nhãn $T_{\text{label}}$ được sinh ra. Mốc thời gian lớn nhất ghi nhận trong toàn bộ hệ thống là `2024-09-26`.
   - Do đó, không thể xác định liệu các phiên hoặc giao dịch xảy ra gần mốc `2024-09-26` là nguyên nhân dẫn đến nhãn hay là hệ quả sau khi nhãn đã được gán.
   - **Xử lý phương pháp luận**: Bài toán được định nghĩa chính xác và minh bạch là **Observational Snapshot Propensity Classification** (Phân loại xu hướng trên lát cắt quan sát tĩnh), không thổi phồng thành "Dự đoán mua hàng tương lai 30 ngày".
2. **Biến nhiễu nhân tạo**:
   - Dữ liệu chứa 7 cột nhiễu ngẫu nhiên (`noise_customer_0` đến `4`, `avg_noise_trans_0` và `1`). Đây là thiết kế chủ đích của bài toán thực nghiệm nhằm kiểm chứng khả năng loại bỏ biến rác của thuật toán Binary PSO.
