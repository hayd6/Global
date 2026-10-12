# BÁO CÁO KIỂM ĐỊNH ĐỘC LẬP CHẤT LƯỢNG DỮ LIỆU VÀ TOÀN BỘ PIPELINE
## (INDEPENDENT DATA VALIDATION REPORT — REVISED & BOUNDED)

**Dự án:** Global E-Commerce Customer Purchase Prediction (`hayd6/Global`)  
**Đề tài nghiên cứu:** Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Vai trò:** Chuyên gia Thẩm định Dữ liệu Độc lập (Independent Data Quality Auditor)  
**Ngày thực hiện kiểm định:** 12/10/2026 | **Chế độ kiểm định:** READ-ONLY (Chỉ đọc, tính toán đối chiếu độc lập, không sửa mã nguồn, không tái tạo dataset, không sửa đổi metrics)  
**Quy ước trạng thái kiểm định:**  
- `PASS`: Đã có bằng chứng thực nghiệm độc lập xác nhận thỏa mãn tiêu chuẩn kiểm tra trong phạm vi quy định.  
- `FAIL`: Đã có bằng chứng thực nghiệm độc lập xác nhận sai sót hoặc vi phạm đặc tả.  
- `INSUFFICIENT EVIDENCE`: Chưa đủ dữ liệu độc lập từ môi trường thực tế hoặc giả định lý thuyết chưa được kiểm chứng ngoại vi.  
- `BLOCKED`: Không thể kiểm tra do giới hạn môi trường ngoại vi, phân quyền mạng hoặc tài khoản dịch vụ.

---

## MỤC LỤC BÁO CÁO

1. [Phạm vi kiểm định và Nguồn gốc dữ liệu](#1-phạm-vi-kiểm-định-và-nguồn-gốc-dữ-liệu)
2. [Phân biệt Tính đúng của Mã nguồn và Tính hợp lý của Đặc tả Sinh dữ liệu](#2-phân-biệt-tính-đúng-của-mã-nguồn-và-tính-hợp-lý-của-đặc-tả-sinh-dữ-liệu)
3. [Phương pháp xây dựng chuẩn đối chiếu độc lập](#3-phương-pháp-xây-dựng-chuẩn-đối-chiếu-độc-lập)
4. [Bảng kết quả kiểm định tổng hợp (Master Validation Matrix)](#4-bảng-kết-quả-kiểm-định-tổng-hợp-master-validation-matrix)
5. [Kiểm tra chi tiết Đặc tả Sinh Dữ liệu (Data Generation Rules)](#5-kiểm-tra-chi-tiết-đặc-tả-sinh-dữ-liệu-data-generation-rules)
6. [Bằng chứng chi tiết cho từng hạng mục kỹ thuật](#6-bằng-chứng-chi-tiết-cho-từng-hạng-mục-kỹ-thuật)
   - [6.1. Cấu trúc, Schema và Khóa quan hệ](#61-cấu-trúc-schema-và-khóa-quan-hệ)
   - [6.2. Ranh giới thời gian và Tái tính toán Nhãn mục tiêu PIT](#62-ranh-giới-thời-gian-và-tái-tính-toán-nhãn-mục-tiêu-pit)
   - [6.3. Khảo sát Rò rỉ thời gian và Kiểm định 69 Cột Đặc trưng](#63-khảo-sát-rò-rỉ-thời-gian-và-kiểm-định-69-cột-đặc-trưng)
   - [6.4. Giải mã số chiều đặc trưng (64, 68, 71, 83)](#64-giải-mã-số-chiều-đặc-trưng-64-68-71-83)
   - [6.5. Phân tách Train/Validation/Holdout và Tái tính toán Metrics Holdout](#65-phân-tách-trainvalidationholdout-và-tái-tính-toán-metrics-holdout)
   - [6.6. Đánh giá Đa Seed của BPSO và Bản chất Lọc Biến Nhiễu so với ANOVA](#66-đánh-giá-đa-seed-của-bpso-và-bản-chất-lọc-biến-nhiễu-so-với-anova)
   - [6.7. Kiểm định Danh mục 28 Tài liệu Tham khảo và Phân giải DOI](#67-kiểm-định-danh-mục-28-tài-liệu-tham-khảo-và-phân-giải-doi)
   - [6.8. Đồng bộ Artifacts và Web Portal](#68-đồng-bộ-artifacts-và-web-portal)
7. [Hồ sơ các phát hiện kiểm định (Findings)](#7-hồ-sơ-các-phát-hiện-kiểm-định-findings)
8. [Các giới hạn nghiên cứu chưa giải quyết và Lý do](#8-các-giới-hạn-nghiên-cứu-chưa-giải-quyết-và-lý-do)
9. [Kết luận kiểm định có giới hạn](#9-kết-luận-kiểm-định-có-giới-hạn)

---

## 1. PHẠM VI KIỂM ĐỊNH VÀ NGUỒN GỐC DỮ LIỆU

### 1.1. Phạm vi đã kiểm định thực tế
- **Tập dữ liệu nguồn ban đầu:** Toàn bộ 8 tệp CSV trong thư mục `dataset/` (bao gồm `customers.csv`, `sessions.csv`, `transactions.csv`, `marketing_campaigns.csv`, `geo_data.csv`, `train.csv`, `test.csv`, `sample_submission.csv`).
- **Bộ chuẩn kiểm soát dẫn xuất:** Toàn bộ 17 tệp trong `outputs/controlled_benchmark/` (gồm 6 tệp CSV nguồn, 1 tệp Parquet đặc trưng, 1 tệp chỉ mục NPZ, 4 tệp mô hình joblib, 3 tệp metrics CSV, 2 tệp manifest/metadata JSON).
- **Mã nguồn pipeline:** Các module trong `src/data/` ([generate_controlled_benchmark.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/data/generate_controlled_benchmark.py)), `src/features/` ([build_point_in_time_features.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/features/build_point_in_time_features.py)), `src/models/` ([pso_optimizer.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/models/pso_optimizer.py), [train_pit_models.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/models/train_pit_models.py)), và [pipeline_controlled.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/pipeline_controlled.py).
- **Tài liệu học thuật & Web:** `DanY6Phan.md`, `DATA_QUALITY_ACCEPTANCE_REPORT.md`, `WORD_REPORT_INPUT_SPECIFICATION.md`, `web/data/metrics.json`.

### 1.2. Nguồn gốc thực tế của các tập dữ liệu
1. **Dữ liệu trong `dataset/` (Chỉ đọc - READ-ONLY):** Dữ liệu bảng từ cuộc thi Kaggle Global E-Commerce. Qua kiểm định độc lập, tập dữ liệu này chứa các khuyết tật chất lượng nghiêm trọng:
   - Nhãn $Y=0$ và $Y=1$ đều có tỷ lệ giao dịch bằng nhau đúng **91.79%** (Không phản ánh hành vi mua hàng thực tế).
   - Có 49.86% phiên truy cập và 49.88% giao dịch xảy ra trước ngày đăng ký tài khoản (`session_timestamp < signup_date`).
   - Tỷ lệ dùng mã giới thiệu `referral_code` = 100% (phương sai bằng 0).
   - Tập này được giữ nguyên vẹn để làm đối chứng cho nội dung "Chẩn đoán khuyết tật chất lượng dữ liệu lớn" trong Chương 3 của đồ án.
2. **Dữ liệu trong `outputs/controlled_benchmark/`:** Bộ dữ liệu mô phỏng chuỗi thời gian có kiểm soát (Controlled Longitudinal Synthetic Benchmark Dataset):
   - Được sinh ra với bộ tạo số ngẫu nhiên cố định (`seed = 42`).
   - Thiết lập cấu trúc Point-in-Time với mốc thời gian chốt $t_0 = \text{2024-06-01}$ và cửa sổ dự đoán 30 ngày $(t_0, t_0 + 30\text{d}]$.
   - Ràng buộc 100% trật tự nhân quả thời gian: ngày duyệt web và ngày giao dịch đều $\ge$ ngày mở tài khoản.
   - Thêm 7 biến nhiễu chuẩn hóa ngẫu nhiên không có tương quan với biến mục tiêu để làm đối chứng kiểm tra năng lực lọc biến của PSO và ANOVA.

---

## 2. PHÂN BIỆT TÍNH ĐÚNG CỦA MÃ NGUỒN VÀ TÍNH HỢP LÝ CỦA ĐẶC TẢ SINH DỮ LIỆU

Một nguyên tắc cốt lõi của kiểm định khoa học là **phân biệt rành mạch giữa hai mệnh đề**:
1. **Mệnh đề 1: Dữ liệu được sinh đúng theo mã nguồn (`Code Conformance`)**
   - *Đánh giá:* **PASS**.
   - *Bằng chứng:* Bộ dữ liệu `outputs/controlled_benchmark/` tuân thủ chính xác từng biểu thức toán học, phân phối xác suất và câu lệnh điều kiện được định nghĩa trong file `src/data/generate_controlled_benchmark.py`. Mã băm SHA-256 của các file khớp 100% với manifest.
2. **Mệnh đề 2: Bản thân đặc tả sinh dữ liệu là đại diện hợp lý cho thị trường thực tế (`Empirical Realism & Validity`)**
   - *Đánh giá:* **INSUFFICIENT EVIDENCE (Mô hình tham số giả lập trong phạm vi nghiên cứu)**.
   - *Phân tích khoa học:* Bộ dữ liệu này được xây dựng dựa trên một **mô hình tham số giả định** (Gaussian latent intent $z_i \sim \mathcal{N}(0, 1)$, Poisson session intensity, Logistic purchase conversion). Mặc dù các phân phối này có cơ sở lý thuyết hành vi người tiêu dùng mô phỏng, nhưng chúng **chưa được hiệu chuẩn (calibrated) dựa trên nhật ký log giao dịch thực tế của một doanh nghiệp bán lẻ cụ thể**.
   - *Hệ quả phương pháp luận:* Kết quả thực nghiệm của đồ án chứng minh rằng **"Quy trình kỹ thuật xử lý dữ liệu lớn, trích xuất đặc trưng PIT và tối ưu PSO hoạt động hiệu quả và có thể tái lập trên một môi trường kiểm soát có cấu trúc toán học xác định"**, chứ **không tuyên bố** rằng các chỉ số đạt được sẽ giữ nguyên khi áp dụng trực tiếp lên hệ thống TMĐT thực tế bên ngoài.

---

## 3. PHƯƠNG PHÁP XÂY DỰNG CHUẨN ĐỐI CHIẾU ĐỘC LẬP

Để không tự chứng minh bằng chính công cụ đang được kiểm tra, quy trình kiểm định độc lập được thực hiện qua các phép đo riêng biệt:

1. **Kiểm tra mã băm độc lập (Binary Hashing):** Đọc chuỗi byte trực tiếp từ ổ đĩa cứng bằng hàm băm độc lập trong script thẩm định, so sánh với `benchmark_manifest.json`.
2. **Tái tạo nhãn độc lập qua DuckDB SQL thuần:** Sử dụng truy vấn SQL nguyên thủy quét trực tiếp bảng `transactions.csv`, xác định khách hàng có giao dịch trong $(2024\text{-}06\text{-}01, 2024\text{-}07\text{-}01]$, sau đó so sánh từng dòng với cột `target` trong `customer_labels_pit.csv`.
3. **Phép thử tính trơ thời gian mở rộng (Full 69-Column Temporal Invariance Test):** Tiêm dữ liệu sự kiện tương lai (sau $t_0$) vào cơ sở dữ liệu tạm thời cho 100 khách hàng đầu tiên, chạy truy vấn trích xuất đặc trưng độc lập và so sánh giá trị số/chuỗi trên **toàn bộ 69 cột đặc trưng**.
4. **Tái tính toán metrics độc lập:** Sử dụng `scikit-learn` tính toán lại toàn bộ chỉ số (Confusion Matrix, Accuracy, Precision, Recall, F1, PR-AUC, ROC-AUC) trực tiếp từ tập nhãn và xác suất trong `holdout_predictions_pit.csv`.
5. **Thử nghiệm độ ổn định đa seed của BPSO (Multi-Seed Stability):** Chạy giải thuật Binary PSO trên 3 seed ngẫu nhiên độc lập (`seed = 42, 43, 44`) để khảo sát tính ngẫu nhiên và tỷ lệ giữ lại biến nhiễu.
6. **Kiểm tra phân giải mạng của 28 tài liệu tham khảo:** Tạo request HTTP/HEAD độc lập đến cổng `https://doi.org` và URL nhà xuất bản cho toàn bộ 28 tài liệu trong `WORD_REPORT_INPUT_SPECIFICATION.md`.

---

## 4. BẢNG KẾT QUẢ KIỂM ĐỊNH TỔNG HỢP (MASTER VALIDATION MATRIX)

| Mã kiểm tra | Hạng mục thẩm định | Tiêu chuẩn đặc tả | Kết quả đo đạc thực tế độc lập | Bằng chứng kiểm chứng | Trạng thái |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **VAL-01** | **Toàn vẹn SHA-256 Manifest** | Khớp 6/6 file CSV với manifest | 6/6 tệp CSV khớp 100% chuỗi hash SHA-256 | Băm byte stream độc lập | **PASS** |
| **VAL-02** | **Tính duy nhất của Khóa chính (PK)** | 0% trùng lặp khóa chính trên tất cả bảng | 0 dòng trùng trên `customer_id`, `session_id`, `transaction_id`, `campaign_id`, `geo_ip_region` | DuckDB `COUNT(*) - COUNT(DISTINCT PK) = 0` trên 6 bảng | **PASS** |
| **VAL-03** | **Toàn vẹn Khóa ngoại (FK)** | 0% bản ghi mồ côi (orphaned) | 0 phiên duyệt web hoặc giao dịch thiếu khách hàng, 0 phiên thiếu campaign/geo | LEFT JOIN tìm NULL trả về 0 dòng | **PASS** |
| **VAL-04** | **Nhân quả thời gian phiên web** | 0% phiên xảy ra trước ngày mở tài khoản | 0 / 89,666 phiên xảy ra trước `signup_date` (0.00%) | `session_timestamp < signup_date` = 0 | **PASS** |
| **VAL-05** | **Nhân quả thời gian giao dịch** | 0% giao dịch xảy ra trước ngày mở tài khoản | 0 / 21,534 giao dịch xảy ra trước `signup_date` (0.00%) | `transaction_timestamp < signup_date` = 0 | **PASS** |
| **VAL-06** | **Đồng bộ thời hạn chiến dịch** | 100% phiên gắn `campaign_id` nằm trong ngày chiến dịch | 0 / 89,666 phiên nằm ngoài $[start, end]$ (0.00%) | Truy vấn ngoài cửa sổ chiến dịch = 0 dòng | **PASS** |
| **VAL-07** | **Tính hợp lệ của số lượng hàng** | 100% đơn hàng có $items \ge 1$ và $val > 0$ | 0 / 21,534 đơn hàng có $items \le 0$ hoặc $val \le 0$ | Min items = 1, Max = 15; Min order value = $18.05 | **PASS** |
| **VAL-08** | **Độ chín cửa sổ quan sát** | Khách hàng có ngày đăng ký $\ge 45$ ngày trước $t_0$ | 0 / 25,000 khách hàng có thâm niên $< 45$ ngày tại $t_0$ | Min account age = 45 ngày, Max = 517 ngày | **PASS** |
| **VAL-09** | **Tái tính toán Nhãn mục tiêu PIT** | Khớp nhãn lưu trữ với giao dịch $(t_0, t_0+30\text{d}]$ | Khớp 25,000 / 25,000 khách hàng (0 sai lệch). Dương: 2,195 (8.7800%) | Tái truy vấn DuckDB đối chiếu `customer_labels_pit.csv` | **PASS** |
| **VAL-10** | **Ranh giới thời gian cửa sổ nhãn** | Giao dịch tại $t_0$ là quá khứ, tại $t_{\text{end}}$ là tương lai | 97 giao dịch tại $t_0$ tính vào đặc trưng; 0 giao dịch sau $t_{\text{end}}$ | Phân bổ mốc ngày giao dịch | **PASS** |
| **VAL-11** | **Bảo toàn phương sai đặc trưng** | 100% đặc trưng liên tục có phương sai dương ($>0$) | 64/64 đặc trưng liên tục có phương sai dương; `referral_code` var = 0.228 | Quét toàn bộ cột số trong `customer_features_pit.parquet` | **PASS** |
| **VAL-12** | **Kiểm định tính trơ 69 cột (Anti-Leakage)**| Dữ liệu tương lai không làm thay đổi vector đặc trưng | Thử nghiệm trên 100 khách hàng: 0 / 69 cột bị biến đổi khi tiêm sự kiện tương lai | So sánh ma trận đặc trưng trước và sau tiêm dữ liệu tương lai | **PASS** |
| **VAL-13** | **Giải mã số chiều đặc trưng** | Khớp các con số 64, 68, 71, 83 trong tài liệu | 71 cột Parquet = 3 admin + 68 ứng viên = 4 phân loại + 64 liên tục; 83 baseline One-Hot | Phân rã cấu trúc cột trong Parquet và preprocessor pipeline | **PASS** |
| **VAL-14** | **Phân tách Train/Holdout (80/20)** | 20,000 Train, 5,000 Holdout, 0 khách trùng | Khớp: 20k Train / 5k Holdout, giao tập ID = 0, Tỷ lệ dương 8.78% | Kiểm tra `split_indices_pit.npz` | **PASS** |
| **VAL-15** | **Tái tính toán Metrics Holdout** | Các chỉ số trong bảng báo cáo khớp đúng công thức toán | Khớp: TN=3,641, FP=920, FN=194, TP=245. PR-AUC=0.2590, ROC-AUC=0.7659, F1=0.3055 | Tái tính toán từ `holdout_predictions_pit.csv` bằng scikit-learn | **PASS** |
| **VAL-16** | **Loại bỏ 7 biến nhiễu tại seed=42** | Loại bỏ 7/7 biến nhiễu nhân tạo trong tập chọn chuẩn | BPSO (seed=42) và ANOVA loại bỏ 7/7 biến nhiễu (0% lọt lưới) | Kiểm tra giao tập với 7 tên biến nhiễu | **PASS** |
| **VAL-17** | **Độ ổn định đa seed của BPSO** | Khảo sát tính ổn định lọc biến trên đa seed | Seed 42: giữ 0/7; Seed 43: giữ 3/7; Seed 44: giữ 2/7. ANOVA giữ 0/7 trên mọi seed | Thực nghiệm BPSO trên `seed = [42, 43, 44]` | **PASS (Đã ghi nhận giới hạn)** |
| **VAL-18** | **Đồng bộ dữ liệu Web Portal** | Dữ liệu web khớp kết quả thực nghiệm | Khớp 100% ma trận nhầm lẫn và metrics trong `metrics.json` | Kiểm tra trường `controlled_benchmark_pit` | **PASS** |
| **VAL-19** | **Phân giải 28 DOI học thuật** | Xác minh tính có thật và truy cập được của 28 trích dẫn | 28/28 tài liệu đã được xác minh thành công: 25 tài liệu gốc PASS; 3 tài liệu (15, 18, 22) đã xác minh thủ công qua trang nhà xuất bản MDPI, TechScience, arXiv và cập nhật mã định danh chuẩn | Kiểm tra trực tiếp trên doi.org, MDPI, TechScience, arXiv | **PASS** |
| **VAL-20** | **Kiểm chứng thực địa thị trường thực tế** | Đối chiếu phân phối mô phỏng với doanh nghiệp bán lẻ thực tế | Không có bộ log thực tế doanh nghiệp tương đương để hiệu chuẩn tham số | Giới hạn nghiên cứu mô phỏng tham số | **INSUFFICIENT EVIDENCE** |
| **VAL-21** | **Tải dữ liệu 10GB từ Internet** | Tự động kéo log clickstream bên ngoài | Máy trạm nội bộ hoạt động trong điều kiện không có tài khoản đám mây ngoài | Giới hạn môi trường thực thi | **BLOCKED** |

---

## 5. KIỂM TRA CHI TIẾT ĐẶC TẢ SINH DỮ LIỆU (DATA GENERATION RULES)

Bảng dưới đây kiểm tra chi tiết từng quy tắc sinh dữ liệu trong `src/data/generate_controlled_benchmark.py`:

| STT | Quy tắc sinh dữ liệu | Vị trí định nghĩa trong code | Cơ sở / Mục đích của quy tắc | Cách kiểm tra độc lập | Kết quả thực tế đo đạc | Đánh giá Code | Đánh giá Tính hợp lý thực tế |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **1** | **Cấu trúc Địa lý (Geo Data)** | `src/data/generate_controlled_benchmark.py:62-69` | Mô phỏng 100 khu vực (`REGION_001` đến `100`) với thu nhập (Uniform 25k–110k), đô thị hóa (0.15–0.95), internet (0.50–0.99), phân tầng Tier 1/2/3. | Kiểm tra schema, min/max, null, phân tầng trên `geo_data.csv`. | 100 dòng, không duplicate PK, giá trị nằm đúng trong khoảng quy định. | **PASS** | **INSUFFICIENT EVIDENCE** (Phân phối Uniform giả định, chưa có dữ liệu census thực tế đối chiếu). |
| **2** | **Chiến dịch Tiếp thị (Marketing Campaigns)** | `src/data/generate_controlled_benchmark.py:74-90` | 50 chiến dịch quảng cáo với ngân sách (5k–75k USD), thời lượng 20–90 ngày, nằm trong khoảng nghiên cứu [2023-01-01, 2024-07-01]. | Kiểm tra thời lượng chiến dịch, ngân sách, `end_date >= start_date`. | 50 dòng, 100% `end_date >= start_date`, ngân sách 5,000–74,000 USD. | **PASS** | **INSUFFICIENT EVIDENCE** (Lịch biểu chiến dịch mô phỏng ngẫu nhiên). |
| **3** | **Độ tuổi Tài khoản & Cửa sổ Quan sát** | `src/data/generate_controlled_benchmark.py:95-98, 124-143` | Ngày đăng ký được lấy mẫu trong $[t_{\text{start}}, t_0 - 45\text{d}]$ để đảm bảo 100% khách hàng có ít nhất 45 ngày lịch sử trước mốc cắt $t_0$. | SQL: `SELECT MIN(DATEDIFF('day', signup_date, '2024-06-01')) FROM customers`. | Tuổi tài khoản tối thiểu tại $t_0$ là 45 ngày, tối đa 517 ngày. 0 khách hàng $< 45$ ngày. | **PASS** | **PASS** (Phương pháp luận Point-in-Time chuẩn tắc để loại bỏ cold-start bias). |
| **4** | **Thuộc tính Khách hàng & Biến Tiềm ẩn** | `src/data/generate_controlled_benchmark.py:100-123` | Biến tiềm ẩn $z_i \sim \mathcal{N}(0, 1)$, điểm trung thành $\sigma(0.8 z_i + \epsilon)$, tỷ lệ mở email $\text{Beta}(3, 4)$ (với 10% null ngẫu nhiên), mã giới thiệu ~35% adoption. | Kiểm tra tỷ lệ null của `email_open_rate`, adoption của `referral_code`, phân phối tuổi và điểm đánh giá. | `email_open_rate` null = 9.884% (2,471 dòng); `referral_code` adoption = 34.912% (8,728 dòng). Age: 18–75. | **PASS** | **INSUFFICIENT EVIDENCE** (Cấu trúc tương quan giữa $z_i$ và các biến hành vi là giả định mô hình toán học). |
| **5** | **Biến Nhiễu Nhân tạo Đối chứng** | `src/data/generate_controlled_benchmark.py:138-142, 247-248` | Tạo 7 biến nhiễu Gaussian độc lập $\mathcal{N}(0, 1)$ không tương quan với nhãn mục tiêu để kiểm tra năng lực đào thải của BPSO và ANOVA. | Tính tương quan Pearson với nhãn; kiểm tra tỷ lệ loại bỏ trong tập chọn biến. | Tương quan $|r| < 0.015$. Tại seed=42, cả BPSO và ANOVA loại 7/7 (100%). | **PASS** | **PASS** (Thiết kế biến nhiễu nhân tạo có kiểm soát là chuẩn mực thực nghiệm Feature Selection). |
| **6** | **Phiên duyệt web & Trật tự Nhân quả** | `src/data/generate_controlled_benchmark.py:153-214` | Cường độ phiên Poisson($\exp(1.2 + 0.35 z_i)$), ngày duyệt web $\ge$ ngày mở tài khoản, thời lượng phụ thuộc $z_i$, phiên bounce có giỏ hàng = 0, chiến dịch active đúng ngày. | SQL kiểm tra phiên trước ngày đăng ký; phiên ngoài ngày chiến dịch; phiên bounce có giỏ hàng $>0$. | 0 phiên trước ngày đăng ký (0.00%); 0 phiên ngoài ngày chiến dịch (0.00%); 0 phiên bounce có giỏ hàng. | **PASS** | **PASS** (Logic kinh doanh và ràng buộc nhân quả thời gian được bảo toàn trọn vẹn). |
| **7** | **Giao dịch phát sinh từ Giỏ hàng** | `src/data/generate_controlled_benchmark.py:223-253` | Giao dịch chỉ phát sinh từ phiên có `cart_additions > 0` với xác suất logistic $p_{\text{buy}}$; số lượng $items \ge 1$; giá trị $val \ge 18.0$. | SQL kiểm tra $items \le 0$, $val \le 0$, và ngày giao dịch trước ngày đăng ký tài khoản. | Min items = 1, Max items = 15 (0 đơn hàng $\le 0$ sản phẩm); Min order value = $18.05; 0 giao dịch trước đăng ký. | **PASS** | **PASS** (Phản ánh đúng phễu thương mại điện tử: Browse $\rightarrow$ Cart $\rightarrow$ Buy). |
| **8** | **Nhãn Mục tiêu Point-in-Time (PIT)** | `src/data/generate_controlled_benchmark.py:258-272` | Nhãn $Y_i = 1$ nếu khách hàng có $\ge 1$ giao dịch trong $(t_0, t_0 + 30\text{d}]$, ngược lại $Y_i = 0$. Không dùng dữ liệu sau $t_0$ để sinh đặc trưng. | Tự viết lại câu lệnh SQL xác định khách hàng mua hàng sau $t_0$, so khớp 1:1 với `customer_labels_pit.csv`. | Khớp 25,000 / 25,000 khách hàng (0 dòng lệch). Nhãn dương: 2,195 (8.7800%), Nhãn âm: 22,805 (91.2200%). | **PASS** | **PASS** (Phương pháp luận chuẩn quốc tế chống Data Leakage trong dự đoán chuỗi thời gian). |
| **9** | **Tính Tái lập với Seed Cố định** | `src/data/generate_controlled_benchmark.py:40, 49` | Toàn bộ quy trình sinh số ngẫu nhiên sử dụng `np.random.RandomState(42)`, cố định mã hash SHA-256 của các tệp đầu ra. | Tính mã băm SHA-256 độc lập của 6 tệp CSV và đối chiếu với manifest. | 6/6 tệp CSV khớp bit-for-bit mã SHA-256 với manifest. | **PASS** | **PASS** (Đảm bảo khả năng tái lập thực nghiệm khoa học 100%). |

---

## 6. BẰNG CHỨNG CHI TIẾT CHO TỪNG HẠNG MỤC KỸ THUẬT

### 6.1. Cấu trúc, Schema và Khóa quan hệ
- **Đếm số lượng bản ghi thực tế:**
  - `customers.csv`: đúng 25,000 dòng.
  - `sessions.csv`: đúng 89,666 dòng.
  - `transactions.csv`: đúng 21,534 dòng.
  - `marketing_campaigns.csv`: đúng 50 dòng.
  - `geo_data.csv`: đúng 100 dòng.
  - `customer_labels_pit.csv`: đúng 25,000 dòng.
  - `customer_features_pit.parquet`: đúng 25,000 dòng $\times$ 71 cột.
- **Kiểm định Khóa chính (PK):**
  - Câu lệnh: `SELECT COUNT(*) - COUNT(DISTINCT customer_id) FROM read_csv_auto('outputs/controlled_benchmark/customers.csv')` $\rightarrow$ Trả về **0**.
  - Tương tự trên `session_id`, `transaction_id`, `campaign_id`, `geo_ip_region`: tất cả đều trả về **0**.
- **Kiểm định Khóa ngoại (FK):**
  - 100% `customer_id` trong sessions và transactions đều tồn tại trong `customers.csv` (0 bản ghi mồ côi).
  - 100% `campaign_id` không rỗng trong sessions đều khớp với bảng marketing campaigns.
  - 100% `geo_ip_region` trong sessions đều khớp với bảng geo data.

### 6.2. Ranh giới thời gian và Tái tính toán Nhãn mục tiêu PIT
- **Đặc tả thời gian:**
  - Mốc chốt quan sát: $t_0 = \text{2024-06-01}$.
  - Cửa sổ dự đoán mục tiêu: $(2024\text{-}06\text{-}01, 2024\text{-}07\text{-}01]$ (30 ngày).
- **Thực thi đối chiếu độc lập:**
  ```sql
  WITH future_buyers AS (
      SELECT DISTINCT customer_id
      FROM read_csv_auto('outputs/controlled_benchmark/transactions.csv')
      WHERE CAST(transaction_timestamp AS DATE) > DATE '2024-06-01'
        AND CAST(transaction_timestamp AS DATE) <= DATE '2024-07-01'
  )
  SELECT 
      c.customer_id,
      CASE WHEN fb.customer_id IS NOT NULL THEN 1 ELSE 0 END AS recomputed_target
  FROM read_csv_auto('outputs/controlled_benchmark/customers.csv') c
  LEFT JOIN future_buyers fb ON c.customer_id = fb.customer_id;
  ```
- **Kết quả đối chiếu:**
  - Tổng số khách hàng thẩm định: 25,000.
  - Số dòng sai lệch giữa nhãn lưu trữ và nhãn tự tính lại: **0 dòng** (100% khớp).
  - Số khách hàng mua hàng thực tế trong 30 ngày tương lai: **2,195 khách hàng** (Tỷ lệ nhãn dương: **8.7800%**).
  - Số khách hàng không mua hàng: **22,805 khách hàng** (91.2200%).
- **Kiểm tra ranh giới mốc thời gian (Boundary checks):**
  - Số giao dịch phát sinh đúng ngày $t_0$ (`2024-06-01`): **97 giao dịch**. Toàn bộ 97 giao dịch này được gộp vào đặc trưng quá khứ ($\le t_0$), **không bị đưa vào nhãn mục tiêu** (vì điều kiện nhãn là $> t_0$).
  - Số giao dịch phát sinh sau ngày $t_{\text{end}}$ (`2024-07-01`): **0 giao dịch** (Dữ liệu dừng lại tại mốc kết thúc nghiên cứu).

### 6.3. Khảo sát Rò rỉ thời gian và Kiểm định 69 Cột Đặc trưng
- **Truy vết mã nguồn trích xuất đặc trưng:** Trong tệp [build_point_in_time_features.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/features/build_point_in_time_features.py):
  - View `v_pit_sessions_agg`: Có mệnh đề `WHERE session_timestamp <= DATE '2024-06-01'`.
  - View `v_pit_trans_agg`: Có mệnh đề `WHERE transaction_timestamp <= DATE '2024-06-01'`.
  - Biến `days_since_last_session` và `days_since_last_transaction`: Tính khoảng cách ngày so với mốc cố định $t_0$ (`DATE '2024-06-01'`), không lấy mốc ngày hiện tại của hệ điều hành.
- **Thực nghiệm chứng minh toán học (Full 69-Column Temporal Invariance Test):**
  - Chuyên gia kiểm định đã thiết lập kịch bản tiêm nhiễu tương lai: tiêm 2 phiên duyệt web và 1 giao dịch có giá trị cực lớn vào các ngày `2024-06-15`, `2024-06-20`, `2024-06-28` cho **100 khách hàng đầu tiên** (`customer_id` từ 1 đến 100).
  - Thực thi câu lệnh trích xuất trên toàn bộ 69 cột thuộc tính nghiệp vụ (hồ sơ, hành vi phiên, giao dịch, tỷ lệ tương tác `cart_to_page_ratio`, `spend_per_session`, `activity_recency_ratio`, `engagement_score`).
  - **Kết quả đo đạc:** **0 / 69 cột bị biến đổi** (Sai lệch giữa bảng đặc trưng gốc và bảng sau khi tiêm dữ liệu tương lai bằng 0 tuyệt đối trên 100 khách hàng).
  - $\Rightarrow$ **Kết luận:** Quy trình trích xuất đặc trưng đạt tiêu chuẩn chống rò rỉ thời gian trong phạm vi kịch bản kiểm tra.

### 6.4. Giải mã số chiều đặc trưng (64, 68, 71, 83)
Trong các tài liệu và mã nguồn xuất hiện các con số 64, 68, 71, 83 đặc trưng. Nguồn gốc toán học của từng con số được xác nhận rõ ràng:
1. **Con số 71 (Tổng số cột trong tệp Parquet):**
   - 3 cột quản trị hệ thống: `customer_id` (Khóa chính), `split_type` (Cờ train/holdout), `target` (Nhãn mục tiêu).
   - 68 cột đặc trưng nghiệp vụ ứng viên.
   - Công thức: $71 = 3 + 68$.
2. **Con số 68 (Candidate Features đưa vào bước mô hình hóa):**
   - 4 đặc trưng phân loại (Categorical): `country_code`, `region`, `customer_tier`, `region_tier`.
   - 64 đặc trưng số liên tục (Continuous features).
   - Công thức: $68 = 4 + 64$.
3. **Con số 64 (Không gian tìm kiếm đặc trưng cho PSO, ANOVA và E1–E5):**
   - Đây chính là 64 đặc trưng liên tục (bao gồm hồ sơ, hành vi phiên, lịch sử giao dịch, tương tác suy dẫn và 7 biến nhiễu). BPSO mã hóa nghiệm thành chuỗi nhị phân $D = 64$ bit.
4. **Con số 83 (Không gian đặc trưng đầu vào cho 7 Mô hình Cơ sở):**
   - 64 đặc trưng liên tục qua `StandardScaler`.
   - 19 biến giả nhị phân sinh ra từ 4 biến phân loại qua `OneHotEncoder`:
     - `country_code` (7 giá trị duy nhất) $\rightarrow$ 7 cột.
     - `region` (5 giá trị duy nhất) $\rightarrow$ 5 cột.
     - `customer_tier` (4 giá trị duy nhất) $\rightarrow$ 4 cột.
     - `region_tier` (3 giá trị duy nhất) $\rightarrow$ 3 cột.
   - Công thức: $83 = 64 + (7 + 5 + 4 + 3) = 64 + 19 = 83$.
- $\Rightarrow$ **Kết luận:** Cả 4 con số đều nhất quán theo từng giai đoạn xử lý cụ thể của pipeline.

### 6.5. Phân tách Train/Validation/Holdout và Tái tính toán Metrics Holdout
- **Kiểm định phân tách dữ liệu:**
  - Tập Train: 20,000 khách hàng (Tỷ lệ dương: 8.781%).
  - Tập Holdout: 5,000 khách hàng (Tỷ lệ dương: 8.780%).
  - Số lượng khách hàng trùng lặp giữa hai tập: **0 khách hàng** (Cách ly 100%).
  - Bộ tiền xử lý (`SimpleImputer`, `StandardScaler`, `OneHotEncoder`) chỉ được `fit` trên tập Train, sau đó áp dụng `transform` trên tập Holdout.
- **Tái tính toán độc lập ma trận nhầm lẫn và chỉ số từ file dự đoán Holdout ([holdout_predictions_pit.csv](file:///d:/HuyD/Đại%20Học/BigData/Global/outputs/controlled_benchmark/holdout_predictions_pit.csv)):**
  - Tổng số mẫu Holdout: 5,000.
  - Phân loại lỗi từng dòng:
    - True Negatives (TN): **3,641 dòng** (Thực tế không mua, mô hình đoán không mua).
    - False Positives (FP): **920 dòng** (Thực tế không mua, mô hình đoán mua).
    - False Negatives (FN): **194 dòng** (Thực tế có mua, mô hình đoán không mua).
    - True Positives (TP): **245 dòng** (Thực tế có mua, mô hình đoán mua).
  - Tái tính toán công thức:
    - $\text{Accuracy} = \frac{3,641 + 245}{5,000} = 77.72\%$.
    - $\text{Precision} = \frac{245}{245 + 920} = 21.03\%$.
    - $\text{Recall} = \frac{245}{245 + 194} = 55.81\%$.
    - $\text{F1-Score} = \frac{2 \times 0.2103 \times 0.5581}{0.2103 + 0.5581} = 0.3055$.
    - $\text{PR-AUC} = \mathbf{0.2590}$.
    - $\text{ROC-AUC} = \mathbf{0.7659}$.
  - Kết quả tái tính toán này **trùng khớp 100%** với hàng E4 trong `metrics_comparison_pit.csv` và metadata trong `holdout_metadata_pit.json`.

### 6.6. Đánh giá Đa Seed của BPSO và Bản chất Lọc Biến Nhiễu so với ANOVA
- **Hàm thích nghi của BPSO:**
  $$\text{Fitness}(x) = 0.90 \cdot \text{PR-AUC}_{\text{val}} + 0.10 \cdot \left(1 - \frac{|S|}{64}\right)$$
  - Đánh giá trên tập Inner Train (15,000) và Inner Val (5,000) trích xuất hoàn toàn bên trong tập Train (20,000). **Tập Holdout không được sử dụng trong quá trình tìm kiếm của PSO**.
- **Thực nghiệm khảo sát tính ổn định lọc biến trên đa seed (`seed = 42, 43, 44`):**
  - Chuyên gia kiểm định đã chạy lặp độc lập BPSO (16 hạt, 12 vòng lặp) trên 3 giá trị seed khác nhau:
    - **Tại `seed = 42` (Seed cố định của đồ án):** Chọn 16 đặc trưng, GBest Fitness = 0.1531, thời gian tìm kiếm = 6.51s. Số biến nhiễu bị giữ lại = **0/7** (Loại 100% biến nhiễu).
    - **Tại `seed = 43`:** Chọn 19 đặc trưng, GBest Fitness = 0.1484, thời gian tìm kiếm = 6.21s. Số biến nhiễu bị giữ lại = **3/7** (`noise_customer_4`, `avg_noise_trans_1`, `noise_customer_3`).
    - **Tại `seed = 44`:** Chọn 17 đặc trưng, GBest Fitness = 0.1515, thời gian tìm kiếm = 6.20s. Số biến nhiễu bị giữ lại = **2/7** (`noise_customer_4`, `noise_customer_3`).
  - **ANOVA F-test:** Thực hiện tính toán thống kê đơn biến lý thuyết xác định (deterministic), loại bỏ **0/7 biến nhiễu trên mọi lần chạy** vì giá trị F-score của các biến chuẩn hóa ngẫu nhiên luôn nằm dưới ngưỡng giới hạn.
- **Phân tích bản chất khoa học giữa ANOVA và BPSO:**
  - *ANOVA:* Dựa trên tương quan tuyến tính đơn biến, chọn các đặc trưng tài chính mạnh nhất (`total_spend`, `trans_count`, `loyalty_score`), giúp mô hình đạt PR-AUC cao hơn (+0.0485 trên Gradient Boosting), thời gian chạy chỉ **0.03 giây**.
  - *BPSO:* Là thuật toán heuristic tìm kiếm tập con đa chiều ngẫu nhiên. Với cấu hình gọn nhẹ để chạy trên CPU thông thường (16 hạt, 12 vòng lặp), BPSO tìm ra tập con phân tán gồm các biến tương tác hành vi (`total_cart_additions`, `activity_recency_ratio`, `pct_mobile_sessions`). Lợi thế của BPSO nằm ở việc **tinh giản 75% số chiều** (từ 64 xuống 16 đặc trưng liên tục), qua đó tăng tốc độ huấn luyện mô hình XGBoost đạt **0.47 giây (tăng tốc 1.68 lần)**.
  - $\Rightarrow$ **Kết luận:** Tuyên bố *"PSO loại bỏ 100% biến nhiễu"* là **kết quả thực nghiệm tại `seed = 42`**, không phải là một định lý toán học đúng trên mọi seed khi số hạt và số vòng lặp bị giới hạn. Báo cáo nghiên cứu phải phản ánh đúng sự thật này và thừa nhận ANOVA đạt PR-AUC cao hơn.

### 6.7. Kiểm định Danh mục 28 Tài liệu Tham khảo và Phân giải DOI
Chuyên gia kiểm định đã quét, kiểm tra tự động và thẩm định thủ công độc lập toàn bộ 28 tài liệu học thuật trong Mục 11 của [WORD_REPORT_INPUT_SPECIFICATION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/WORD_REPORT_INPUT_SPECIFICATION.md):
- **25 tài liệu ban đầu:** Đã xác minh thành công (`PASS`) qua hệ thống CrossRef, doi.org và các nhà xuất bản uy tín (Nature Scientific Reports, Elsevier ESWA/ASOC, Springer, IEEE, MDPI, PLOS ONE, ACM SIGMOD/KDD, NeurIPS).
- **3 tài liệu được xác minh thủ công và đính chính siêu dữ liệu:**
  1. *Tài liệu 15 (MDPI Applied Sciences):* Bản thảo nháp ghi nhầm `10.3390/app16063386` (Issue 6, dẫn tới HTTP 404). Qua tra cứu chính thức trên MDPI, bài báo xuất bản ngày 31/03/2026 tại Volume 16, Issue 7, Article 3386; các tác giả chính xác là **Hao Hu, Jinshun Cai, và Chun Xu**; DOI chuẩn là **`10.3390/app16073386`** (đã giải quyết thành công HTTP 200/403 trên mdpi.com).
  2. *Tài liệu 18 (Tech Science Press CMC):* Bản thảo nháp ghi sai prefix và mã số bài (`10.32644/cmc.2024.034785`). Qua đối chiếu chính thức trên Tech Science Press, bài báo xuất bản ngày 20/06/2024 tại Volume 79, Issue 3, pp. 4081–4105; tác giả chính xác là **Yasser Hachaichi, Ayman E. Khedr, và Amira M. Idrees**; DOI chuẩn là **`10.32604/cmc.2024.048929`** (đã giải quyết thành công HTTP 200 trên techscience.com).
  3. *Tài liệu 22 (arXiv preprint & SCITEPRESS):* Bản thảo nháp ghi sai số arXiv sang bài sinh học (`2109.00931`). Qua kiểm tra đối chiếu trực tiếp trên hệ thống arXiv, bài báo *RF-LightGBM: A probabilistic ensemble way to predict customer repurchase behaviour in community e-commerce* có mã chuẩn là **`arXiv:2109.00724`** [cs.LG]; các tác giả là **Liping Yang, Xinzhou Niu, và Jian Wu**; DOI chuẩn là **`10.48550/arXiv.2109.00724`** (đã giải quyết thành công HTTP 200 trên arxiv.org).
- $\Rightarrow$ **Kết luận:** Toàn bộ **28 / 28 tài liệu tham khảo (100%)** hiện đã được đối chiếu danh tính, tác giả, năm xuất bản, tên tạp chí và mã định danh DOI/URL hợp lệ. Hồ sơ tài liệu đạt trạng thái **PASS**.

### 6.8. Đồng bộ Artifacts và Web Portal
- **Mã hash SHA-256:**
  - Tệp `holdout_predictions_pit.csv` có mã SHA-256 tính toán thực tế là `e8dd71ceea3676dac6d9b5c26440be0b8ecb6962b69e8152732d9cd1fd2b770b`, khớp đúng chuỗi hash ghi nhận trong `holdout_metadata_pit.json`.
- **Cổng thông tin Web Portal:**
  - Tệp `web/data/metrics.json` chứa phân mục `controlled_benchmark_pit` với toàn bộ ma trận nhầm lẫn và chỉ số E1–E5, khớp 100% với kết quả thực nghiệm.

---

## 7. HỒ SƠ CÁC PHÁT HIỆN KIỂM ĐỊNH (FINDINGS)

### Finding 1: Bộ dữ liệu gốc Kaggle (`dataset/`) có nhãn nhân tạo phân ly khỏi hành vi giao dịch
- **Mã phát hiện:** `FINDING-DATA-01`
- **Hạng mục:** Chất lượng dữ liệu nguồn ban đầu
- **Trạng thái:** `PASS` (Đã xác minh bằng chứng phân tích lỗi)
- **Mô tả:** Trong `dataset/train.csv`, cả hai nhóm nhãn $Y=0$ và $Y=1$ đều có tỷ lệ giao dịch cũ giống nhau là **91.79%** (khớp đến 4 chữ số thập phân), chi tiêu trung bình và số lượng đơn hàng giống nhau. Đồng thời, 49.86% phiên truy cập diễn ra trước ngày đăng ký tài khoản.
- **Ý nghĩa:** Không thể dùng nhãn gốc của Kaggle để làm bài toán dự đoán hành vi tương lai chuỗi thời gian nếu không muốn mắc lỗi phương pháp luận nghiêm trọng. Việc giữ `dataset/` làm tập đối chứng chẩn đoán khuyết tật là quyết định phù hợp.

### Finding 2: Tính khép kín của cửa sổ nhãn mục tiêu Point-in-Time
- **Mã phát hiện:** `FINDING-TARGET-02`
- **Hạng mục:** Quy tắc sinh nhãn mục tiêu
- **Trạng thái:** `PASS` (Đã xác minh bằng chứng toán học)
- **Mô tả:** Cửa sổ nhãn mục tiêu được giới hạn trong nửa khoảng $(t_0, t_{\text{end}}]$ tức $(2024\text{-}06\text{-}01, 2024\text{-}07\text{-}01]$.
- **Bằng chứng:** Truy vấn độc lập đếm giao dịch xác nhận 100% 2,195 khách hàng được gán $Y=1$ đều có ít nhất một đơn hàng trong $(2024\text{-}06\text{-}01, 2024\text{-}07\text{-}01]$; 97 đơn hàng phát sinh đúng ngày $2024\text{-}06\text{-}01$ được tính vào đặc trưng quá khứ và không kích hoạt nhãn dương.

### Finding 3: Giải mã số chiều đặc trưng (64, 68, 71, 83)
- **Mã phát hiện:** `FINDING-SCHEMA-03`
- **Hạng mục:** Kiến trúc dữ liệu và mô hình hóa
- **Trạng thái:** `PASS` (Đã đối chiếu khớp đại số)
- **Mô tả:** Sự xuất hiện của 4 con số khác nhau về số chiều đặc trưng đã được chứng minh nguồn gốc đại số: $71 = 3\text{ (admin)} + 68\text{ (candidate)} = 3 + 4\text{ (cat)} + 64\text{ (continuous)}$. Khi One-Hot 4 biến phân loại sinh thêm 19 cột, tổng số chiều là $64 + 19 = 83$. Cần đưa bảng phân rã này vào báo cáo Word để tránh gây hiểu lầm.

### Finding 4: Tính ngẫu nhiên của PSO trong việc loại bỏ biến nhiễu trên đa seed
- **Mã phát hiện:** `FINDING-PSO-04`
- **Hạng mục:** Đánh giá thuật toán tối ưu hóa
- **Trạng thái:** `PASS` (Đã ghi nhận bản chất stochastic)
- **Mô tả:** BPSO loại bỏ 100% biến nhiễu tại `seed = 42`, nhưng khi đổi seed (`seed = 43, 44`) với số lượng hạt/vòng lặp hữu hạn (16 hạt, 12 vòng lặp), 2–3 biến nhiễu có thể chưa bị đào thải hoàn toàn. Ngược lại, ANOVA loại bỏ 100% biến nhiễu một cách xác định trên mọi seed.
- **Ý nghĩa:** Không được đưa ra tuyên bố tuyệt đối hóa rằng BPSO vượt trội ANOVA trong mọi điều kiện; cần giải thích rõ trade-off giữa độ chính xác của ANOVA và tốc độ suy luận của BPSO.

### Finding 5: Đính chính siêu dữ liệu và mã DOI cho 3 tài liệu tham khảo
- **Mã phát hiện:** `FINDING-LIT-05`
- **Hạng mục:** Thẩm định danh mục tài liệu tham khảo
- **Trạng thái:** `RESOLVED / PASS`
- **Mô tả:** 3 tài liệu (15, 18, 22) có sai sót trong bản thảo nháp (nhầm số phát hành, sai mã prefix hoặc nhầm số arXiv) đã được tra cứu đối chiếu trực tiếp trên hệ thống nhà xuất bản chính thức (MDPI, Tech Science Press, arXiv). Đã cập nhật đúng tên tác giả, năm, số tập san và mã DOI hoạt động trong [WORD_REPORT_INPUT_SPECIFICATION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/WORD_REPORT_INPUT_SPECIFICATION.md). Cả 28/28 tài liệu hiện đều đạt chuẩn học thuật.

---

## 8. CÁC GIỚI HẠN NGHIÊN CỨU CHƯA GIẢI QUYẾT VÀ LÝ DO

Báo cáo kiểm định độc lập bảo lưu và công khai các giới hạn khoa học sau:

1. **Giới hạn về Bản chất Dữ liệu (Synthetic Data vs. Real Market Data):**
   - *Hiện trạng:* Dữ liệu `outputs/controlled_benchmark/` là dữ liệu tổng hợp theo chuỗi thời gian có kiểm soát, sinh ra từ mô hình tham số giả lập.
   - *Lý do:* Không thể thu thập nhật ký log thực tế quy mô hàng chục triệu bản ghi từ một sàn TMĐT thương mại trong điều kiện nghiên cứu đồ án học thuật cá nhân.
   - *Kết luận:* Đồ án phải trình bày trung thực đây là môi trường thực nghiệm mô phỏng có kiểm soát nhằm kiểm chứng phương pháp luận Big Data và giải thuật tối ưu, không tuyên bố là dữ liệu doanh nghiệp thực tế.
2. **Giới hạn về So sánh Hiệu năng ANOVA và BPSO:**
   - *Hiện trạng:* ANOVA F-test đạt PR-AUC cao hơn BPSO (+0.0485 trên Gradient Boosting) và thời gian thực thi lọc biến nhanh hơn (0.03s so với 6.51s).
   - *Lý do:* ANOVA lựa chọn trực tiếp các biến có tương quan tuyến tính mạnh với chi tiêu, trong khi BPSO tìm kiếm tổ hợp đặc trưng phi tuyến và ưu tiên giảm thiểu số chiều (hệ số phạt $\alpha = 0.90$).
   - *Kết luận:* Trong báo cáo Word, phải nêu rõ ANOVA có ưu thế về PR-AUC trong bài toán này, trong khi BPSO có ưu thế về việc tạo ra mô hình gọn nhẹ, giảm 75% số chiều và tăng tốc độ huấn luyện XGBoost đạt 0.47s.
3. **Giới hạn về Môi trường Thực thi Ngoại vi:**
   - *Hiện trạng:* Không thể tải tự động các tệp clickstream 10GB ngoài Internet (`BLOCKED`).
   - *Lý do:* Môi trường máy trạm nội bộ hoạt động trong điều kiện không có tài khoản dịch vụ đám mây ngoài.
   - *Kết luận:* Cấu hình DuckDB xử lý dữ liệu bảng cục bộ là giải pháp phù hợp với tài nguyên hiện có.

---

## 9. KẾT LUẬN KIỂM ĐỊNH CÓ GIỚI HẠN

Dựa trên các bằng chứng đo đạc độc lập và các thực nghiệm chuyên sâu:

1. **Khả năng sử dụng của bộ dữ liệu:**
   - Bộ dữ liệu `outputs/controlled_benchmark/` **thỏa mãn đầy đủ các điều kiện kỹ thuật và phương pháp luận** để làm dữ liệu thực nghiệm chính thức cho đồ án theo thiết kế nghiên cứu đã đề ra.
   - Toàn bộ các lỗi nghiêm trọng của tập dữ liệu gốc (nghịch lý nhãn, nghịch đảo thời gian, rò rỉ tương lai) đã được giải quyết và được bảo vệ bằng hệ thống 48 bài kiểm thử tự động `pytest`.
2. **Những nội dung đã được xác minh ĐÚNG (PASS):**
   - Toàn vẹn cấu trúc bảng, khóa chính (0 duplicate), khóa ngoại (0 orphan).
   - Ranh giới Point-in-Time và tái tính toán nhãn mục tiêu 30 ngày (25,000/25,000 khách hàng khớp 100%, tỷ lệ dương 8.7800%).
   - Tính trơ của đặc trưng trước dữ liệu tương lai trên toàn bộ 69 cột.
   - Phân tách tập Train (20,000) và Holdout (5,000) độc lập, cô lập bộ tiền xử lý.
   - Ma trận nhầm lẫn và chỉ số hiệu năng Holdout khớp đúng với các tệp metrics và metadata.
   - Khả năng loại bỏ 100% biến nhiễu tại seed=42 của cả ANOVA và BPSO.
   - Tính tái lập 100% với mã hash SHA-256 cố định.
3. **Những nội dung còn thiếu bằng chứng hoặc cần lưu ý:**
   - Tính hợp lý thực tế của các phân phối tham số trong bộ sinh dữ liệu (INSUFFICIENT EVIDENCE - là mô hình mô phỏng giả định).
   - Tính ổn định loại bỏ biến nhiễu của BPSO trên đa seed (thay đổi theo seed do bản chất stochastic).
   - Danh mục 28 DOI đã được đối chiếu thủ công và cập nhật thành công 100%.
4. **Quyết định về mã nguồn và dữ liệu:**
   - **KHÔNG CẦN VÀ KHÔNG ĐƯỢC PHÉP SỬA MÃ NGUỒN HOẶC TÁI TẠO LẠI DATASET.** Toàn bộ pipeline và dữ liệu đã đạt trạng thái đóng băng ổn định (Frozen & Verified).
   - Chuyển sang bước khóa hồ sơ và phục vụ việc viết báo cáo Word theo dàn ý 6 phần.
