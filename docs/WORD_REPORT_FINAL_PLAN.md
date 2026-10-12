# KẾ HOẠCH TRIỂN KHAI VIẾT BÁO CÁO ĐỒ ÁN TỐT NGHIỆP BẰNG MICROSOFT WORD
## (FINAL WORD REPORT WRITING PLAN & DETAILED SECTION BLUEPRINT)

**Dự án:** Global E-Commerce Customer Purchase Prediction (`hayd6/Global`)  
**Tên đề tài tiếng Việt:** Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Tên đề tài tiếng Anh:** Behavioral Feature Mining and PSO-Driven Feature Selection for Customer Purchase Prediction in E-Commerce  
**Căn cứ triển khai:**
- Dàn ý phân công 6 phần: [DanY6Phan.md](file:///d:/HuyD/Đại%20Học/BigData/Global/DanY6Phan.md)
- Bảng đặc tả đầu vào số liệu: [docs/WORD_REPORT_INPUT_SPECIFICATION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/WORD_REPORT_INPUT_SPECIFICATION.md)
- Báo cáo kiểm định dữ liệu độc lập: [docs/INDEPENDENT_DATA_VALIDATION_REPORT.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/INDEPENDENT_DATA_VALIDATION_REPORT.md)
- Quyết định khóa hồ sơ dữ liệu: [docs/FINAL_DATA_VALIDATION_DECISION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/FINAL_DATA_VALIDATION_DECISION.md)
- Bảng kiểm tra đầu vào: [docs/WORD_REPORT_PREPARATION_CHECKLIST.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/WORD_REPORT_PREPARATION_CHECKLIST.md)

---

## TỔNG QUAN KẾ HOẠCH VÀ QUY CHUẨN ĐỊNH DẠNG VĂN BẢN

- **Phần mềm sử dụng:** Microsoft Word (định dạng tệp tin `.docx`).
- **Khổ giấy & Căn lề chuẩn học thuật:** Khổ A4, lề trên 2.0 cm, lề dưới 2.0 cm, lề trái 3.0 cm (để đóng gáy), lề phải 2.0 cm.
- **Phông chữ & Giãn dòng:** Times New Roman, cỡ chữ 13 pt, giãn dòng 1.3 lines, giãn đoạn Before 0 pt, After 6 pt.
- **Đánh số đề mục:** Đánh số phân cấp tối đa 4 cấp (ví dụ: `4.4.2.1`).
- **Bảng biểu & Hình ảnh:** Đánh số theo chương (ví dụ: `Bảng 4.2`, `Hình 3.1`), tiêu đề bảng đặt phía trên, tiêu đề hình đặt phía dưới; bắt buộc ghi rõ nguồn trích dẫn dữ liệu.
- **Công thức toán học:** Định dạng bằng Microsoft Equation Editor chuyên nghiệp, đánh số thứ tự công thức góc phải (ví dụ: `(2.4)`).
- **Quy mô dự kiến:** Khoảng 100 – 120 trang (chưa tính phụ lục).

---

## KẾ HOẠCH TRIỂN KHAI CHI TIẾT THEO 6 PHẦN

### PHẦN 1. GIỚI THIỆU NGHIÊN CỨU (Dự kiến: 12 – 15 trang)

#### 1. Mục tiêu và Nội dung cần trình bày
- Dẫn dắt người đọc từ bức tranh vĩ mô của thương mại điện tử (TMĐT) và dữ liệu lớn (Big Data) đến bài toán dự đoán hành vi khách hàng.
- Khẳng định tính cấp thiết của việc kết hợp dữ liệu đa nguồn (hồ sơ, phiên truy cập, giỏ hàng, giao dịch, chiến dịch) theo trật tự thời gian.
- Trình bày rõ ràng vấn đề nghiên cứu, câu hỏi trung tâm, mục tiêu tổng quát, 7 mục tiêu cụ thể, phạm vi và giới hạn dữ liệu.

#### 2. Các tiểu mục chi tiết cần viết
- **1.1. Bối cảnh nghiên cứu:**
  - `1.1.1. Sự phát triển của thương mại điện tử:` Xu hướng tăng trưởng kinh tế số, hành vi mua sắm đa kênh, sự bùng nổ dữ liệu log clickstream.
  - `1.1.2. Vai trò của dữ liệu trong hoạt động kinh doanh:` Phân biệt phân tích mô tả, phân tích dự đoán và hỗ trợ quyết định phân bổ ngân sách marketing.
  - `1.1.3. Thách thức khai thác dữ liệu hành vi:` Kích thước bảng chênh lệch lớn, dữ liệu bảng phi tuyến, mất cân bằng nhãn nghiêm trọng (< 10%).
  - `1.1.4. Dẫn vào hướng nghiên cứu:` Nhu cầu khai phá đặc trưng hành vi suy diễn và tối ưu hóa không gian đặc trưng bằng metaheuristic (PSO).
- **1.2. Vấn đề nghiên cứu:**
  - `1.2.1. Vấn đề thực tiễn:` Khó khăn trong tích hợp dữ liệu đa bảng thành hồ sơ khách hàng 360 độ mà không làm nghẽn RAM máy tính thông thường.
  - `1.2.2. Vấn đề kỹ thuật:` Đánh đổi (trade-off) giữa việc dùng toàn bộ đặc trưng gây quá khớp/tăng chi phí tính toán và việc nén đặc trưng.
  - `1.2.3. Khoảng trống nghiên cứu:` Thiếu các nghiên cứu thực nghiệm đối chiếu sòng phẳng giữa lọc thống kê (ANOVA) và metaheuristic (BPSO) trên cùng bài toán Point-in-Time.
  - `1.2.4. Phát biểu vấn đề nghiên cứu:` Chốt câu hỏi trung tâm của đồ án.
- **1.3. Giới thiệu bộ dữ liệu nghiên cứu:**
  - `1.3.1. Nguồn dữ liệu & Hai tập dữ liệu đối chứng:` Phân định rõ tập gốc `dataset/` (Kaggle) và tập chuẩn kiểm soát `outputs/controlled_benchmark/`.
  - `1.3.2. Quy mô và cấu trúc dữ liệu:` Bảng tổng hợp số lượng dòng, số cột, kiểu dữ liệu 6 bảng nguồn.
  - `1.3.3. Vai trò của từng bảng và khóa liên kết:` `customer_id`, `session_id`, `transaction_id`, `campaign_id`, `geo_ip_region`.
  - `1.3.4. Biến mục tiêu Point-in-Time:` Khái niệm mốc cắt $t_0 = \text{2024-06-01}$ và cửa sổ nhãn 30 ngày $(t_0, t_0+30\text{d}]$.
- **1.4. Lý do lựa chọn đề tài và dataset:** Tính đại diện cho bài toán TMĐT, tính thách thức Big Data, tính phù hợp cho BPSO và khả năng triển khai trên CPU máy tính cá nhân qua DuckDB.
- **1.5. Mục tiêu nghiên cứu:** Mục tiêu tổng quát và 7 mục tiêu cụ thể.
- **1.6. Đối tượng, phạm vi và giới hạn nghiên cứu:**
  - `1.6.1. Đối tượng nghiên cứu.`
  - `1.6.2. Phạm vi dữ liệu.`
  - `1.6.3. Phạm vi kỹ thuật.`
  - `1.6.4. Giới hạn bắt buộc nêu rõ:` Dữ liệu là Controlled Synthetic Benchmark Dataset, phục vụ kiểm chứng thuật toán mô phỏng.
- **1.7. Đóng góp dự kiến và điểm khác biệt:** Đóng góp về phương pháp luận Point-in-Time, đóng góp thực nghiệm kiểm chứng BPSO vs ANOVA, đóng góp sản phẩm (Dashboard & Web).
- **1.8. Bố cục báo cáo:** Tóm tắt nội dung 6 phần tiếp theo.

#### 3. Bảng biểu, Số liệu và Công thức
- **Bảng 1.1:** Bảng tổng quan quy mô bộ dữ liệu kiểm soát (25,000 khách hàng, 89,666 phiên, 21,534 giao dịch, 50 chiến dịch, 100 khu vực).
- **Hình 1.1:** Sơ đồ quan hệ thực thể (ERD) giữa 6 bảng dữ liệu.
- **Số liệu bắt buộc:** 25,000 khách hàng; tỷ lệ dương tính 8.7800% (2,195 khách hàng); cửa sổ quan sát $\ge 45$ ngày; mốc cắt 01/06/2024.

#### 4. Nguồn dữ liệu và Tài liệu tham khảo
- Nguồn: `benchmark_manifest.json`, `customers.csv`.
- Tài liệu trích dẫn: Zhang & Chen (2023), Sakar et al. (2019), Saito & Rehmsmeier (2015).

#### 5. Thảo luận & Giới hạn
- Phải tuyên bố minh bạch: Đây là nghiên cứu thực nghiệm trên bộ dữ liệu tổng hợp có kiểm soát, không đại diện cho dữ liệu kinh doanh của một sàn TMĐT cụ thể ngoài đời thực.

---

### PHẦN 2. CÂU HỎI VÀ PHƯƠNG PHÁP NGHIÊN CỨU (Dự kiến: 18 – 22 trang)

#### 1. Mục tiêu và Nội dung cần trình bày
- Hệ thống hóa 5 câu hỏi nghiên cứu (`RQ1` – `RQ5`) và 5 giả thuyết nghiên cứu tương ứng ($H_1$ – $H_5$).
- Thiết lập cơ sở lý thuyết toán học cho mô hình Point-in-Time, thuật toán Binary PSO, ANOVA F-test và các mô hình Boosting.
- Tổng quan tài liệu học thuật theo 4 chuyên đề lớn dựa trên 28 bài báo đã được xác minh DOI.

#### 2. Các tiểu mục chi tiết cần viết
- **2.1. Mục tiêu và định hướng nghiên cứu:** Chi tiết hóa các chỉ tiêu kỹ thuật cần đạt.
- **2.2. Câu hỏi nghiên cứu (RQ1 – RQ5):**
  - `RQ1:` Các nhóm đặc trưng hành vi nào có thể khai phá từ dữ liệu đa bảng mà không gây rò rỉ thời gian?
  - `RQ2:` Khả năng phân loại của 7 mô hình Machine Learning cơ sở trên dữ liệu mất cân bằng như thế nào?
  - `RQ3:` BPSO có khả năng đào thải biến nhiễu nhân tạo và tối ưu hóa số chiều tốt hơn lọc thống kê ANOVA hay không?
  - `RQ4:` Trade-off giữa độ chính xác dự đoán (PR-AUC) và tốc độ huấn luyện mô hình giữa ANOVA và BPSO như thế nào?
  - `RQ5:` Làm thế nào để trực quan hóa kết quả nghiên cứu hỗ trợ ra quyết định kinh doanh qua Dashboard tương tác?
- **2.3. Giả thuyết nghiên cứu:** Phát biểu hình thức $H_1$, $H_2$, $H_3$, $H_4$, $H_5$.
- **2.4. Thiết kế nghiên cứu và Quy trình kỹ thuật tổng thể:**
  - `2.4.1. Kiến trúc luồng dữ liệu End-to-End:` Trình bày chi tiết luồng dữ liệu từ bảng thô đến web portal.
  - `2.4.2. Nguyên tắc Point-in-Time & Anti-Leakage First:` Cơ sở toán học của việc chặn thông tin tại $t_0$.
  - `2.4.3. Phân tách tập dữ liệu nghiêm ngặt:` Tỷ lệ 80/20 (Train 20,000 / Holdout 5,000), nguyên tắc fit/transform của preprocessor.
- **2.5. Phương pháp luận toán học và thuật toán:**
  - `2.5.1. Công thức hàm thích nghi BPSO:` Thiết lập hàm mục tiêu kết hợp PR-AUC và phạt số chiều.
  - `2.5.2. Toán học giải thuật Binary PSO:` Biểu diễn nghiệm nhị phân, quy tắc cập nhật vận tốc/vị trí, hàm kích hoạt sigmoid.
  - `2.5.3. Phương pháp lọc thống kê ANOVA F-test:` Công thức tính F-statistic và cơ chế xếp hạng p-value.
  - `2.5.4. Các mô hình Machine Learning:` Cơ chế phân loại của Logistic Regression, Random Forest, Gradient Boosting, XGBoost.
- **2.6. Tiêu chí đánh giá chất lượng mô hình:**
  - `2.6.1. Chỉ số đánh giá trên dữ liệu mất cân bằng:` Ưu thế vượt trội của PR-AUC so với ROC-AUC, công thức F1-Score, Precision, Recall.
  - `2.6.2. Tiêu chí đo lường hiệu quả tính toán:` Thời gian tìm kiếm đặc trưng, thời gian huấn luyện mô hình, tỷ lệ nén số chiều.
- **2.7. Tổng quan nghiên cứu liên quan (Literature Review):**
  - Phân tích 4 nhóm: (1) Dự đoán mua hàng TMĐT, (2) Lựa chọn đặc trưng bằng Metaheuristic, (3) Mô hình Boosting trên dữ liệu bảng, (4) Kiến trúc Big Data nhúng với DuckDB.

#### 3. Bảng biểu, Số liệu và Công thức
- **Công thức (2.1) — Hàm thích nghi BPSO:**
  $$\text{Fitness}(x) = 0.90 \cdot \text{PR-AUC}_{\text{val}} + 0.10 \cdot \left(1 - \frac{|S|}{64}\right)$$
- **Công thức (2.2) & (2.3) — Cập nhật vận tốc và vị trí BPSO:**
  $$v_{id}^{t+1} = w v_{id}^t + c_1 r_1 (p_{id} - x_{id}^t) + c_2 r_2 (g_d - x_{id}^t)$$
  $$x_{id}^{t+1} = \begin{cases} 1 & \text{nếu } \text{rand}() < \frac{1}{1 + \exp(-v_{id}^{t+1})} \\ 0 & \text{ngược lại} \end{cases}$$
- **Hình 2.1:** Sơ đồ quy trình nghiên cứu tổng thể (Pipeline Flowchart).
- **Bảng 2.1:** Bảng tổng hợp so sánh các nghiên cứu tương đồng trong giai đoạn 2021 – 2026.

#### 4. Nguồn dữ liệu và Tài liệu tham khảo
- Trích dẫn chính: Kennedy & Eberhart (1997), Thaher et al. (2022), Tijjani et al. (2024), Hu et al. (2026), Hachaichi et al. (2024), Raasveldt & Mühleisen (2019), Chen & Guestrin (2016).

#### 5. Thảo luận & Giới hạn
- Nêu rõ vì sao không chọn Accuracy làm chỉ số tối ưu (do tỷ lệ nhãn âm chiếm 91.22%, đoán toàn bộ âm tính vẫn đạt Acc 91.22% nhưng vô giá trị nghiệp vụ).

---

### PHẦN 3. XỬ LÝ DỮ LIỆU VÀ PHÂN TÍCH KHÁM PHÁ (EDA) (Dự kiến: 25 – 30 trang)

#### 1. Mục tiêu và Nội dung cần trình bày
- Phơi bày toàn diện các khuyết tật chất lượng dữ liệu của tập Kaggle nguồn `dataset/` (nghịch lý nhãn, nghịch đảo thời gian).
- Trình bày giải pháp khắc phục bằng bộ dữ liệu kiểm soát `outputs/controlled_benchmark/` và kiểm định 9 quy tắc sinh dữ liệu.
- Phân tích kiến trúc tích hợp DuckDB, xây dựng 68 đặc trưng hành vi và chứng minh tính trơ thời gian trên 69 cột.
- Báo cáo phân tích khám phá dữ liệu (EDA) trực quan, mối quan hệ tương quan và phân phối nhãn.

#### 2. Các tiểu mục chi tiết cần viết
- **3.1. Chẩn đoán khuyết tật chất lượng dữ liệu nguồn (`dataset/`):**
  - `3.1.1. Nghịch lý phân phối nhãn Kaggle:` Chứng minh cả $Y=0$ và $Y=1$ đều có 91.79% giao dịch lịch sử.
  - `3.1.2. Nghịch đảo trật tự thời gian:` 49.86% phiên truy cập và 49.88% giao dịch xảy ra trước ngày đăng ký tài khoản.
  - `3.1.3. Lỗi phương sai và tính phi thực tế:` Cột `referral_code` bị gán 100% (phương sai bằng 0).
- **3.2. Thiết kế và kiểm định bộ chuẩn Point-in-Time (`outputs/controlled_benchmark/`):**
  - `3.2.1. Logic chuỗi sự kiện TMĐT hợp lệ:` Phễu Browse $\rightarrow$ Cart $\rightarrow$ Buy.
  - `3.2.2. Kiểm định 9 quy tắc sinh dữ liệu:` Bảng đối chiếu chi tiết giữa lý thuyết và đo đạc thực tế.
  - `3.2.3. Thiết lập biến đối chứng khoa học:` Cơ chế tạo 7 biến nhiễu Gaussian $\mathcal{N}(0, 1)$.
- **3.3. Tích hợp dữ liệu đa bảng bằng DuckDB:**
  - `3.3.1. Ưu thế kỹ thuật của DuckDB trên dữ liệu lớn cục bộ:` Cơ chế thực thi vector hóa (Vectorized Execution), Columnar Storage, không tràn bộ nhớ RAM.
  - `3.3.2. Truy vấn tích hợp Point-in-Time:` Trình bày mã SQL tích hợp sessions và transactions có mệnh đề chặn ngày $\le t_0$.
- **3.4. Xây dựng không gian đặc trưng hành vi (Feature Engineering):**
  - `3.4.1. Giải mã các con số chiều đặc trưng:` Phân tích rõ đại số $71 \rightarrow 68 \rightarrow 64 \rightarrow 83$.
  - `3.4.2. Từ điển 68 đặc trưng nghiệp vụ theo 6 nhóm:` Bảng định nghĩa chi tiết tên biến, kiểu dữ liệu, ý nghĩa nghiệp vụ.
- **3.5. Kiểm định tính trơ thời gian (Temporal Invariance Test):**
  - `3.5.1. Thiết kế kịch bản tiêm nhiễu tương lai:` Tiêm giao dịch sau $t_0$ cho 100 khách hàng.
  - `3.5.2. Kết quả đo đạc:` 0 / 69 cột bị biến đổi giá trị (Bằng chứng không rò rỉ dữ liệu tương lai).
- **3.6. Phân tích khám phá dữ liệu (EDA):**
  - `3.6.1. Phân tích phân phối nhãn mục tiêu:` 8.78% Positive vs 91.22% Negative.
  - `3.6.2. Phân tích tương quan đặc trưng hành vi với nhãn mua hàng.`
  - `3.6.3. Kiểm tra tính độc lập của 7 biến nhiễu.`
- **3.7. Chuẩn bị dữ liệu cho Machine Learning:** Lưu trữ dưới dạng Parquet tối ưu, phân chia Train/Holdout (80/20).

#### 3. Bảng biểu, Số liệu và Công thức
- **Bảng 3.1:** Bảng so sánh đối đầu giữa bộ dữ liệu gốc Kaggle (`dataset/`) và bộ chuẩn kiểm soát (`outputs/controlled_benchmark/`).
- **Bảng 3.2:** Bảng kiểm tra 9 quy tắc sinh dữ liệu (Vị trí code, Cơ sở, Kiểm tra độc lập, Kết quả, Đánh giá).
- **Bảng 3.3:** Bảng từ điển 68 đặc trưng ứng viên (Feature Dictionary) phân loại theo 6 nhóm.
- **Bảng 3.4:** Bảng giải thích chi tiết 4 con số chiều đặc trưng (71, 68, 64, 83).
- **Hình 3.1:** Biểu đồ phân phối nhãn mục tiêu Point-in-Time.
- **Hình 3.2:** Ma trận tương quan nhiệt (Correlation Heatmap) giữa các đặc trưng hành vi và nhãn mục tiêu.

#### 4. Nguồn dữ liệu và Tài liệu tham khảo
- Nguồn: `benchmark_manifest.json`, `customer_features_pit.parquet`, `scratch/validation_summary.json`.
- Tài liệu trích dẫn: Raasveldt & Mühleisen (2019), Sakar et al. (2019).

#### 5. Thảo luận & Giới hạn
- Nêu rõ: Cấu trúc tương quan giữa biến tiềm ẩn $z_i$ và các biến hành vi là giả định toán học của bộ sinh, không phải luật nhân quả tất yếu ngoài đời thực.

---

### PHẦN 4. XÂY DỰNG, HUẤN LUYỆN VÀ TỐI ƯU MÔ HÌNH (Dự kiến: 25 – 30 trang)

#### 1. Mục tiêu và Nội dung cần trình bày
- Báo cáo kết quả huấn luyện và đánh giá 7 mô hình Machine Learning cơ sở trên 83 đặc trưng baseline.
- Trình bày chi tiết tiến trình tối ưu hóa lựa chọn đặc trưng bằng thuật toán BPSO trên không gian 64 chiều.
- So sánh toàn diện 5 cấu hình thực nghiệm nâng cao (E1 – E5).
- Phân tích chi tiết ma trận nhầm lẫn Holdout Test của mô hình chính thức E4.
- Thảo luận khoa học trung thực về sự đánh đổi giữa ANOVA F-test và BPSO; công bố kết quả khảo sát đa seed.

#### 2. Các tiểu mục chi tiết cần viết
- **4.1. Thiết kế thực nghiệm Machine Learning:**
  - `4.1.1. Phân chia tập dữ liệu phân tầng:` Train (20,000) và Holdout (5,000), cùng tỷ lệ dương tính 8.78%.
  - `4.1.2. Pipeline tiền xử lý cô lập:` Imputer, Scaler, One-Hot chỉ fit trên Train.
- **4.2. Huấn luyện và Đánh giá 7 Mô hình Cơ sở (83 Features):**
  - `4.2.1. Cấu hình và tham số 7 mô hình:` Gradient Boosting, Random Forest, Logistic Regression, Decision Tree, SGDClassifier, Naive Bayes, KNN.
  - `4.2.2. Bảng kết quả so sánh hiệu năng 7 mô hình:` Phân tích chi tiết vị trí dẫn đầu của Gradient Boosting (PR-AUC = 0.2758).
- **4.3. Quá trình tối ưu hóa lựa chọn đặc trưng bằng Binary PSO:**
  - `4.3.1. Thiết lập tham số và cơ chế kiểm soát tài nguyên:` 16 hạt, 12 vòng lặp, thời gian chạy 6.51 giây.
  - `4.3.2. Động lực học bầy đàn và tiến trình hội tụ:` Phân tích đường cong GBest Fitness từ 0.1452 đến 0.1531.
  - `4.3.3. Danh sách 16 đặc trưng BPSO lựa chọn:` Phân tích xu hướng ưu tiên các biến tương tác hành vi và thiết bị.
  - `4.3.4. Năng lực đào thải 7 biến nhiễu nhân tạo tại seed=42.`
- **4.4. So sánh 5 Cấu hình Thực nghiệm Nâng cao (E1 – E5):**
  - `4.4.1. Cấu hình E1 (Full 64 continuous features).`
  - `4.4.2. Cấu hình E2 (ANOVA Top 16 features):` Lọc biến nhanh (0.03s), đạt PR-AUC cao nhất (0.3075).
  - `4.4.3. Cấu hình E3 (BPSO Top 16 features):` Giảm 75% chiều, tốc độ huấn luyện nhanh nhất (0.47s, tăng tốc 1.68 lần).
  - `4.4.4. Cấu hình E4 (BPSO + Optuna hyperparameter tuning):` Mô hình chốt kiểm định.
  - `4.4.5. Cấu hình E5 (Ensemble Stacking Classifier).`
- **4.5. Đánh giá chi tiết Mô hình Chốt E4 trên tập Holdout Độc lập:**
  - `4.5.1. Phân tích ma trận nhầm lẫn (Confusion Matrix):` TN=3,641, FP=920, FN=194, TP=245.
  - `4.5.2. Các chỉ số đo đạc chính thức:` Accuracy (77.72%), Precision (21.03%), Recall (55.81%), F1-Score (0.3055), PR-AUC (0.2590), ROC-AUC (0.7659).
- **4.6. Thảo luận Khoa học Trung thực về ANOVA vs BPSO:**
  - `4.6.1. Bản chất toán học của sự chênh lệch PR-AUC:` ANOVA chọn biến tài chính mạnh; BPSO chọn biến tương tác hành vi phi tuyến.
  - `4.6.2. Giá trị thực tế của BPSO:` Giảm tải kích thước mô hình, tăng tốc độ suy luận, bảo đảm khả năng mở rộng.
  - `4.6.3. Khảo sát tính ổn định đa seed của BPSO (seeds 42, 43, 44):` Ghi nhận bản chất stochastic của metaheuristic.

#### 3. Bảng biểu, Số liệu và Công thức
- **Bảng 4.1:** Bảng kết quả so sánh 7 mô hình cơ sở trên 83 đặc trưng (PR-AUC, ROC-AUC, F1, Accuracy).
- **Bảng 4.2:** Bảng tiến trình hội tụ qua 12 vòng lặp của thuật toán BPSO (GBest Fitness, PR-AUC val, số lượng biến chọn).
- **Bảng 4.3:** Bảng danh sách 16 đặc trưng BPSO lựa chọn so sánh với 16 đặc trưng ANOVA lựa chọn.
- **Bảng 4.4:** Bảng so sánh toàn diện 5 cấu hình thực nghiệm nâng cao (E1 – E5) về PR-AUC, ROC-AUC, F1, Accuracy, Thời gian chọn biến và Thời gian huấn luyện.
- **Bảng 4.5:** Ma trận nhầm lẫn của mô hình E4 trên 5,000 khách hàng Holdout.
- **Bảng 4.6:** Bảng kết quả khảo sát BPSO trên 3 seed ngẫu nhiên (`seed = 42, 43, 44`).
- **Hình 4.1:** Đường cong hội tụ hàm thích nghi GBest Fitness của BPSO qua các thế hệ.
- **Hình 4.2:** Biểu đồ so sánh PR-AUC và thời gian huấn luyện giữa E1, E2, E3, E4, E5.
- **Hình 4.3:** Đường cong Precision-Recall Curve và ROC Curve trên tập Holdout của mô hình E4.

#### 4. Nguồn dữ liệu và Tài liệu tham khảo
- Nguồn: `baseline_metrics.csv`, `metrics_comparison_pit.csv`, `holdout_predictions_pit.csv`, `holdout_metadata_pit.json`, `pso_feature_mask_pit.json`, `scratch/deep_evidence_summary.json`.
- Tài liệu trích dẫn: AlShourbaji et al. (2023), Thaher et al. (2022), Li (2021), Saito & Rehmsmeier (2015), Chen & Guestrin (2016).

#### 5. Thảo luận & Giới hạn
- Nghiêm cấm tuyên bố BPSO vượt trội ANOVA về PR-AUC. Phải giải thích trung thực rằng ANOVA có PR-AUC cao hơn (+0.0485), trong khi BPSO có ưu thế về giảm chiều và thời gian huấn luyện.

---

### PHẦN 5. DASHBOARD VÀ WEBSITE TRÌNH BÀY KẾT QUẢ (Dự kiến: 15 – 20 trang)

#### 1. Mục tiêu và Nội dung cần trình bày
- Trình bày giải pháp trực quan hóa dữ liệu phục vụ quản trị kinh doanh thông qua Power BI Dashboard.
- Trình bày kiến trúc kỹ thuật và giao diện của trang web nghiên cứu khoa học.
- Đóng gói sản phẩm nghiên cứu thành công cụ hỗ trợ ra quyết định phân bổ ngân sách marketing TMĐT.

#### 2. Các tiểu mục chi tiết cần viết
- **5.1. Mục tiêu và yêu cầu thiết kế hệ thống trực quan hóa:**
  - `5.1.1. Yêu cầu nghiệp vụ quản trị TMĐT:` Nắm bắt doanh thu, tỷ lệ mua lại, phân khúc khách hàng giá trị cao.
  - `5.1.2. Yêu cầu công nghệ:` Trực quan hóa tương tác, độ trễ thấp, giao diện hiện đại.
- **5.2. Thiết kế và Triển khai Power BI Dashboard:**
  - `5.2.1. Nguồn dữ liệu xuất bản Power BI:` Tệp `dashboard_customer_summary.csv` (200,000 bản ghi khách hàng).
  - `5.2.2. Trang 1 — Tổng quan Thương mại Điện tử (Executive Overview):` Thẻ KPI (Doanh thu, Đơn hàng, Tỷ lệ mua lại 8.78%), biểu đồ phân bổ doanh thu theo vùng địa lý và nguồn truy cập.
  - `5.2.3. Trang 2 — Phân tích Hành vi Khách hàng (Customer Behavior Insights):` Phễu chuyển đổi duyệt web $\rightarrow$ giỏ hàng $\rightarrow$ mua hàng, ma trận phân khúc điểm trung thành (Loyalty Matrix).
  - `5.2.4. Trang 3 — So sánh Mô hình Machine Learning (Model Evaluation):` Biểu đồ radar so sánh 7 baseline, thanh so sánh PR-AUC E1–E5, trực quan ma trận nhầm lẫn 5,000 mẫu Holdout.
  - `5.2.5. Trang 4 — Hàm ý Kinh doanh & Phân bổ Ngân sách (Actionable Strategy):` Mô phỏng phân bổ ngân sách tiếp thị nhắm mục tiêu vào nhóm xác suất mua $> 0.21$.
- **5.3. Xây dựng Website Nghiên cứu Khoa học (Web Portal):**
  - `5.3.1. Kiến trúc kỹ thuật Frontend:` HTML5, Vanilla CSS hiện đại, JavaScript bất đồng bộ (Vanilla JS), không phụ thuộc framework cồng kềnh.
  - `5.3.2. Cấu trúc 5 tab chuyên đề trên Website:`
    - *Tab 1 (Overview):* Giới thiệu đề tài, nhóm thực hiện, các chỉ số tóm tắt.
    - *Tab 2 (Data & PIT):* Giới thiệu quy trình Point-in-Time, từ điển đặc trưng và kết quả kiểm định.
    - *Tab 3 (Models & PSO):* Bảng tương tác so sánh baseline, tiến trình hội tụ PSO, kết quả E1–E5.
    - *Tab 4 (Interactive Prediction Demo):* Form nhập tham số khách hàng để mô phỏng tính điểm xác suất mua hàng theo thời gian thực.
    - *Tab 5 (Audit & Reproducibility):* Bản kê mã hash SHA-256, báo cáo kiểm định và mã nguồn mở.
  - `5.3.3. Cơ chế đồng bộ dữ liệu động:` Đọc trực tiếp tệp `web/data/metrics.json`.
- **5.4. Đánh giá tính ứng dụng và khả năng triển khai thực tế:** Hỗ trợ phòng marketing tối ưu hóa ROI cho các chiến dịch quảng cáo.

#### 3. Bảng biểu, Số liệu và Công thức
- **Bảng 5.1:** Bảng đặc tả cấu trúc dữ liệu tệp `dashboard_customer_summary.csv` cho Power BI.
- **Bảng 5.2:** Bảng đối chiếu các chỉ số hiển thị trên Web Portal với artifact gốc `metrics_comparison_pit.csv`.
- **Hình 5.1 — 5.4:** Ảnh chụp màn hình 4 trang Power BI Dashboard (Trang 1 Tổng quan, Trang 2 Hành vi, Trang 3 Mô hình, Trang 4 Chiến lược kinh doanh).
- **Hình 5.5 — 5.8:** Ảnh chụp giao diện Website nghiên cứu (Trang chủ, Tab Models, Tab Demo dự đoán, Tab Audit).

#### 4. Nguồn dữ liệu và Tài liệu tham khảo
- Nguồn: `outputs/powerbi/dashboard_customer_summary.csv`, `web/index.html`, `web/data/metrics.json`.

#### 5. Thảo luận & Giới hạn
- Nêu rõ Dashboard và Web Portal đóng vai trò là tầng trình diễn kết quả nghiên cứu khoa học, chưa tích hợp hệ thống thanh toán hay cơ sở dữ liệu thời gian thực của sàn giao dịch.

---

### PHẦN 6. HẠN CHẾ, HƯỚNG PHÁT TRIỂN VÀ KẾT LUẬN (Dự kiến: 8 – 10 trang)

#### 1. Mục tiêu và Nội dung cần trình bày
- Đánh giá mức độ giải quyết 5 câu hỏi nghiên cứu (`RQ1` – `RQ5`) và 7 mục tiêu ban đầu.
- Trình bày trung thực và đầy đủ 3 giới hạn nghiên cứu khoa học.
- Đề xuất các hướng nghiên cứu mở rộng trong tương lai.
- Kết luận chung toàn bộ đồ án và chuẩn hóa danh mục 28 tài liệu tham khảo có DOI.

#### 2. Các tiểu mục chi tiết cần viết
- **6.1. Tổng kết giải quyết 5 Câu hỏi nghiên cứu (RQ1 – RQ5):**
  - Trả lời rành mạch từng câu hỏi dựa trên các bằng chứng số liệu cụ thể ở Phần 3 và Phần 4.
- **6.2. Đánh giá mức độ hoàn thành 7 Mục tiêu nghiên cứu:**
  - Lập bảng tổng kết đối chiếu từng mục tiêu đặt ra ở Mục 1.5 với kết quả đạt được.
- **6.3. Ba giới hạn nghiên cứu cốt lõi (Bắt buộc):**
  - `6.3.1. Giới hạn về bản chất dữ liệu (Synthetic Benchmark Data):` Dữ liệu sinh từ mô hình toán học tham số giả định, chưa được đối chứng với log thực tế của doanh nghiệp.
  - `6.3.2. Giới hạn về thuật toán (Trade-off ANOVA vs BPSO):` BPSO bị giới hạn tài nguyên tính toán (16 hạt, 12 vòng lặp) nên PR-AUC thấp hơn ANOVA, tính ngẫu nhiên stochastic trên đa seed.
  - `6.3.3. Giới hạn về hạ tầng triển khai:` Xử lý trên môi trường máy trạm đơn node qua DuckDB, chưa thử nghiệm trên cụm phân tán Spark nhiều máy.
- **6.4. Hướng phát triển trong tương lai:**
  - `6.4.1.` Nghiên cứu thuật toán Multi-Objective PSO (MOPSO) tìm kiếm đường biên Pareto giữa PR-AUC và số chiều.
  - `6.4.2.` Ứng dụng mô hình Deep Learning chuỗi thời gian (Temporal Fusion Transformer, LSTM) khi có dữ liệu clickstream liên tục.
  - `6.4.3.` Thử nghiệm triển khai pipeline trên nền tảng đám mây phân tán (Databricks / AWS EMR).
- **6.5. Kết luận chung toàn bộ đồ án.**
- **6.6. Danh mục 28 Tài liệu tham khảo học thuật chính thức (2021 – 2026 có DOI):**
  - Trình bày chuẩn mực 28 bài báo khoa học đã được thẩm định độc lập.

#### 3. Bảng biểu, Số liệu và Công thức
- **Bảng 6.1:** Bảng tổng kết mức độ hoàn thành 7 mục tiêu nghiên cứu và sản phẩm bàn giao tương ứng.
- **Danh mục 28 tài liệu tham khảo:** Đầy đủ tác giả, năm, tên bài, tạp chí, tập, số, trang và liên kết DOI giải quyết được.

#### 4. Nguồn dữ liệu và Tài liệu tham khảo
- Nguồn: Mục 11 của [WORD_REPORT_INPUT_SPECIFICATION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/WORD_REPORT_INPUT_SPECIFICATION.md).

#### 5. Thảo luận & Giới hạn
- Nhấn mạnh tính đóng góp của đề tài nằm ở **phương pháp luận nghiên cứu nghiêm cẩn, thiết kế chống rò rỉ dữ liệu chuẩn tắc và tính minh bạch học thuật tuyệt đối**.

---

## 3. LỘ TRÌNH VÀ TIẾN ĐỘ THỰC HIỆN TẠO FILE WORD

| Bước | Nội dung công việc | Đầu ra tệp tin | Thời gian dự kiến | Trạng thái |
| :---: | :--- | :---: | :---: | :---: |
| **B1** | Hoàn thiện thẩm định dữ liệu & chuẩn hóa 28 DOI | `docs/INDEPENDENT_DATA_VALIDATION_REPORT.md` | Đã hoàn thành | **DONE** |
| **B2** | Ra quyết định khóa hồ sơ dữ liệu & checklist | `docs/FINAL_DATA_VALIDATION_DECISION.md`, Checklist | Đã hoàn thành | **DONE** |
| **B3** | Thiết lập kế hoạch chi tiết triển khai Word 6 phần | `docs/WORD_REPORT_FINAL_PLAN.md` | Đã hoàn thành | **DONE** |
| **B4** | Soạn thảo Phần 1 (Giới thiệu) & Phần 2 (Phương pháp) | Word Sections 1 & 2 | Tiếp theo | **SẴN SÀNG** |
| **B5** | Soạn thảo Phần 3 (EDA) & Phần 4 (Machine Learning & PSO)| Word Sections 3 & 4 | Tiếp theo | **SẴN SÀNG** |
| **B6** | Soạn thảo Phần 5 (Dashboard & Web) & Phần 6 (Kết luận) | Word Sections 5 & 6 | Tiếp theo | **SẴN SÀNG** |
| **B7** | Ghép nối toàn văn, định dạng mục lục & xuất bản `.docx` | `BaoCao_TotNghiep_Global.docx` | Bước cuối | **CHỜ THỰC HIỆN** |
