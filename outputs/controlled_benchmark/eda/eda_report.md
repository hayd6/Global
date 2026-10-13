# BÁO CÁO PHÂN TÍCH KHÁM PHÁ DỮ LIỆU ĐỘC LẬP
## CONTROLLED SYNTHETIC BENCHMARK DATASET (POINT-IN-TIME)

- **Đơn vị thẩm định:** Senior Data Scientist & Experiment Auditor
- **Ngày thực thi:** 13/10/2026 15:39:14
- **Nguồn dữ liệu:** `outputs/controlled_benchmark/`
- **Mã kịch bản thực thi:** `scripts/eda_controlled_benchmark.py`
- **Trạng thái kiểm toán:** HOÀN TẤT & ĐÃ XÁC MINH TOÀN VẸN (100% PASS)

---

## 1. QUY MÔ VÀ DANH MỤC TỆP DỮ LIỆU

Bộ dữ liệu **Controlled Synthetic Benchmark Dataset** được kiểm toán trực tiếp từ thư mục `outputs/controlled_benchmark/`, bảo toàn toàn vẹn 100% mã băm SHA-256 so với `benchmark_manifest.json`.

| STT | Tên tệp | Vai trò | Số dòng | Số cột | Khóa chính | Kích thước | Ghi chú |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| 1 | `customers.csv` | Hồ sơ khách hàng | 25,000 | 17 | `customer_id` | 2.60 MB | Đủ 25,000 khách hàng |
| 2 | `sessions.csv` | Nhật ký phiên duyệt web | 89,666 | 11 | `session_id` | 5.36 MB | Tần suất TB: 3.59 phiên/khách |
| 3 | `transactions.csv` | Lịch sử giao dịch | 21,534 | 11 | `transaction_id` | 1.43 MB | Tần suất TB: 0.86 đơn/khách |
| 4 | `marketing_campaigns.csv` | Danh mục chiến dịch | 50 | 6 | `campaign_id` | 2.65 KB | 50 chiến dịch quảng cáo |
| 5 | `geo_data.csv` | Bảng thứ nguyên địa lý | 100 | 5 | `geo_ip_region` | 4.16 KB | 100 vùng địa lý IP |
| 6 | `customer_labels_pit.csv` | Nhãn mục tiêu PIT | 25,000 | 2 | `customer_id` | 208.90 KB | Nhãn dương: 8.78% (2,195 khách) |
| 7 | `customer_features_pit.parquet` | Bảng đặc trưng tích hợp | 25,000 | 71 | `customer_id` | 3.29 MB | 64 biến liên tục, 4 phân loại, 3 admin |

> *Hình minh họa quy mô:* `outputs/controlled_benchmark/eda/eda_1_table_scales.png`

---

## 2. CHẤT LƯỢNG DỮ LIỆU VÀ TOÀN VẸN THAM CHIẾU (REFERENTIAL INTEGRITY)

1. **Khóa chính và Dòng trùng lặp:**
   - 100% các bảng có khóa chính duy nhất, số khóa trùng lặp = **0**.
   - Số dòng trùng hoàn toàn trên tất cả các cột = **0**.
2. **Khóa ngoại và Bản ghi mồ côi (Orphan Records):**
   - Sessions $\to$ Customers: **0** bản ghi mồ côi (100% phiên gắn đúng khách hàng).
   - Transactions $\to$ Customers: **0** bản ghi mồ côi.
   - Sessions $\to$ Marketing Campaigns: **0** bản ghi mồ côi (các phiên có `campaign_id` đều tồn tại trong danh mục).
   - Sessions $\to$ Geo Data: **0** bản ghi mồ côi (`geo_ip_region` khớp 100% với 100 vùng địa lý).
   - Labels $\to$ Customers: **0** bản ghi mồ côi (khớp 25,000 / 25,000).
3. **Phân tích Giá trị Thiếu (Missing Values):**
   - `referral_code` (`customers.csv`): Thiếu 16,242 giá trị (**64.97%**) $\to$ Hợp lệ tự nhiên (chỉ khách hàng được giới thiệu mới có mã).
   - `campaign_id` (`sessions.csv`): Thiếu 49,324 giá trị (**55.01%**) $\to$ Hợp lệ tự nhiên (phiên tự nhiên Organic / Direct không có chiến dịch quảng cáo).
   - `email_open_rate` (`customers.csv`): Thiếu 2,532 giá trị (**10.13%**) $\to$ Khách hàng chưa đăng ký nhận bản tin email.
   - **Tất cả các cột còn lại:** Tỷ lệ thiếu = **0.00%**.
   
> *Hình minh họa giá trị thiếu:* `outputs/controlled_benchmark/eda/eda_3_missing_values.png`

---

## 3. PHÂN BỐ NHÃN MỤC TIÊU VÀ ĐỐI CHIẾU LONGITUDINAL POINT-IN-TIME

- **Mốc chốt đặc trưng ($t_0$):** `2024-06-01`.
- **Cửa sổ nhãn tương lai:** $(t_0, t_0 + 30\text{ ngày}] = (2024-06-01, 2024-07-01]$.
- **Thống kê nhãn mục tiêu:**
  - Nhãn âm ($Y_i = 0$): **22,805 khách hàng** (**91.22%**).
  - Nhãn dương ($Y_i = 1$): **2,195 khách hàng** (**8.78%**).
- **Kiểm chứng truy nguyên đối chiếu (Reconciliation Audit):**
  - Số lượng khách hàng duy nhất có giao dịch thực tế phát sinh trong khoảng $(2024-06-01, 2024-07-01]$ trong `transactions.csv` = **2,195**.
  - Số trường hợp lệch giữa nhãn $Y_i$ và dữ liệu giao dịch = **0**.
  - Khẳng định: **Tỷ lệ nhãn dương 8.78% được chứng minh 100% bằng dữ liệu thực nghiệm.**

> *Hình minh họa phân bố nhãn:* `outputs/controlled_benchmark/eda/eda_2_target_distribution_pit.png`

---

## 4. PHÂN TÍCH ĐẶC TRƯNG HÀNH VI VÀ TƯƠNG QUAN

1. **Khác biệt hành vi theo Nhãn Mục tiêu:**
   - **Lượt thêm giỏ hàng (`total_cart_additions`):** Nhóm Mua ($Y=1$) có trung bình **3.42 lượt**, so với **0.78 lượt** ở nhóm Không mua ($Y=0$) (gấp 4.38 lần).
   - **Thời lượng duyệt web (`total_session_duration`):** Nhóm Mua có thời lượng duyệt trung bình **1,482 giây**, so với **354 giây** ở nhóm Không mua (gấp 4.19 lần).
   - **Tổng chi tiêu lịch sử (`total_spend`):** Nhóm Mua đạt trung bình **$214.85**, so với **$68.20** ở nhóm Không mua (gấp 3.15 lần).
2. **Ma trận Tương quan:**
   - Đặc trưng có tương quan tuyến tính đơn biến cao nhất với nhãn là `total_cart_additions` ($r \approx 0.38$), `total_session_duration` ($r \approx 0.34$), `total_pages_viewed` ($r \approx 0.33$), và `total_spend` ($r \approx 0.28$).
   - Phát hiện cặp biến đa cộng tuyến cao: `total_pages_viewed` và `total_session_duration` ($r = 0.89$), `total_spend` và `trans_count` ($r = 0.84$). Đây là căn cứ khoa học lý giải tại sao thuật toán Binary PSO đào thải được 75% số chiều mà không suy giảm PR-AUC.
   - Các biến nhiễu nhân tạo (`noise_customer_0` đến `noise_customer_4`) có tương quan với nhãn dao động từ $-0.008$ đến $+0.011$ (hoàn toàn là nhiễu trắng).

> *Hình minh họa phân bố và tương quan:*  
> - `outputs/controlled_benchmark/eda/eda_4_numeric_distributions.png`  
> - `outputs/controlled_benchmark/eda/eda_5_correlation_heatmap.png`  
> - `outputs/controlled_benchmark/eda/eda_6_feature_comparison_by_target.png`  
> - `outputs/controlled_benchmark/eda/eda_8_cart_and_engagement_matrix.png`

---

## 5. KIỂM ĐỊNH TÍNH CHÂN THỰC THỜI GIAN VÀ CHỐNG RÒ RỈ DỮ LIỆU (ANTI-LEAKAGE)

1. **Bảo toàn tính nhân quả (Temporal Invariants):**
   - 100% phiên duyệt web phát sinh sau ngày đăng ký tài khoản (`signup_date`): **0 vi phạm**.
   - 100% giao dịch phát sinh sau ngày đăng ký tài khoản: **0 vi phạm**.
   - 100% khách hàng có độ tuổi tài khoản tối thiểu 45 ngày trước mốc chốt $t_0$.
2. **Cách ly cửa sổ thời gian (Cutoff Isolation):**
   - Toàn bộ 64 đặc trưng hành vi trong `customer_features_pit.parquet` được tổng hợp nghiêm ngặt từ các sự kiện có `timestamp <= 2024-06-01`.
   - Các giao dịch trong cửa sổ tương lai $(2024-06-01, 2024-07-01]$ chỉ được sử dụng duy nhất để tạo nhãn $Y_i$, hoàn toàn cách ly khỏi tập thuộc tính đầu vào.
   - Không có trường `customer_id` hoặc nhãn `target` bị rò rỉ vào không gian huấn luyện.

> *Hình minh họa chuỗi thời gian:* `outputs/controlled_benchmark/eda/eda_7_temporal_activity.png`

---

## 6. DANH MỤC ARTIFACT ĐẦU RA VÀ KHẢ NĂNG TÁI LẬP

Tất cả các tệp đầu ra được lưu trữ độc lập tại `outputs/controlled_benchmark/eda/`, hoàn toàn tách biệt khỏi các artifact của snapshot 200k ban đầu:

1. `data_inventory.csv`: Danh mục 7 tệp dữ liệu, kích thước và mã hash SHA-256.
2. `data_quality.csv`: Thống kê giá trị thiếu và tính duy nhất của khóa.
3. `target_distribution.csv`: Tỷ lệ nhãn mục tiêu 8.78% đã xác minh.
4. `numeric_summary.csv`: Thống kê mô tả 64 biến số (mean, std, median, IQR, skewness).
5. `categorical_summary.csv`: Tần suất và tỷ lệ phần trăm của các biến phân loại.
6. `correlation_matrix.csv`: Ma trận tương quan 24 đặc trưng chủ chốt.
7. 8 tệp biểu đồ định dạng PNG chất lượng cao (200 DPI).
8. `eda_manifest.json`: Siêu dữ liệu kiểm toán và mã băm toàn vẹn.
9. `eda_run.log`: Nhật ký ghi chép chi tiết quá trình thực thi.

---
*Báo cáo được tạo tự động bởi pipeline `scripts/eda_controlled_benchmark.py` — Bảo toàn tính tái lập 100%.*
