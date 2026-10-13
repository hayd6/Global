# BÁO CÁO PHÂN TÍCH KHÁM PHÁ DỮ LIỆU ĐỘC LẬP
## CONTROLLED SYNTHETIC BENCHMARK DATASET (POINT-IN-TIME)

- **Đơn vị thẩm định:** Senior Data Scientist & Experiment Auditor
- **Ngày thực thi:** 13/10/2026 16:50:59
- **Nguồn dữ liệu:** `outputs/controlled_benchmark/`
- **Mã kịch bản thực thi:** `scripts/eda_controlled_benchmark.py`
- **Độ phân giải thời gian thực tế:** `DATE (YYYY-MM-DD)`
- **Trạng thái kiểm toán tổng hợp:** PASS (9/9 hạng mục đạt - 100.0%)

---

## 1. QUY MÔ VÀ DANH MỤC TỆP DỮ LIỆU

Bộ dữ liệu **Controlled Synthetic Benchmark Dataset** được kiểm toán trực tiếp từ thư mục `outputs/controlled_benchmark/`. Toàn bộ các giá trị quy mô và mã băm SHA-256 dưới đây được tính toán động trực tiếp từ các tệp trên đĩa:

| STT | Tên tệp | Vai trò | Số dòng | Số cột | Khóa chính | Kích thước | Mã SHA-256 (rút gọn) |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| 1 | `customers.csv` | Core Entity | 25,000 | 17 | `customer_id` | 2.60 MB | `73f6eac2...` |
| 2 | `sessions.csv` | Event Log | 89,666 | 11 | `session_id` | 5.36 MB | `98e20cb0...` |
| 3 | `transactions.csv` | Event Log | 21,534 | 11 | `transaction_id` | 1.43 MB | `af9a31b8...` |
| 4 | `marketing_campaigns.csv` | Dimension | 50 | 6 | `campaign_id` | 2.65 KB | `fe48fb5d...` |
| 5 | `geo_data.csv` | Dimension | 100 | 5 | `geo_ip_region` | 4.16 KB | `9e889ff1...` |
| 6 | `customer_labels_pit.csv` | Target Label | 25,000 | 2 | `customer_id` | 208.90 KB | `ec49cf9c...` |
| 7 | `customer_features_pit.parquet` | Feature Store | 25,000 | 71 | `customer_id` | 3.29 MB | `16b2bb90...` |

> *Hình minh họa quy mô:* `outputs/controlled_benchmark/eda/eda_1_table_scales.png`

---

## 2. CHẤT LƯỢNG DỮ LIỆU VÀ TOÀN VẸN THAM CHIẾU (REFERENTIAL INTEGRITY)

1. **Khóa chính và Dòng trùng lặp:**
   - 100% các bảng thỏa mãn tính duy nhất của khóa chính: số khóa trùng lặp = **0**, số khóa rỗng = **0** (`primary_key_uniqueness`: **PASS**).
   - Số dòng trùng lặp hoàn toàn trên toàn bộ các cột = **0** (`full_row_duplicates`: **PASS**).
2. **Khóa ngoại và Bản ghi mồ côi (Orphan Records):**
   - Sessions $\to$ Customers: **0** bản ghi mồ côi.
   - Transactions $\to$ Customers: **0** bản ghi mồ côi.
   - Sessions $\to$ Marketing Campaigns: **0** bản ghi mồ côi.
   - Sessions $\to$ Geo Data: **0** bản ghi mồ côi.
   - Labels $\leftrightarrow$ Customers: **0** bản ghi mồ côi hai chiều (khớp 1:1 đủ 25,000 khách hàng).
   - Trạng thái toàn vẹn khóa ngoại: **PASS**.
3. **Phân tích Giá trị Thiếu (Missing Values):**
| `referral_code` | `customers.csv` | 16,242 | **64.97%** |
| `campaign_id` | `sessions.csv` | 49,324 | **55.01%** |
| `email_open_rate` | `customers.csv` | 2,532 | **10.13%** |
| `email_open_rate` | `customer_features_pit.parquet` | 2,532 | **10.13%** |
   - **Thống kê tổng hợp thuộc tính:** Trong tổng số 123 thuộc tính được kiểm toán trên toàn bộ 7 bảng, có 4 cột chứa giá trị khuyết thiếu tự nhiên và 119 cột đạt tỷ lệ hoàn chỉnh 100.0% (tỷ lệ thiếu = 0.00%).
   - *Diễn giải nghiệp vụ:* Việc thiếu giá trị ở `referral_code` (khách hàng không qua giới thiệu), `campaign_id` (phiên truy cập tự nhiên organic/direct) và `email_open_rate` (khách chưa đăng ký nhận thư) hoàn toàn phản ánh đặc trưng tự nhiên của bài toán thương mại điện tử.

> *Hình minh họa giá trị thiếu:* `outputs/controlled_benchmark/eda/eda_3_missing_values.png`

---

## 3. PHÂN BỐ NHÃN MỤC TIÊU VÀ ĐỐI CHIẾU LONGITUDINAL POINT-IN-TIME

- **Độ phân giải thời gian:** Dữ liệu có độ phân giải theo ngày (`DATE`).
- **Mốc chốt đặc trưng ($t_0$):** Sau khi kết thúc ngày `2024-06-01`.
- **Cửa sổ nhãn tương lai:** 30 ngày, từ ngày `2024-06-02` đến hết ngày `2024-07-01` ($[2024-06-02, 2024-07-01]$).
- **Thống kê nhãn mục tiêu:**
   - Nhãn âm ($Y_i = 0$): **22,805 khách hàng** (**91.22%**).
   - Nhãn dương ($Y_i = 1$): **2,195 khách hàng** (**8.78%**).
- **Kiểm chứng truy nguyên đối chiếu (Reconciliation Audit):**
   - Số lượng khách hàng duy nhất có giao dịch thực tế phát sinh trong khoảng $[2024-06-02, 2024-07-01]$ trong `transactions.csv` = **2,195**.
   - Số trường hợp sai lệch giữa nhãn $Y_i$ và dữ liệu giao dịch tương lai = **0**.
   - Tỷ lệ khớp đối chiếu thực tế: **100.00%** (25,000/25,000 khách hàng).
   - Khẳng định: **Tỷ lệ nhãn dương 8.78% được chứng minh bằng dữ liệu thực nghiệm.**

> *Hình minh họa phân bố nhãn:* `outputs/controlled_benchmark/eda/eda_2_target_distribution_pit.png`

---

## 4. PHÂN TÍCH ĐẶC TRƯNG HÀNH VI VÀ TƯƠNG QUAN

1. **Khác biệt hành vi theo Nhãn Mục tiêu (Số liệu tính thực tế từ Feature Store):**
   - **Lượt thêm giỏ hàng (`total_cart_additions`):** Nhóm Mua ($Y=1$) đạt trung bình **3.45 lượt**, so với **2.17 lượt** ở nhóm Không mua ($Y=0$) (chênh lệch **1.59 lần**).
   - **Thời lượng duyệt web (`total_session_duration`):** Nhóm Mua đạt trung bình **890.87 giây**, so với **563.68 giây** ở nhóm Không mua (chênh lệch **1.58 lần**).
   - **Tổng chi tiêu lịch sử (`total_spend`):** Nhóm Mua đạt trung bình **$180.31**, so với **$98.12** ở nhóm Không mua (chênh lệch **1.84 lần**).
   - **Số trang đã xem (`total_pages_viewed`):** Nhóm Mua đạt trung bình **22.82 trang**, so với **15.42 trang** ở nhóm Không mua (chênh lệch **1.48 lần**).
2. **Ma trận Tương quan Tuyến tính (Pearson):**
   - Tương quan tuyến tính đơn biến với nhãn mục tiêu nằm trong khoảng thực tế điển hình của dữ liệu hành vi e-commerce:
     - `total_session_duration`: $r = 0.1506$
     - `total_pages_viewed`: $r = 0.1437$
     - `total_spend`: $r = 0.1355$
     - `total_cart_additions`: $r = 0.1351$
   - Phát hiện các cặp biến đa cộng tuyến rất cao:
     - `total_pages_viewed` và `total_session_duration`: $r = 0.9695$.
     - `total_spend` và `trans_count`: $r = 0.9136$.
   - **Nhận định khoa học thận trọng:** Sự xuất hiện của các cặp biến đa cộng tuyến mạnh ($r > 0.90$) chỉ ra sự tồn tại của lượng lớn thông tin dư thừa trong không gian thuộc tính ban đầu. Đây là cơ sở thực nghiệm thúc đẩy việc áp dụng các kỹ thuật chọn đặc trưng (như PSO hoặc ANOVA) nhằm loại bỏ biến trùng lặp. Tuy nhiên, khả năng thuật toán BPSO duy trì hay cải thiện PR-AUC trong khi giảm số chiều là một giả thuyết thực nghiệm cần được chứng minh bằng kết quả mô hình hóa ở Phần 4, không thể suy diễn đơn thuần từ phân tích tương quan EDA.
   - Các biến nhiễu nhân tạo (`noise_customer_0` đến `noise_customer_4`) có tương quan với nhãn dao động sát 0 từ **-0.0050** đến **0.0026** (hoàn toàn là nhiễu trắng ngẫu nhiên).

> *Hình minh họa phân bố và tương quan:*  
> - `outputs/controlled_benchmark/eda/eda_4_numeric_distributions.png`  
> - `outputs/controlled_benchmark/eda/eda_5_correlation_heatmap.png`  
> - `outputs/controlled_benchmark/eda/eda_6_feature_comparison_by_target.png`  
> - `outputs/controlled_benchmark/eda/eda_8_cart_and_engagement_matrix.png`

---

## 5. KIỂM ĐỊNH TÍNH CHÂN THỰC THỜI GIAN VÀ CHỐNG RÒ RỈ DỮ LIỆU (ANTI-LEAKAGE)

1. **Bảo toàn tính nhân quả (Temporal Invariants):**
   - 100% phiên duyệt web phát sinh sau ngày đăng ký tài khoản (`signup_date`): **0 vi phạm** (`temporal_invariants`: **PASS**).
   - 100% giao dịch phát sinh sau ngày đăng ký tài khoản: **0 vi phạm**.
   - 100% khách hàng đăng ký trước mốc chốt $t_0$: **0 vi phạm**.
2. **Cách ly cửa sổ thời gian (Cutoff Isolation & Anti-Leakage):**
   - Bảng đặc trưng `customer_features_pit.parquet` chỉ tổng hợp các sự kiện có `timestamp <= 2024-06-01`.
   - Tổng giao dịch lịch sử trước mốc chốt: **19,061 giao dịch**.
   - Tổng giao dịch tính trong `customer_features_pit.parquet` (`SUM(trans_count)`): **19,061 giao dịch** (Khớp, sai lệch = 0).
   - Tổng số giao dịch trong cửa sổ tương lai (2,473 giao dịch từ ngày 2024-06-02 đến 2024-07-01) hoàn toàn **không xuất hiện** trong không gian đặc trưng (`point_in_time_isolation`: **PASS**).
3. **Đối chiếu cấp khách hàng từng bản ghi (Customer-level Parity Audit):**
   - Khóa khách hàng `customer_id` và nhãn `target` khớp thứ tự và giá trị 100% giữa các bảng (`customer_id_and_target_alignment`: **PASS**).
   - So sánh từng khách hàng (25,000 khách hàng) giữa sự kiện thô và bảng đặc trưng: sai lệch tối đa trên `trans_count`, `total_spend`, `total_items_count`, `sess_count`, `total_session_duration`, `total_pages_viewed`, `total_cart_additions`, `days_since_last_session`, `days_since_last_transaction` đạt **0.0** (`customer_level_aggregation_parity`: **PASS**).
4. **Phân tách không gian thuộc tính dự báo:**
   - Không gian đặc trưng dự báo (candidate predictors) gồm đúng **68 đặc trưng** (64 biến số liên tục, 4 biến phân loại).
   - Các trường định danh (`customer_id`), nhãn mục tiêu tương lai (`target`) và cờ phân chia quản trị (`split_type`) hoàn toàn bị cô lập khỏi tập biến đầu vào của mô hình (`feature_space_cleanliness`: **PASS**).

> *Hình minh họa chuỗi thời gian:* `outputs/controlled_benchmark/eda/eda_7_temporal_activity.png`

---

## 6. DANH MỤC ARTIFACT ĐẦU RA VÀ KHẢ NĂNG TÁI LẬP

Tất cả các tệp đầu ra được lưu trữ độc lập tại `outputs/controlled_benchmark/eda/`, hoàn toàn tách biệt khỏi các artifact của snapshot 200k ban đầu:

1. `data_inventory.csv`: Danh mục 7 tệp dữ liệu, kích thước và mã hash SHA-256 thực tế.
2. `data_quality.csv`: Thống kê giá trị thiếu, tính duy nhất của khóa và dòng trùng lặp trên 123 thuộc tính.
3. `target_distribution.csv`: Tỷ lệ nhãn mục tiêu 8.78% đã xác minh đối chiếu.
4. `numeric_summary.csv`: Thống kê mô tả 64 biến số dự báo (phân định rõ với trường `target`).
5. `categorical_summary.csv`: Tần suất và tỷ lệ phần trăm của các biến phân loại.
6. `correlation_matrix.csv`: Ma trận tương quan 24 đặc trưng chủ chốt.
7. 8 tệp biểu đồ định dạng PNG chất lượng cao (200 DPI), tạo động 100% không hardcode.
8. `eda_manifest.json`: Siêu dữ liệu kiểm toán, bộ kiểm tra 9 hạng mục động và mã băm toàn vẹn.
9. `eda_run.log`: Nhật ký ghi chép chi tiết quá trình thực thi.

---
*Báo cáo được tạo tự động và tính toán động hoàn toàn bởi pipeline `scripts/eda_controlled_benchmark.py` — Bảo toàn tính tái lập 100%.*
