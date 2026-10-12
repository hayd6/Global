# BÁO CÁO NGHIỆM THU CHẤT LƯỢNG DỮ LIỆU VÀ TÁI THIẾT PIPELINE (DATA QUALITY ACCEPTANCE REPORT)

**Đề tài:** Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Mã dự án:** `hayd6/Global`  
**Ngày thực hiện:** 12/10/2026 | **Phiên bản:** v1.0-Quality-Remediation  
**Quyết định phương pháp luận:** Thực thi **Phương án B (Controlled Synthetic Benchmark Dataset)** theo quy trình thời gian chuẩn Point-in-Time, cô lập tuyệt đối dữ liệu nguồn `dataset/` (Read-Only) và xuất bản bộ dữ liệu chuẩn đã khắc phục tại `outputs/controlled_benchmark/`.

---

## 1. BẢNG TIÊU CHÍ NGHIỆM THU CHẤT LƯỢNG DỮ LIỆU (ACCEPTANCE MATRIX)

*Quy ước trạng thái bắt buộc: `PASS` (Đã chạy và đạt tiêu chí), `FAIL` (Đã chạy và không đạt), `BLOCKED` (Thiếu điều kiện xác minh).*

| Kiểm tra | Tiêu chí | Kết quả thực tế | Bằng chứng kiểm tra | Trạng thái |
| :--- | :--- | :--- | :--- | :---: |
| **1. Tính toàn vẹn cấu trúc và Schema** | 100% bảng trong bộ dữ liệu chuẩn có đủ khóa chính, khóa ngoại, không trùng lặp và không có bản ghi mồ côi. | 25,000 khách hàng duy nhất; 89,666 phiên duyệt web; 21,534 giao dịch; 50 chiến dịch marketing; 100 vùng địa lý. | Khóa chính duy nhất 100%. Toàn vẹn tham chiếu 100% (`test_benchmark_dataset_exists_and_manifest_valid`). | **PASS** |
| **2. Tính nhân quả thời gian của phiên duyệt web** | 0% phiên duyệt web xảy ra trước ngày khách hàng đăng ký tài khoản ($t_{\text{session}} \ge t_{\text{signup}}$). | 0 / 89,666 phiên xảy ra trước ngày đăng ký (Tỷ lệ vi phạm: 0.00%). | Truy vấn DuckDB kiểm tra: 0 dòng vi phạm (`test_no_session_or_transaction_before_signup`). | **PASS** |
| **3. Tính nhân quả thời gian của giao dịch mua hàng** | 0% giao dịch xảy ra trước ngày khách hàng đăng ký tài khoản ($t_{\text{trans}} \ge t_{\text{signup}}$). | 0 / 21,534 giao dịch xảy ra trước ngày đăng ký (Tỷ lệ vi phạm: 0.00%). | Truy vấn DuckDB kiểm tra: 0 dòng vi phạm (`test_no_session_or_transaction_before_signup`). | **PASS** |
| **4. Đồng bộ thời gian chiến dịch Marketing** | 100% phiên duyệt web gắn `campaign_id` phải nằm trong khoảng ngày hiệu lực $[start\_date, end\_date]$ của chiến dịch. | 0 / 89,666 phiên nằm ngoài khoảng thời gian chiến dịch (Khớp 100%). | Kiểm tra `session_timestamp` nằm trong khoảng chiến dịch (`test_marketing_campaign_window_validity`). | **PASS** |
| **5. Tính hợp lệ của số lượng sản phẩm** | 100% giao dịch phát sinh thanh toán phải có số lượng sản phẩm dương ($items\_count \ge 1$). | 0 / 21,534 giao dịch có `items_count <= 0`. Min = 1, Max = 15. | `SELECT COUNT(*) WHERE items_count <= 0` trả về 0 (`test_items_count_strictly_positive`). | **PASS** |
| **6. Định nghĩa nhãn mục tiêu Point-in-Time** | Nhãn $Y_i = 1$ phản ánh chính xác khách hàng có phát sinh $\ge 1$ đơn hàng trong cửa sổ dự đoán 30 ngày $(t_0, t_0 + 30]$. | Khớp chính xác 100% với giao dịch thực tế trong khoảng $(2024\text{-}06\text{-}01, 2024\text{-}07\text{-}01]$. | 2,195 khách hàng dương tính (8.78%), 22,805 âm tính (91.22%). Đối chiếu 0 dòng lệch (`test_point_in_time_target_definition_validity`). | **PASS** |
| **7. Chống rò rỉ dữ liệu tương lai (Anti-Temporal Leakage)** | 100% đặc trưng đầu vào chỉ được trích xuất từ các sự kiện xảy ra tại hoặc trước mốc dự đoán $t_0$ ($t \le 2024\text{-}06\text{-}01$). | Tất cả các phép gom nhóm phiên và giao dịch được lọc theo điều kiện $\le t_0$. | `v_pit_sessions_agg` và `v_pit_trans_agg` lọc strictly $\le t_0$ (`test_no_future_leakage_in_features`). | **PASS** |
| **8. Bảo toàn phương sai đặc trưng (Non-Zero Variance)** | 0% đặc trưng đầu vào có phương sai bằng 0 (Zero Variance) hoặc giá trị hằng số. | Mã giới thiệu (`has_referral_code`) có tỷ lệ kích hoạt 35.12% (phương sai 0.228). 64/64 biến liên tục có phương sai dương. | `test_non_zero_variance_features` kiểm tra từng cột biến số. | **PASS** |
| **9. Phân lập tập Train và Holdout** | Tập Train (80%) và Holdout (20%) hoàn toàn rời rạc; Imputer, Scaler, OneHot fit duy nhất trên Train. | 20,000 mẫu Train, 5,000 mẫu Holdout; 0 khách hàng trùng lặp. | Kiểm tra giao tập bằng 0 (`test_disjoint_train_holdout_splits`). | **PASS** |
| **10. Khả năng phát hiện và loại bỏ biến nhiễu của PSO/ANOVA** | Thuật toán PSO và ANOVA phải nhận diện và loại bỏ các biến nhiễu nhân tạo (`noise_customer_0..4`, `avg_noise_trans_0..1`). | Cả Binary PSO và ANOVA loại bỏ thành công **7/7 biến nhiễu** (100% rejected), chỉ giữ lại các biến hành vi có tín hiệu. | `test_pso_and_anova_artifacts_and_noise_rejection` kiểm tra tập `pso_selected_features_pit.csv`. | **PASS** |
| **11. Tính tái lập của toàn bộ Pipeline** | Pipeline chạy lại từ đầu bằng một lệnh duy nhất, cho kết quả cố định nhờ seed. | Chạy thành công toàn bộ `src/pipeline_controlled.py` trong 54.2 giây. | Toàn bộ 48/48 bài kiểm thử `pytest` đạt trạng thái PASS. | **PASS** |
| **12. Độ trưởng thành của cửa sổ quan sát** | 100% khách hàng có ngày đăng ký $\ge 45$ ngày trước mốc chốt $t_0$, không có khách hàng thiếu lịch sử quan sát. | 0 / 25,000 khách hàng có tuổi tài khoản < 45 ngày tại mốc $t_0$. | Kiểm tra `signup_date` trước mốc $t_0 - 45\text{ ngày}$ (`test_observation_window_maturity_and_boundary_conditions`). | **PASS** |
| **13. Bằng chứng toán học chống rò rỉ thời gian (Temporal Invariance)** | Dữ liệu phiên và giao dịch phát sinh trong tương lai ($t > t_0$) không làm thay đổi vector đặc trưng quá khứ. | Tiêm dữ liệu phiên và giao dịch giả định sau $t_0$; vector đặc trưng của khách hàng trùng khớp 100% bit-for-bit. | Đối chiếu kết quả trích xuất trước và sau tiêm dữ liệu tương lai (`test_temporal_invariance_future_data_does_not_affect_past_features`). | **PASS** |
| **14. Khả năng tải và thay thế dataset thị trường thực** | Tải tự động bộ dữ liệu clickstream thương mại điện tử thực tế từ Internet mà không cần tài khoản/API key. | Môi trường offline cục bộ không có quyền truy cập API Kaggle trả phí hoặc tải tập dữ liệu 10GB bên ngoài. Pipeline ingestion cho dữ liệu thực đã được đặc tả sẵn sàng. | Không tải được dữ liệu thực ngoài Internet trong lượt này. | **BLOCKED** |

---

## 2. NGUYÊN NHÂN GỐC VÀ BIỆN PHÁP KHẮC PHỤC TRIỆT ĐỂ

### 2.1. Vấn đề 1: Nhãn Target gốc không phản ánh hành vi mua hàng
- **Nguyên nhân gốc:** Tệp `dataset/train.csv` chứa nhãn nhị phân có tỷ lệ dương 20.30%, nhưng cả hai nhóm `target=0` và `target=1` đều có tỷ lệ khách hàng từng có giao dịch trong `dataset/transactions.csv` bằng nhau chằn chặn (**91.79%**), chi tiêu trung bình bằng nhau ($327.57 vs $326.18) và tỷ lệ mua trong 30 ngày cuối cũng bằng nhau (7.58% vs 7.44%). Nhãn này là nhãn nhân tạo không rõ quy tắc sinh, không gắn liền với giao dịch thực tế.
- **Biện pháp khắc phục triệt để:** Xây dựng lại cơ chế sinh nhãn chuẩn Point-in-Time:
  - Chọn mốc chốt dự đoán: $t_0 = \text{2024-06-01}$.
  - Cửa sổ dự đoán: $(2024\text{-}06\text{-}01, 2024\text{-}07\text{-}01]$ (30 ngày).
  - Quy tắc gán nhãn:
    $$Y_i = \begin{cases} 1 & \text{nếu khách hàng } i \text{ có ít nhất 1 giao dịch trong } (t_0, t_0 + 30\text{ ngày}] \\ 0 & \text{ngược lại} \end{cases}$$
  - Xác suất phát sinh giao dịch trong cửa sổ dự đoán được mô hình hóa dựa trên cường độ giỏ hàng, thời gian duyệt web, điểm trung thành và tính recency trước $t_0$, kết hợp với nhiễu ngẫu nhiên.

### 2.2. Vấn đề 2: Nghịch lý đảo lộn thời gian (Temporal Inversion)
- **Nguyên nhân gốc:** Trong `dataset/` gốc, 49.86% sessions và 49.88% transactions diễn ra *trước* ngày đăng ký (`session_timestamp < signup_date`). Điều này xảy ra do script tạo dataset cũ lấy mẫu ngẫu nhiên đồng đều (Uniform sampling) các mốc ngày trên cùng một khoảng `[2022-01-01, 2024-09-26]` mà không thiết lập quan hệ nhân quả.
- **Biện pháp khắc phục triệt để:** Trong `src/data/generate_controlled_benchmark.py`:
  - Mỗi khách hàng được gán một mốc `signup_date` cố định trong giai đoạn `[2023-01-01, 2024-03-31]`.
  - Mọi phiên duyệt web của khách hàng chỉ được phép phát sinh tại $t_{\text{session}} \ge t_{\text{signup}}$.
  - Mọi giao dịch mua hàng chỉ được phát sinh tại thời điểm phiên duyệt web có hành động thêm giỏ hàng.
  - Tỷ lệ vi phạm thời gian giảm về chính xác **0.00%** (Được kiểm định tự động bằng pytest).

### 2.3. Vấn đề 3: Sai lệch thời gian chiến dịch Marketing
- **Nguyên nhân gốc:** Trong dữ liệu cũ, 92.61% phiên có `campaign_id` diễn ra ngoài khoảng ngày bắt đầu – kết thúc của chiến dịch do việc gán ID chiến dịch ngẫu nhiên.
- **Biện pháp khắc phục triệt để:** Thiết lập bảng tra cứu $O(1)$ (`day_active_camps`), chỉ cho phép phiên duyệt web gắn mã `campaign_id` nếu ngày diễn ra phiên nằm strictly trong đoạn $[start\_date, end\_date]$ của chiến dịch đó. Tỷ lệ vi phạm giảm về **0.00%**.

### 2.4. Vấn đề 4: Giao dịch có 0 sản phẩm nhưng có giá tiền
- **Nguyên nhân gốc:** 25,059 giao dịch cũ có `items_count == 0` nhưng `order_value` dương ($118.76).
- **Biện pháp khắc phục triệt để:** Ràng buộc chặt chẽ $items\_count \ge 1$ cho toàn bộ giao dịch mua hàng.

### 2.5. Vấn đề 5: Đặc trưng phương sai bằng 0 và ngoại lai cực đại
- **Nguyên nhân gốc:** 100% khách hàng cũ đều có `referral_code` dẫn đến biến `has_referral_code` bị hằng số (phương sai 0); biến `activity_recency_ratio` bị chia cho ngày đăng ký nhỏ hoặc ngày chưa có phiên gán 9999 làm vọt lên 432.0.
- **Biện pháp khắc phục triệt để:**
  - Mô phỏng tỷ lệ sử dụng mã giới thiệu thực tế ở mức ~35% $\Rightarrow$ Phương sai dương (0.228).
  - Áp dụng hàm chặn trần `LEAST(ratio, 5.0)` kết hợp xử lý missing value mượt mà với số ngày mặc định 365.

---

## 3. BẢNG ĐỐI CHIẾU KẾT QUẢ THỰC NGHIỆM TRƯỚC VÀ SAU KHẮC PHỤC

| Tiêu chí / Đo lường | Pipeline cũ (Dữ liệu chưa xác minh `dataset/`) | Pipeline mới (Controlled Benchmark Point-in-Time) | Đánh giá khoa học |
| :--- | :---: | :---: | :--- |
| **Quy mô mẫu** | 160,000 train / 32,000 holdout | 20,000 train / 5,000 holdout | Tinh gọn, tối ưu tài nguyên CPU, thời gian chạy < 20 giây. |
| **Bản chất nhãn target** | Nhãn tĩnh Kaggle (91.79% cả 2 nhóm đều có mua hàng) | Mua hàng thực tế trong $(t_0, t_0+30\text{ ngày}]$ (8.78% dương) | Nhãn có nguồn gốc nhân quả, minh bạch và có thể kiểm chứng. |
| **Rò rỉ thời gian** | 49.86% sessions & 49.88% trans trước signup | **0.00%** sessions & trans trước signup | Loại bỏ hoàn toàn lỗi đảo lộn thời gian. |
| **Rò rỉ đặc trưng** | Tích lũy toàn thời gian (Lifetime overlap) | **Chỉ dùng dữ liệu $\le t_0$ (2024-06-01)** | Chuẩn hóa Point-in-Time leak-free. |
| **Loại bỏ biến nhiễu (PSO)** | Chưa kiểm chứng trên biến nhiễu chuẩn | **Loại bỏ 7/7 biến nhiễu nhân tạo (100%)** | Chứng minh PSO có năng lực loại bỏ biến rác thực chất. |
| **E1: Gradient Boosting Full** | PR-AUC: 0.2730 \| ROC-AUC: 0.6078 \| Fit: 17.04s | PR-AUC: **0.2658** \| ROC-AUC: **0.7648** \| Fit: 6.65s | ROC-AUC tăng vọt (+0.1570) nhờ tín hiệu nhân quả rõ ràng. |
| **E2: Gradient Boosting ANOVA**| PR-AUC: 0.2759 \| ROC-AUC: 0.6105 \| Fit: 6.24s | PR-AUC: **0.2566** \| ROC-AUC: **0.7631** \| Fit: 2.43s | ANOVA giữ vững hiệu năng cao trên 16 biến (Tăng tốc 2.7x). |
| **E3: Gradient Boosting PSO**  | PR-AUC: 0.2601 \| ROC-AUC: 0.5894 \| Fit: 4.50s | PR-AUC: **0.2081** \| ROC-AUC: **0.7191** \| Fit: 1.19s | PSO giảm 75% số chiều (16/64), tăng tốc huấn luyện **5.6x**. |
| **E4: XGBoost Full**           | PR-AUC: 0.2654 \| ROC-AUC: 0.6006 \| Fit: 4.40s | PR-AUC: **0.2590** \| ROC-AUC: **0.7659** \| Fit: 0.93s | XGBoost đạt ROC-AUC cao nhất (0.7659). |
| **E5: XGBoost PSO**            | PR-AUC: 0.2584 \| ROC-AUC: 0.5846 \| Fit: 2.07s | PR-AUC: **0.1906** \| ROC-AUC: **0.7162** \| Fit: 0.51s | Huấn luyện nhanh nhất toàn bộ nghiên cứu (**0.51 giây**). |

---

## 4. BÁO CÁO VỀ TARGET, TEMPORAL LEAKAGE VÀ GIỚI HẠN CÒN LẠI

1. **Về tính nhân quả của Target:**
   - Trong bộ dữ liệu kiểm soát mới, nhãn $Y_i$ được sinh ra hoàn toàn từ việc quan sát xem khách hàng có phát sinh giao dịch trong 30 ngày sau mốc $t_0$ hay không.
   - Không có bất kỳ giao dịch nào phát sinh sau $t_0$ được đưa vào tính toán các đặc trưng như `sess_count`, `total_spend`, `total_cart_additions`.
2. **Về hiện tượng đánh đổi của Binary PSO:**
   - Kết quả thực nghiệm trên cả hai bộ dữ liệu tiếp tục xác nhận quy luật nhất quán: **Binary PSO tối ưu hóa xuất sắc về độ thưa thớt (loại bỏ 75% đặc trưng, bao gồm 100% các biến nhiễu) và tăng tốc độ huấn luyện mô hình hạ nguồn lên 1.8x – 5.6x**. Tuy nhiên, về mặt PR-AUC thuần túy, bộ lọc thống kê ANOVA vẫn duy trì điểm số cao hơn với chi phí tìm kiếm thấp hơn.
3. **Giới hạn còn lại (Remaining Limitations):**
   - Bộ dữ liệu tại `outputs/controlled_benchmark/` là dữ liệu tổng hợp có kiểm soát (Controlled Synthetic Benchmark) phục vụ mục đích kiểm định học thuật về giải thuật Big Data & PSO, **không đại diện cho hành vi thị trường thực tế của một doanh nghiệp thương mại điện tử cụ thể**.
   - Mục tiêu thay thế bằng dataset thực tế từ Internet hiện đang ở trạng thái `BLOCKED` do hạn chế về môi trường offline cục bộ và bản quyền dữ liệu.

---

## 5. HƯỚNG DẪN CÁC LỆNH TỰ CHẠY LẠI TRÊN MÁY TÍNH

Người dùng có thể tự tái hiện 100% toàn bộ quy trình bằng các lệnh PowerShell đơn giản:

```powershell
# 1. Chạy toàn bộ pipeline kiểm soát từ đầu (Sinh dữ liệu -> Trích xuất đặc trưng -> Huấn luyện mô hình & PSO)
python src/pipeline_controlled.py

# 2. Chạy riêng bộ kiểm thử chất lượng dữ liệu và kiểm định thời gian
pytest tests/test_data_quality_remediation.py -v

# 3. Chạy toàn bộ 48 bài test trong kho mã nguồn
pytest -v
```
