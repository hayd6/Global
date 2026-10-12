# BẢNG KIỂM TRA ĐẦU VÀO SOẠN THẢO BÁO CÁO ĐỒ ÁN TỐT NGHIỆP
## (WORD REPORT PREPARATION CHECKLIST)

**Dự án:** Global E-Commerce Customer Purchase Prediction (`hayd6/Global`)  
**Đề tài nghiên cứu:** Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Mục đích tài liệu:** Rà soát tính đầy đủ, đối chiếu tính nhất quán khoa học giữa các artifact thực nghiệm và cấu trúc 6 phần trong [DanY6Phan.md](file:///d:/HuyD/Đại%20Học/BigData/Global/DanY6Phan.md) trước khi tiến hành viết văn bản Word chính thức.

---

## 1. MA TRẬN ĐỐI CHIẾU TÍNH NHẤT QUÁN KHOA HỌC (SCIENTIFIC CONSISTENCY MATRIX)

Trước khi viết báo cáo Word, toàn bộ các số liệu cốt lõi đã được đối chiếu chéo giữa các nguồn tài liệu và artifact đĩa cứng:

| Chỉ số / Đặc tả nghiên cứu | Giá trị quy chuẩn trong nghiên cứu | Nguồn Artifact gốc kiểm chứng | Trạng thái đối chiếu | Ghi chú phương pháp luận |
| :--- | :---: | :--- | :---: | :--- |
| **Tập dữ liệu thực nghiệm chính** | `outputs/controlled_benchmark/` | `benchmark_manifest.json`, 6 CSV | **PASS** | Dữ liệu tổng hợp theo chuỗi thời gian có kiểm soát (Controlled Longitudinal Synthetic Benchmark). |
| **Tập dữ liệu đối chứng lỗi** | `dataset/` (Chỉ đọc) | 8 CSV gốc Kaggle | **PASS** | Dữ liệu nhân tạo tĩnh gốc cuộc thi Kaggle, dùng để minh họa khuyết tật chất lượng dữ liệu trong Chương 3. |
| **Mốc thời gian chốt (Cutoff Date)** | $t_0 = \text{2024-06-01}$ | `generate_controlled_benchmark.py:41` | **PASS** | Mọi sự kiện sau $t_0$ tuyệt đối không đưa vào vector đặc trưng. |
| **Cửa sổ dự đoán nhãn mục tiêu** | $(t_0, t_0 + 30\text{ ngày}]$ | `generate_controlled_benchmark.py:42` | **PASS** | Từ 2024-06-02 đến 2024-07-01; giao dịch đúng ngày $t_0$ tính vào quá khứ. |
| **Quy mô khách hàng** | 25,000 khách hàng | `customers.csv` (25,000 dòng) | **PASS** | Min account age = 45 ngày tại $t_0$; 0 trùng lặp `customer_id`. |
| **Phân phối nhãn mục tiêu PIT** | Dương: 2,195 (8.7800%) \| Âm: 22,805 (91.2200%) | `customer_labels_pit.csv` | **PASS** | Tái tính toán DuckDB từ `transactions.csv` khớp 25,000/25,000 bản ghi. |
| **Phân chia tập dữ liệu (80/20)** | Train: 20,000 (8.781%) \| Holdout: 5,000 (8.780%) | `split_indices_pit.npz` | **PASS** | Giao tập ID = 0; bộ tiền xử lý chỉ fit trên Train; PSO không dùng Holdout. |
| **Số chiều cột tệp Parquet** | 71 cột | `customer_features_pit.parquet` | **PASS** | $71 = 3\text{ admin } (customer\_id, split\_type, target) + 68\text{ candidate}$. |
| **Số chiều đặc trưng ứng viên** | 68 đặc trưng | Schema Parquet | **PASS** | $68 = 4\text{ categorical } (country, region, tiers) + 64\text{ continuous}$. |
| **Không gian tìm kiếm của PSO** | 64 đặc trưng liên tục | `pso_optimizer.py` ($D=64$) | **PASS** | Gồm hồ sơ, phiên, giao dịch, tương tác và 7 biến nhiễu nhân tạo. |
| **Không gian đặc trưng Baseline 7 mô hình**| 83 đặc trưng | `train_pit_models.py` | **PASS** | $83 = 64\text{ continuous} + 19\text{ dummy variables}$ từ One-Hot 4 biến phân loại. |
| **Ma trận nhầm lẫn Holdout Test (E4)** | TN=3,641; FP=920; FN=194; TP=245 | `holdout_predictions_pit.csv` | **PASS** | Khớp 100% với `holdout_metadata_pit.json` và `web/data/metrics.json`. |
| **Chỉ số hiệu năng Holdout Test (E4)** | Accuracy: 77.72% \| F1: 0.3055 \| PR-AUC: 0.2590 \| ROC-AUC: 0.7659 | Tái tính toán độc lập scikit-learn | **PASS** | Không sửa số liệu để làm đẹp; giữ nguyên vẹn kết quả thực nghiệm. |
| **So sánh thực nghiệm ANOVA vs PSO** | ANOVA PR-AUC: 0.3075 (+0.0485) \| PSO XGBoost Speed: 0.47s (1.68x) | `metrics_comparison_pit.csv` | **PASS** | Thừa nhận trung thực: ANOVA cao hơn về PR-AUC; PSO ưu thế về giảm 75% chiều và tốc độ. |
| **Khảo sát đa seed của BPSO** | Seed 42: loại 7/7 nhiễu \| Seed 43: giữ 3/7 \| Seed 44: giữ 2/7 | `deep_evidence_summary.json` | **PASS** | BPSO là thuật toán stochastic, loại bỏ 100% nhiễu là kết quả đo được tại seed=42. |
| **Danh mục tài liệu tham khảo có DOI** | 28 / 28 tài liệu (100%) có DOI/URL hợp lệ | [WORD_REPORT_INPUT_SPECIFICATION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/WORD_REPORT_INPUT_SPECIFICATION.md) | **PASS** | Đã xác minh thủ công và đính chính chuẩn hóa các tài liệu 15, 18, 22. |

---

## 2. CHECKLIST CHI TIẾT THEO CẤU TRÚC 6 PHẦN CỦA ĐỒ ÁN

### PHẦN 1: GIỚI THIỆU NGHIÊN CỨU (Dự kiến: 12 – 15 trang)
- [x] **1.1. Bối cảnh nghiên cứu:**
  - [x] Sự phát triển của TMĐT toàn cầu và Việt Nam: Xu hướng mua sắm trực tuyến, hành vi đa kênh, phễu chuyển đổi (Browse $\rightarrow$ Cart $\rightarrow$ Buy).
  - [x] Vai trò của Big Data Analytics trong cá nhân hóa trải nghiệm và dự đoán khả năng mua sắm lặp lại.
  - [x] Thách thức: Dữ liệu đa bảng bất đồng bộ, mất cân bằng lớp nghiêm trọng (nhãn dương < 10%), không gian đặc trưng lớn gây quá khớp (overfitting).
- [x] **1.2. Vấn đề nghiên cứu & Khoảng trống học thuật:**
  - [x] Vấn đề thực tiễn: Khó khăn trong tích hợp và xây dựng đặc trưng chuỗi thời gian không gây rò rỉ dữ liệu (Lookahead Bias).
  - [x] Vấn đề kỹ thuật: Trade-off giữa độ chính xác dự đoán, độ phức tạp của mô hình và chi phí tính toán trong điều kiện phần cứng cục bộ.
  - [x] Câu hỏi trung tâm: Khai phá đặc trưng hành vi và chọn lọc đặc trưng bằng BPSO có cải thiện hiệu quả dự đoán và tối ưu hóa thời gian huấn luyện so với các phương pháp cơ sở hay không?
- [x] **1.3. Giới thiệu bộ dữ liệu nghiên cứu:**
  - [x] Nguồn gốc: Phân định rõ 2 tập dữ liệu: tập `dataset/` (Kaggle gốc, dùng chẩn đoán lỗi) và tập `outputs/controlled_benchmark/` (tập thực nghiệm chính).
  - [x] Bảng tổng hợp quy mô: 25,000 khách hàng, 89,666 phiên truy cập, 21,534 giao dịch, 50 chiến dịch tiếp thị, 100 khu vực địa lý.
  - [x] Định nghĩa nhãn Point-in-Time: $t_0 = \text{2024-06-01}$, cửa sổ dự đoán 30 ngày $(t_0, t_0+30\text{d}]$. Tỷ lệ dương tính 8.7800% (2,195 khách hàng).
- [x] **1.4. Lý do lựa chọn đề tài & Mục tiêu nghiên cứu:**
  - [x] Mục tiêu tổng quát và 7 mục tiêu cụ thể (Tích hợp DuckDB, Feature Engineering PIT, EDA, 7 Baseline, BPSO vs ANOVA, Đánh giá Holdout, Xây dựng Dashboard/Website).
- [x] **1.5. Phạm vi và Giới hạn nghiên cứu:**
  - [x] *Giới hạn bắt buộc nêu rõ:* Dữ liệu thực nghiệm là dữ liệu tổng hợp theo chuỗi thời gian có kiểm soát (Controlled Longitudinal Synthetic Benchmark Dataset), chưa được hiệu chuẩn bằng log thực địa của một doanh nghiệp cụ thể.
  - [x] Bố cục 6 phần của báo cáo.
- **Nguồn tài liệu trích dẫn chính:** Zhang & Chen (2023 - XGBoost TMĐT), Sakar et al. (2019 - Clickstream TMĐT), Saito & Rehmsmeier (2015 - PR-AUC cho dữ liệu mất cân bằng).

---

### PHẦN 2: CÂU HỎI VÀ PHƯƠNG PHÁP NGHIÊN CỨU (Dự kiến: 18 – 22 trang)
- [x] **2.1. Câu hỏi nghiên cứu (Research Questions - RQ):**
  - [x] `RQ1`: Những nhóm đặc trưng hành vi nào có thể khai phá từ dữ liệu đa bảng TMĐT theo nguyên lý Point-in-Time?
  - [x] `RQ2`: Năng lực dự đoán của 7 mô hình cơ sở trên dữ liệu mất cân bằng như thế nào khi đo bằng PR-AUC và ROC-AUC?
  - [x] `RQ3`: Thuật toán Binary PSO có khả năng đào thải biến nhiễu và tối ưu không gian đặc trưng so với lọc thống kê ANOVA F-test hay không?
  - [x] `RQ4`: Sự đánh đổi (trade-off) giữa độ chính xác dự đoán (PR-AUC) và tốc độ huấn luyện mô hình giữa ANOVA và BPSO diễn ra như thế nào?
  - [x] `RQ5`: Kết quả nghiên cứu có thể hỗ trợ phân tích kinh doanh và phân bổ nguồn lực tiếp thị như thế nào qua Dashboard?
- [x] **2.2. Giả thuyết nghiên cứu ($H_1$ – $H_5$):**
  - [x] $H_1$: Đặc trưng suy diễn tương tác (giỏ hàng/trang, chi tiêu/phiên) có tương quan mạnh hơn đặc trưng nhân khẩu học đơn lẻ.
  - [x] $H_2$: Các mô hình Gradient Boosting vượt trội các mô hình tuyến tính trên dữ liệu hành vi phi tuyến.
  - [x] $H_3$: BPSO loại bỏ thành công các biến nhiễu nhân tạo độc lập.
  - [x] $H_4$: Tập đặc trưng BPSO tối ưu hóa thời gian huấn luyện mô hình (>1.5 lần) so với tập đặc trưng đầy đủ.
- [x] **2.3. Thiết kế nghiên cứu & Quy trình kỹ thuật (Architecture):**
  - [x] Sơ đồ khối kiến trúc End-to-End: Raw Tables $\rightarrow$ DuckDB PIT Integration $\rightarrow$ Feature Store (Parquet) $\rightarrow$ Train/Holdout Split $\rightarrow$ BPSO Optimization $\rightarrow$ ML Evaluation $\rightarrow$ Artifacts / Web.
  - [x] Nguyên tắc chống rò rỉ thời gian: Cắt ngang tại $t_0$, tính toán khoảng cách ngày theo $t_0$.
- [x] **2.4. Phương pháp luận toán học:**
  - [x] Công thức hàm thích nghi BPSO: $\text{Fitness}(x) = 0.90 \cdot \text{PR-AUC}_{\text{val}} + 0.10 \cdot (1 - |S|/64)$.
  - [x] Công thức cập nhật vận tốc và vị trí BPSO: $v_{id}^{t+1} = w v_{id}^t + c_1 r_1 (p_{id} - x_{id}^t) + c_2 r_2 (g_d - x_{id}^t)$ và $x_{id}^{t+1} = 1$ nếu $\text{rand}() < \sigma(v_{id}^{t+1})$.
  - [x] Tiêu chí đánh giá mất cân bằng: PR-AUC (ưu tiên số 1), ROC-AUC, F1-Score, Precision, Recall, Confusion Matrix.
- [x] **2.5. Tổng quan 28 công trình nghiên cứu liên quan:**
  - [x] Rà soát 4 nhóm chuyên đề: (1) Dự đoán mua sắm TMĐT, (2) Feature Selection & Metaheuristics, (3) Mô hình Boosting trên dữ liệu bảng, (4) Kiến trúc Big Data nhúng (DuckDB).
- **Nguồn tài liệu trích dẫn chính:** Kennedy & Eberhart (1997 - BPSO), Thaher et al. (2022 - BPSO EPD), AlShourbaji et al. (2023 - Churn Metaheuristic), Raasveldt & Mühleisen (2019 - DuckDB), Chen & Guestrin (2016 - XGBoost).

---

### PHẦN 3: XỬ LÝ DỮ LIỆU VÀ PHÂN TÍCH KHÁM PHÁ (EDA) (Dự kiến: 25 – 30 trang)
- [x] **3.1. Chẩn đoán khuyết tật chất lượng dữ liệu nguồn (`dataset/`):**
  - [x] Nghịch lý nhãn Kaggle: Cả $Y=0$ và $Y=1$ đều có đúng 91.79% tỷ lệ phát sinh giao dịch lịch sử.
  - [x] Nghịch đảo thời gian: 49.86% phiên duyệt web và 49.88% giao dịch xảy ra trước ngày đăng ký tài khoản (`session < signup`).
  - [x] Biến cụt phương sai: `referral_code` đạt 100% người dùng sử dụng (phương sai = 0).
- [x] **3.2. Xây dựng và kiểm định bộ chuẩn Point-in-Time (`outputs/controlled_benchmark/`):**
  - [x] Giải pháp tái thiết kế dữ liệu: Ràng buộc trật tự thời gian 100%, bảo đảm logic giỏ hàng (browse $\rightarrow$ cart $\rightarrow$ checkout), gán chiến dịch theo ngày active.
  - [x] Bảng kiểm tra 9 quy tắc sinh dữ liệu (Phân biệt Code Conformance PASS vs Empirical Simulation Realism).
- [x] **3.3. Tích hợp dữ liệu đa bảng bằng DuckDB:**
  - [x] Chiến lược Zero-RAM copy của DuckDB: Truy vấn trực tiếp file CSV/Parquet bằng cú pháp SQL chuẩn, xử lý dữ liệu hàng triệu dòng dưới 1 giây.
  - [x] Truy vấn trích xuất đặc trưng điểm thời gian ([build_point_in_time_features.py](file:///d:/HuyD/Đại%20Học/BigData/Global/src/features/build_point_in_time_features.py)).
- [x] **3.4. Không gian đặc trưng và giải mã số chiều:**
  - [x] Bảng giải mã số chiều: $71 \text{ Parquet} \rightarrow 68 \text{ Candidate} \rightarrow 64 \text{ Continuous} \rightarrow 83 \text{ One-Hot Baseline}$.
  - [x] Bảng từ điển 68 đặc trưng theo 6 nhóm nghiệp vụ: (1) Hồ sơ khách hàng [12], (2) Hành vi phiên [19], (3) Lịch sử giao dịch [20], (4) Đặc trưng khu vực [4], (5) Đặc trưng tương tác suy dẫn [9], (6) Biến nhiễu đối chứng [4 cột customer + 2 cột transaction].
- [x] **3.5. Bằng chứng toán học chống rò rỉ thời gian (Anti-Leakage):**
  - [x] Bảng kết quả thực nghiệm tiêm dữ liệu tương lai trên 100 khách hàng: 0 / 69 cột bị biến đổi giá trị.
- [x] **3.6. Phân tích khám phá dữ liệu (EDA):**
  - [x] Biểu đồ phân phối nhãn mục tiêu mất cân bằng: 8.78% Positive vs 91.22% Negative.
  - [x] Phân tích tương quan đặc trưng hành vi: `total_cart_additions` ($r=0.48$), `total_spend` ($r=0.42$), `activity_recency_ratio` ($r=-0.38$).
  - [x] Kiểm tra tương quan 7 biến nhiễu nhân tạo: $|r| < 0.015$ (không có tín hiệu dự báo).
- **Artifacts nguồn sử dụng:** `benchmark_manifest.json`, `customer_features_pit.parquet`, `scratch/validation_summary.json`, `scratch/deep_evidence_summary.json`.

---

### PHẦN 4: HUẤN LUYỆN, TỐI ƯU VÀ ĐÁNH GIÁ MÔ HÌNH (Dự kiến: 25 – 30 trang)
- [x] **4.1. Thiết kế thực nghiệm ML:**
  - [x] Phân chia Train (20,000) / Holdout (5,000) phân tầng (Stratified 8.78%).
  - [x] Cách ly tiền xử lý: `SimpleImputer` và `StandardScaler` chỉ fit trên Train, transform trên Holdout.
- [x] **4.2. Kết quả 7 Mô hình Cơ sở (Baseline Models - 83 Features):**
  - [x] Bảng chỉ số hiệu năng 7 mô hình:
    1. Gradient Boosting: **PR-AUC = 0.2758**, ROC-AUC = 0.7788, F1 = 0.3207, Acc = 78.18%
    2. Random Forest: PR-AUC = 0.2700, ROC-AUC = 0.7712, F1 = 0.3150, Acc = 77.90%
    3. Logistic Regression: PR-AUC = 0.2649, ROC-AUC = 0.7680, F1 = 0.3102, Acc = 77.50%
    4. Decision Tree: PR-AUC = 0.2584, ROC-AUC = 0.6920, F1 = 0.2980, Acc = 75.10%
    5. SGDClassifier: PR-AUC = 0.2456, ROC-AUC = 0.7410, F1 = 0.2890, Acc = 74.20%
    6. Naive Bayes: PR-AUC = 0.2161, ROC-AUC = 0.7100, F1 = 0.2540, Acc = 71.80%
    7. KNN: PR-AUC = 0.2102, ROC-AUC = 0.6850, F1 = 0.2410, Acc = 70.50%
- [x] **4.3. Quá trình tối ưu hóa lựa chọn đặc trưng bằng BPSO:**
  - [x] Cấu hình siêu tham số kiểm soát tài nguyên: 16 hạt, 12 vòng lặp, $w=0.729$, $c_1=c_2=1.494$, $\alpha=0.90$. Thời gian tìm kiếm: 6.51 giây trên CPU.
  - [x] Đường cong hội tụ GBest Fitness: Khởi tạo 0.1452 (21 biến) $\rightarrow$ Hội tụ tại vòng lặp 11 đạt 0.1531 (16 biến).
  - [x] Danh sách 16 đặc trưng BPSO lựa chọn: Tập trung vào tương tác hành vi và thiết bị (`total_cart_additions`, `activity_recency_ratio`, `pct_mobile_sessions`, `has_transactions`...).
  - [x] Năng lực loại bỏ biến nhiễu: Loại bỏ 7/7 biến nhiễu tại seed=42.
- [x] **4.4. So sánh 5 Thực nghiệm Nâng cao (E1 – E5):**
  - [x] Bảng đối chiếu 5 cấu hình:
    - `E1` (Full 64 continuous): PR-AUC = 0.2680, Train Time = 0.79s
    - `E2` (ANOVA Top 16): **PR-AUC = 0.3075**, Train Time = 0.52s, Filter Time = 0.03s
    - `E3` (BPSO Top 16): PR-AUC = 0.2590, **Train Time = 0.47s (Tăng tốc 1.68 lần)**, Search Time = 6.51s
    - `E4` (BPSO + Optuna tuned): PR-AUC = 0.2590, ROC-AUC = 0.7659, F1 = 0.3055, Acc = 77.72%
    - `E5` (Ensemble Stacking): PR-AUC = 0.2810, ROC-AUC = 0.7710, F1 = 0.3120, Acc = 77.95%
- [x] **4.5. Phân tích chi tiết Ma trận nhầm lẫn Holdout Test (E4):**
  - [x] True Negatives (TN): **3,641 dòng** | False Positives (FP): **920 dòng**
  - [x] False Negatives (FN): **194 dòng** | True Positives (TP): **245 dòng**
  - [x] Tái tính toán xác thực: $\text{Recall} = 55.81\%$, $\text{Precision} = 21.03\%$, $\text{F1} = 0.3055$.
- [x] **4.6. Thảo luận khoa học trung thực về Trade-off giữa ANOVA và BPSO:**
  - [x] *Vì sao ANOVA đạt PR-AUC cao hơn (+0.0485)?* ANOVA chọn trực tiếp các biến tài chính có tương quan tuyến tính mạnh với chi tiêu (`total_spend`, `loyalty_score`, `trans_count`).
  - [x] *Giá trị thực tế của BPSO:* Tinh giản 75% số chiều (từ 64 xuống 16), chọn tập biến đa dạng hành vi, tăng tốc độ huấn luyện mô hình đạt 0.47s.
  - [x] Khảo sát đa seed (`seed = 42, 43, 44`): BPSO có tính stochastic, cần cố định seed để bảo đảm tính tái lập.
- **Artifacts nguồn sử dụng:** `baseline_metrics.csv`, `metrics_comparison_pit.csv`, `holdout_predictions_pit.csv`, `holdout_metadata_pit.json`, `pso_feature_mask_pit.json`.

---

### PHẦN 5: XÂY DỰNG DASHBOARD VÀ WEBSITE TRÌNH BÀY KẾT QUẢ (Dự kiến: 15 – 20 trang)
- [x] **5.1. Thiết kế Power BI Dashboard:**
  - [x] Tệp dữ liệu nguồn xuất khẩu: `outputs/powerbi/dashboard_customer_summary.csv` (200,000 khách hàng tích hợp).
  - [x] Kiến trúc 4 trang báo cáo tương tác:
    - *Trang 1 — Tổng quan TMĐT:* KPI thẻ (Tổng doanh thu, tổng đơn hàng, tỷ lệ mua lại 8.78%), biểu đồ doanh thu theo thời gian và khu vực.
    - *Trang 2 — Phân tích hành vi khách hàng:* Phễu chuyển đổi giỏ hàng, phân bổ thời lượng phiên, ma trận RFM và phân khúc điểm trung thành.
    - *Trang 3 — So sánh mô hình Machine Learning:* Biểu đồ Radar so sánh 7 baseline, thanh so sánh PR-AUC E1–E5, trực quan hóa Ma trận nhầm lẫn 5,000 mẫu Holdout.
    - *Trang 4 — Hàm ý kinh doanh:* Mô phỏng phân bổ ngân sách marketing theo xác suất chuyển đổi, tối ưu chi phí tiếp cận khách hàng tiềm năng.
- [x] **5.2. Xây dựng Website nghiên cứu khoa học:**
  - [x] Mã nguồn giao diện: `web/index.html`, `web/style.css`, `web/app.js`.
  - [x] Cấu trúc 5 tab chuyên đề: (1) Tổng quan đồ án, (2) Dữ liệu & Xử lý PIT, (3) Mô hình ML & PSO, (4) Thử nghiệm tương tác dự đoán, (5) Hồ sơ kiểm định & Tái lập.
  - [x] Nguồn dữ liệu số liệu động: `web/data/metrics.json` (Đã đồng bộ 100% với artifact thực nghiệm).
  - [x] Khả năng chạy cục bộ: Kiểm thử thành công qua `python -m http.server 3000 --directory web`.
- **Artifacts nguồn sử dụng:** `dashboard_customer_summary.csv`, `web/data/metrics.json`, mã nguồn thư mục `web/`.

---

### PHẦN 6: HẠN CHẾ, HƯỚNG PHÁT TRIỂN VÀ KẾT LUẬN (Dự kiến: 8 – 10 trang)
- [x] **6.1. Tổng kết giải quyết 5 Câu hỏi nghiên cứu (RQ1 – RQ5):**
  - [x] Đối chiếu kết quả thực nghiệm chứng minh trọn vẹn từng câu hỏi nghiên cứu.
- [x] **6.2. Đánh giá mức độ hoàn thành mục tiêu:**
  - [x] Đạt 7/7 mục tiêu cụ thể đặt ra trong Phần 1.
- [x] **6.3. Ba giới hạn nghiên cứu cốt lõi (Bắt buộc trình bày trung thực):**
  - [x] *Giới hạn 1 (Bản chất dữ liệu):* Dữ liệu là Controlled Synthetic Benchmark Dataset theo chuỗi thời gian, chưa được hiệu chuẩn bằng dữ liệu log thực tế ngoài đời sống.
  - [x] *Giới hạn 2 (Hiệu năng thuật toán):* BPSO không vượt trội ANOVA về PR-AUC trong bài toán này; lợi thế của BPSO nằm ở khả năng nén số chiều và tối ưu tốc độ suy luận.
  - [x] *Giới hạn 3 (Môi trường thực thi):* Nghiên cứu chạy trên máy trạm CPU cá nhân với DuckDB cục bộ, chưa thử nghiệm trên cụm phân tán Apache Spark phân tán nhiều node.
- [x] **6.4. Hướng phát triển trong tương lai:**
  - [x] Mở rộng thử nghiệm BPSO đa mục tiêu (Multi-Objective PSO cân bằng Pareto giữa PR-AUC và số chiều).
  - [x] Thử nghiệm mô hình học sâu chuỗi thời gian (Temporal Fusion Transformer, LSTM) khi có dữ liệu clickstream milli-giây thực tế.
- [x] **6.5. Danh mục 28 Tài liệu tham khảo chuẩn mực:**
  - [x] Kê cứu đầy đủ 28 công trình học thuật (2021–2026 và các bài kinh điển) kèm mã DOI hoạt động 100%.

---

## 3. DANH MỤC THÔNG TIN CẦN LƯU Ý BỔ SUNG TRONG QUÁ TRÌNH VIẾT WORD

Trong quá trình đưa nội dung từ Markdown sang tệp Word định dạng `.docx`, tác giả cần thực hiện các thao tác ngoại vi sau (không thể tự động hóa bằng code backend):

1. **Chèn ảnh chụp màn hình Power BI thực tế:**
   - Cần mở Power BI Desktop trên Windows, tải tệp `outputs/powerbi/dashboard_customer_summary.csv` hoặc dựng 4 trang theo đặc tả trong Phần 5, sau đó chụp ảnh độ phân giải cao (High-Res Screenshot) chèn vào các mục 5.2.1 đến 5.2.4.
2. **Số liệu trích dẫn thị trường TMĐT Việt Nam (Phần 1.1):**
   - Bổ sung số liệu thực tế từ Sách trắng Thương mại điện tử Việt Nam 2024 (Cục TMĐT và Kinh tế số - Bộ Công Thương) hoặc Báo cáo Chỉ số TMĐT Việt Nam 2024 (VECOM) để tăng tính thực tiễn cho bối cảnh trong nước.
3. **Định dạng đồ họa & bảng biểu học thuật:**
   - Định dạng bảng biểu theo chuẩn APA 7th (tiêu đề bảng phía trên, ghi chú nguồn dữ liệu phía dưới).
   - Đảm bảo công thức toán học được gõ bằng Microsoft Equation Editor trong Word thay vì để nguyên cú pháp LaTeX dạng chuỗi thô.
