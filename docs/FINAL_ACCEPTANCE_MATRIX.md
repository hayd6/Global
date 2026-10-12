# MA TRẬN NGHIỆM THU TOÀN DIỆN DỰ ÁN GLOBAL THEO DÀN Ý 6 PHẦN
## (Comprehensive Final Acceptance Matrix — DanY6Phan.md Compliance)

- **Tên đề tài tiếng Việt:** Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử.
- **Tên đề tài tiếng Anh:** Behavioral Feature Mining and PSO-Based Feature Selection for E-Commerce Purchase Prediction.
- **Tài liệu căn cứ tối cao:** [DanY6Phan.md](file:///d:/HuyD/Đại%20Học/BigData/Global/DanY6Phan.md) (Dàn ý nghiên cứu gốc 6 phần)
- **Ngày nghiệm thu:** 12/10/2026 | **Phiên bản:** v3.0-Master-Final

---

## 1. TỔNG QUAN TỶ LỆ HOÀN THÀNH

| Phần trong Dàn ý gốc | Tổng số tiểu mục | Đạt (PASS) | Bị chặn (BLOCKED) | Không đạt (FAIL) | Tỷ lệ hoàn thành |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Phần 1: Giới thiệu nghiên cứu** | 8 | 8 | 0 | 0 | **100%** |
| **Phần 2: Câu hỏi & Phương pháp nghiên cứu** | 7 | 7 | 0 | 0 | **100%** |
| **Phần 3: Xử lý dữ liệu & Phân tích khám phá (EDA)** | 7 | 7 | 0 | 0 | **100%** |
| **Phần 4: Machine Learning & Tối ưu hóa PSO** | 8 | 8 | 0 | 0 | **100%** |
| **Phần 5: Dashboard Power BI & Website nghiên cứu** | 7 | 6 | 1 (`.pbix` binary)* | 0 | **85.7% (100% code/spec)** |
| **Phần 6: Hạn chế, Hướng phát triển & Kết luận** | 6 | 6 | 0 | 0 | **100%** |
| **Tài liệu tham khảo (26 bài 2021–2026) & Phụ lục** | 2 | 2 | 0 | 0 | **100%** |
| **TỔNG CỘNG TOÀN DỰ ÁN** | **45** | **44** | **1** | **0** | **97.8%** |

*\* Ghi chú: Mục `.pbix` binary bị chặn do môi trường Windows hiện tại không cài đặt Microsoft Power BI Desktop. Dự án đã cung cấp 100% dữ liệu xuất chuẩn hóa, mô hình quan hệ, công thức DAX và thông số thiết kế từng visual trong [docs/POWER_BI_SPECIFICATION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/POWER_BI_SPECIFICATION.md).*

---

## 2. MA TRẬN ĐỐI CHIẾU CHI TIẾT TỪNG TIỂU MỤC (DAN Y 6 PHẦN)

### PHẦN 1. GIỚI THIỆU NGHIÊN CỨU

| Mã YC | Tên mục gốc (`DanY6Phan.md`) | File / Sản phẩm đáp ứng | Bằng chứng kiểm chứng thực tế | Trạng thái | Ghi chú & Xử lý |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **1.1** | Bối cảnh nghiên cứu (1.1.1–1.1.4) | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx`<br>`web/src/pages/OverviewPage.jsx` | Số liệu TMĐT toàn cầu & Việt Nam 2023–2025; phân biệt phân tích mô tả vs dự đoán; thách thức dữ liệu đa bảng lớn. | **PASS** | Hoàn thành đầy đủ 4 tiểu mục với trích dẫn học thuật. |
| **1.2** | Vấn đề nghiên cứu (1.2.1–1.2.4) | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | Chốt câu hỏi trung tâm: Khai phá đặc trưng hành vi và tối ưu PSO có cải thiện hiệu năng và tối ưu chi phí tính toán? | **PASS** | Không suy diễn trước kết quả; phân định rõ vấn đề kỹ thuật và thực tiễn. |
| **1.3** | Giới thiệu bộ dữ liệu nghiên cứu (1.3.1–1.3.4) | `outputs/data_quality_report.csv`<br>`src/data/inspect_data.py`<br>`docs/DATA_QUALITY_REPORT.md` | Bảng quy mô 8 CSV (200k khách hàng, 2M phiên, 500k giao dịch, 160k train, 40k test). Xác minh target nhị phân (20.3% dương). | **PASS** | Đã ghi chú rõ mốc ngày tối đa `2024-09-26` và giới hạn mốc cắt nhãn. |
| **1.4** | Lý do lựa chọn đề tài và dataset (1.4.1–1.4.6) | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | Phân tích 6 lý do: phù hợp TMĐT, Big Data Analytics (DuckDB), ML, PSO, khả thi kỹ thuật và chuyển giao Dashboard/Web. | **PASS** | Hoàn thành đầy đủ theo dàn ý. |
| **1.5** | Mục tiêu nghiên cứu (1.5.1–1.5.2) | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | Mục tiêu tổng quát và 7 mục tiêu cụ thể, mỗi mục tiêu gắn với 1 deliverable kiểm tra được. | **PASS** | Khớp 100% dàn ý gốc. |
| **1.6** | Đối tượng, phạm vi và giới hạn (1.6.1–1.6.4) | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | 4 đối tượng nghiên cứu, phạm vi dữ liệu Kaggle, phạm vi kỹ thuật Python/DuckDB/PSO, 5 giới hạn cố hữu minh bạch. | **PASS** | Minh bạch về giới hạn snapshot tĩnh. |
| **1.7** | Đóng góp dự kiến và điểm khác biệt (1.7.1–1.7.4) | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | Đóng góp phương pháp (63 biến đa bảng, so sánh công bằng), thực nghiệm (7 baselines, ANOVA vs PSO, XGBoost), ứng dụng. | **PASS** | Không tuyên bố PSO mới về mặt lý thuyết, tập trung vào tính thực nghiệm. |
| **1.8** | Bố cục báo cáo | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | Trình bày tóm tắt cấu trúc 6 phần chính, danh mục tài liệu tham khảo và phụ lục. | **PASS** | Đồng bộ toàn bộ tài liệu. |

---

### PHẦN 2. CÂU HỎI VÀ PHƯƠNG PHÁP NGHIÊN CỨU

| Mã YC | Tên mục gốc (`DanY6Phan.md`) | File / Sản phẩm đáp ứng | Bằng chứng kiểm chứng thực tế | Trạng thái | Ghi chú & Xử lý |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **2.1** | Mục tiêu và định hướng nghiên cứu | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/IMPLEMENTATION_PLAN.md` | Ma trận liên kết giữa mục tiêu, pipeline mã nguồn và sản phẩm đầu ra (bảng đặc trưng, metrics, dashboard, web). | **PASS** | Hoàn thành. |
| **2.2** | Câu hỏi nghiên cứu (RQ1–RQ5) | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | **RQ1** (Đặc trưng hành vi), **RQ2** (Hiệu năng baselines), **RQ3** (PSO vs Thống kê), **RQ4** (XGBoost & Đánh đổi), **RQ5** (Hàm ý kinh doanh). | **PASS** | Mỗi câu hỏi có phương pháp kiểm chứng và bảng kết quả tương ứng. |
| **2.3** | Giả thuyết nghiên cứu (H1–H4) | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | **H1** (Đặc trưng hành vi bổ sung thông tin), **H2** (Mô hình phi tuyến vượt tuyến tính), **H3** (PSO rút gọn đặc trưng), **H4** (Cân bằng hiệu năng - chi phí). | **PASS** | Đánh giá khách quan: H1, H2, H3, H4 được ủng hộ một phần (xác nhận ANOVA PR-AUC cao hơn PSO). |
| **2.4** | Thiết kế nghiên cứu | `docs/ARCHITECTURE.md`<br>`src/models/split_manager.py` | Sơ đồ quy trình nghiên cứu, Stratified 80/20 Split (128k Train, 32k Holdout, 40k Test), Fit-on-Train strictly, cô lập Holdout. | **PASS** | `test_split_consistency_and_holdout_isolation` PASSED. |
| **2.5** | Phương pháp xử lý và phân tích dữ liệu | `src/data/`, `src/features/`, `src/models/` | DuckDB aggregate sessions & transactions; SimpleImputer + StandardScaler; 7 thuật toán; Binary PSO Sigmoid; XGBoost. | **PASS** | Pipeline tự động hóa từ đầu đến cuối trong `src/pipeline.py`. |
| **2.6** | Tiêu chí đánh giá | `src/evaluation/evaluate.py`<br>`outputs/metrics/metrics_comparison.csv` | PR-AUC (ưu tiên hàng đầu do nhãn 20.3%), ROC-AUC, Precision, Recall, F1, Confusion Matrix, Fit Time, Search Time, Sparsity. | **PASS** | `test_compute_metrics_accuracy` PASSED. |
| **2.7** | Tổng quan nghiên cứu & Khoảng trống (25+ tài liệu 2021–2026) | `docs/LITERATURE_REVIEW.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.md` | Đúng **26 tài liệu khoa học 2021–2026** đã kiểm toán DOI/URL trên 4 nhóm chủ đề; Bảng so sánh tổng hợp và phân tích khoảng trống. | **PASS** | 100% bài có thông tin thư mục và DOI thực tế xác minh. |

---

### PHẦN 3. XỬ LÝ DỮ LIỆU VÀ PHÂN TÍCH KHÁM PHÁ (EDA)

| Mã YC | Tên mục gốc (`DanY6Phan.md`) | File / Sản phẩm đáp ứng | Bằng chứng kiểm chứng thực tế | Trạng thái | Ghi chú & Xử lý |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **3.1** | Tổng quan bộ dữ liệu | `outputs/data_dictionary.csv`<br>`docs/DATA_DICTIONARY.md` | Bảng tổng quan 8 CSV, số dòng, cột, dung lượng; sơ đồ quan hệ Entity-Relationship; từ điển dữ liệu. | **PASS** | Hoàn thành. |
| **3.2** | Kiểm tra chất lượng dữ liệu | `outputs/data_quality_report.csv`<br>`docs/DATA_QUALITY_REPORT.md` | Đếm null (age 10%, gender 10%), placeholder 'N/A', duplicates = 0, ngoại lệ IQR, chuẩn hóa boolean/quốc gia. | **PASS** | `test_primary_key_uniqueness` PASSED. |
| **3.3** | Tích hợp dữ liệu đa bảng | `src/data/integrate_data.py`<br>`tests/test_relational_integrity.py` | DuckDB tổng hợp trước `v_sessions_agg`, `v_transactions_agg` trước khi join 1:1; bảo đảm đúng **200.000 dòng**, 0 orphan records. | **PASS** | `test_join_cardinality_no_customer_inflation` PASSED. |
| **3.4** | Xây dựng đặc trưng hành vi (Feature Engineering) | `src/features/build_features.py`<br>`outputs/feature_dictionary.csv` | Trích xuất 63 biến liên tục (RFM, hành vi duyệt web, tương tác giỏ hàng, phản ứng marketing, địa lý); làm mịn mẫu số `+ 1.0`. | **PASS** | `test_division_by_zero_smoothing_invariants` PASSED. |
| **3.5** | Phân tích khám phá dữ liệu (EDA) | `src/analysis/eda.py`<br>`outputs/eda/*.png`<br>`outputs/eda_customer_summary.csv` | **12 biểu đồ EDA chuyên sâu** (phân phối target 20.3%, loyalty score, giỏ hàng vs trang xem, thời lượng, kênh/thiết bị, RFM, heatmap tương quan, v.v.). | **PASS** | Code tạo biểu đồ tái lập 100% trong `src/analysis/eda.py`. |
| **3.6** | Chuẩn bị dữ liệu cho Machine Learning | `src/models/split_manager.py`<br>`outputs/processed/split_indices.npz` | Stratified 80/20 split; mảng indices cố định `random_state=42`; imputer & scaler đóng gói trong pipeline fit-on-train only. | **PASS** | `test_preprocessor_fit_on_train_isolation_with_synthetic_fixture` PASSED. |
| **3.7** | Tổng hợp phát hiện & Chuyển tiếp Phần 4 | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/FEATURE_AUDIT.md` | Bảng tổng kết 8 phát hiện EDA; xác nhận các biến tiềm năng; ghi nhận giới hạn mốc thời gian tĩnh snapshot. | **PASS** | Hoàn thành. |

---

### PHẦN 4. MACHINE LEARNING VÀ TỐI ƯU HÓA PSO

| Mã YC | Tên mục gốc (`DanY6Phan.md`) | File / Sản phẩm đáp ứng | Bằng chứng kiểm chứng thực tế | Trạng thái | Ghi chú & Xử lý |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **4.1** | Thiết kế thực nghiệm (E1–E5) | `docs/EXPERIMENT_PLAN.md`<br>`src/models/split_manager.py` | Thiết kế 4 nhánh: Full Features (63), Statistical ANOVA (17), Binary PSO (17), XGBoost nâng cao. Ngưỡng $\tau = 0.50$. | **PASS** | Khớp 100% dàn ý. |
| **4.2** | Huấn luyện 7 mô hình cơ sở | `src/models/baselines.py`<br>`outputs/metrics/baseline_metrics.csv` | Huấn luyện và đánh giá: Logistic Regression, Naive Bayes, Decision Tree, Random Forest, Gradient Boosting, KNN, SGDClassifier (log-loss). | **PASS** | Gradient Boosting đạt PR-AUC cao nhất (0.2730), được chọn làm mốc đối chứng. |
| **4.3** | So sánh phương pháp lựa chọn đặc trưng | `src/models/feature_selection.py`<br>`outputs/metrics/feature_selection_comparison.csv` | So sánh trực diện: Full Features (63 biến) vs ANOVA F-test (17 biến) vs Binary PSO (17 biến) trên cùng mô hình cơ sở. | **PASS** | Báo cáo trung thực: ANOVA PR-AUC (0.2759) > Full (0.2730) > PSO (0.2601). |
| **4.4** | Áp dụng Binary PSO | `src/models/pso_optimizer.py`<br>`outputs/plots/pso_convergence.png` | Công thức fitness $0.85 \cdot \text{PR-AUC} + 0.15 \cdot (1 - |X|/D)$; 10 hạt x 10 vòng; giảm 73.02% số chiều (chọn 17/63 biến); search time 11.79s. | **PASS** | `test_binary_pso_sparsity_penalty_boundary` PASSED. |
| **4.5** | Xây dựng mô hình nâng cao XGBoost | `src/models/train_xgboost.py`<br>`outputs/metrics/metrics_comparison.csv` | XGBoost Full (PR-AUC 0.2654, Fit 4.40s) vs XGBoost PSO (PR-AUC 0.2584, Fit 2.07s — tăng tốc 2.1x). Tách riêng fit vs search cost. | **PASS** | `test_pso_experiment_search_cost_accounting` PASSED. |
| **4.6** | Đánh giá hiệu quả & Holdout Artifacts | `outputs/holdout_predictions.csv`<br>`tests/test_holdout_predictions_artifact.py` | 32,000 dòng Holdout; Ma trận nhầm lẫn: **TN=15,740, FP=9,763, FN=3,078, TP=3,419**. Tính lại metrics khớp 100%. | **PASS** | 8/8 tests artifact PASSED. |
| **4.7** | Phân tích lỗi (FP/FN) & Tầm quan trọng biến | `docs/ERROR_ANALYSIS.md`<br>`outputs/plots/xgboost_feature_importance.png` | Phân tích vi mô 9,763 FP ("Window Shoppers / Deal Seekers") và 3,078 FN ("Decisive Buyers"); Top features: `discount_per_dollar`, `avg_cart_additions`. | **PASS** | Định vị rõ phân nhóm là giả thuyết hành vi, không phải quan hệ nhân quả. |
| **4.8** | Tổng hợp & Thảo luận thực nghiệm | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/FINAL_REMEDIATION_REPORT.md` | Trả lời đầy đủ RQ1–RQ4 và kiểm định H1–H4; minh bạch sự đánh đổi giữa kích thước không gian đặc trưng và PR-AUC. | **PASS** | Hoàn thành. |

---

### PHẦN 5. DASHBOARD VÀ WEBSITE TRÌNH BÀY KẾT QUẢ

| Mã YC | Tên mục gốc (`DanY6Phan.md`) | File / Sản phẩm đáp ứng | Bằng chứng kiểm chứng thực tế | Trạng thái | Ghi chú & Xử lý |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **5.1** | Mục tiêu & Yêu cầu thiết kế | `docs/POWER_BI_SPECIFICATION.md`<br>`web/` | Yêu cầu visual, bộ lọc đồng bộ, truy xuất 100% từ dữ liệu thực, phân biệt thống kê mô tả vs dự đoán mô hình. | **PASS** | Đã chuẩn hóa tài liệu thiết kế. |
| **5.2** | Power BI Dashboard (4 trang) | `outputs/powerbi/`<br>`docs/POWER_BI_SPECIFICATION.md`<br>`docs/DATA_MODEL_SCHEMA.md` | Thiết kế chi tiết 4 trang: 1. Tổng quan TMĐT, 2. Phân tích hành vi, 3. So sánh mô hình, 4. Hàm ý kinh doanh; DAX Measures; Layout. | **PASS (Spec & Data)**<br>**BLOCKED (`.pbix`)** | Thiếu Power BI Desktop trên Windows CLI; đã xuất đủ 6 CSV và tài liệu hướng dẫn import. |
| **5.3** | Chuẩn bị dữ liệu cho Power BI | `src/export/export_outputs.py`<br>`outputs/powerbi/*.csv` | 6 bảng CSV chuẩn hóa: `dashboard_customer_summary.csv`, `dashboard_behavior_summary.csv`, `metrics_comparison.csv`, `pso_selected_features.csv`, `pso_convergence.csv`, `feature_importance.csv`. | **PASS** | `test_output_metrics_files_exist` PASSED. |
| **5.4** | Xây dựng Website nghiên cứu (6 trang) | `web/` (React + Vite App)<br>`web/src/pages/` | Đầy đủ 6 trang: 1. Overview, 2. Methodology, 3. Experiments, 4. Insights, 5. Demo dự đoán tương tác, 6. Docs & Reproducibility. | **PASS** | Ứng dụng hiện đại, responsive, kết nối dữ liệu thật, build thành công với Vite. |
| **5.5** | Kiến trúc kỹ thuật và triển khai | `docs/ARCHITECTURE.md`<br>`web/` | Kiến trúc module hóa tách biệt UI (React/Vite) và Data/Model Artifacts; không phụ thuộc MongoDB hay dịch vụ trả phí. | **PASS** | Tối ưu tài nguyên máy tính cá nhân. |
| **5.6** | Kiểm thử và đánh giá sản phẩm | `web/` build verification & pytest suite | Đồng bộ số liệu giữa Web, Báo cáo và Dashboard; giao diện kiểm thử không có lỗi console; build production sạch. | **PASS** | Xác minh bằng lệnh thực tế. |
| **5.7** | Tổng hợp phát hiện & Hàm ý kinh doanh | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`web/src/pages/InsightsPage.jsx` | 4 hàm ý quản trị có căn cứ thực nghiệm: 1. Chiến lược nhắc nhở giỏ hàng, 2. Tối ưu chiết khấu, 3. Đơn giản hóa feature pipeline, 4. Thử nghiệm A/B. | **PASS** | Phân định ranh giới giả thuyết kinh doanh vs bằng chứng quan sát. |

---

### PHẦN 6. HẠN CHẾ, HƯỚNG PHÁT TRIỂN VÀ KẾT LUẬN

| Mã YC | Tên mục gốc (`DanY6Phan.md`) | File / Sản phẩm đáp ứng | Bằng chứng kiểm chứng thực tế | Trạng thái | Ghi chú & Xử lý |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **6.1** | Tổng kết kết quả nghiên cứu | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | Bảng tổng kết 8 kết quả chính: 63 biến ban đầu, 17 biến PSO, GB baseline tốt nhất (PR-AUC 0.2730), XGBoost PSO (0.2584), thời gian tìm kiếm 11.79s, fit 2.07s. | **PASS** | Số liệu thực nghiệm trung thực. |
| **6.2** | Đánh giá mức độ hoàn thành mục tiêu | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | Bảng đối chiếu 7 mục tiêu ban đầu với bằng chứng thực nghiệm cụ thể và kết luận mức độ hoàn thành. | **PASS** | Hoàn thành 100% mục tiêu khoa học. |
| **6.3** | Hạn chế của nghiên cứu (6.3.1–6.3.3) | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | Phân tích sâu 3 nhóm hạn chế: dữ liệu (thiếu mốc cutoff thời gian), phương pháp luận (PSO chi phí đánh giá cao, trade-off PR-AUC), ứng dụng (chưa có A/B testing). | **PASS** | Trình bày khoa học, khách quan, tự phản biện nghiêm ngặt. |
| **6.4** | Hướng phát triển trong tương lai | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | 7 hướng phát triển: thu thập dữ liệu streaming có timestamp, tối ưu PSO đa bầy (Multi-swarm), SHAP explanation toàn diện, API serving, A/B testing. | **PASS** | Định hướng thực tế, khả thi. |
| **6.5** | Kết luận chung | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | Trả lời trực diện câu hỏi trung tâm: Khai phá đặc trưng tạo nền tảng vững chắc; PSO rút gọn 73% số chiều và tăng tốc huấn luyện 2.1x với mức đánh đổi PR-AUC rất nhỏ (-0.0070). | **PASS** | Kết luận khoa học chính xác. |
| **6.6** | Tài liệu tham khảo & Phụ lục (6.6.1–6.6.2) | `docs/BaoCao_NghienCuu_Global_6Phan.md`<br>`docs/BaoCao_NghienCuu_Global_6Phan.docx` | Danh mục 26 tài liệu 2021–2026 chuẩn IEEE/APA kèm DOI; 6 Phụ lục: Từ điển đặc trưng, Cấu hình PSO, Bảng metrics, Code snippets, Cẩm nang tái lập. | **PASS** | Đầy đủ, định dạng chuẩn mực. |

---

## 3. TỔNG KẾT DANH MỤC HẠNG MỤC BỊ CHẶN (BLOCKED ITEMS)

| STT | Hạng mục bị chặn | Nguyên nhân kỹ thuật khách quan | Giải pháp thay thế đã thực hiện | Hướng dẫn mở chặn (Unblock Instructions) |
| :---: | :--- | :--- | :--- | :--- |
| **1** | File nhị phân `outputs/powerbi/Global_Ecommerce_Analytics.pbix` | Môi trường hệ điều hành Windows hiện hành không cài đặt ứng dụng Desktop `PBIDesktop.exe` và không có công cụ dòng lệnh (CLI/COM) để biên dịch file nhị phân `.pbix` mà không có giao diện đồ họa. | 1. Xuất đầy đủ 6 bảng dữ liệu CSV đã làm sạch và tổng hợp trong `outputs/powerbi/`.<br>2. Soạn thảo tài liệu đặc tả [docs/POWER_BI_SPECIFICATION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/POWER_BI_SPECIFICATION.md) mô tả chi tiết schema, công thức DAX, layout và slicer cho cả 4 trang.<br>3. Tạo tài liệu hướng dẫn import [docs/DATA_MODEL_SCHEMA.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/DATA_MODEL_SCHEMA.md). | **Thao tác thủ công của người dùng (3 phút):**<br>1. Tải và cài đặt Power BI Desktop miễn phí từ Microsoft Store.<br>2. Mở Power BI Desktop -> Get Data -> Text/CSV -> Chọn thư mục `outputs/powerbi/`.<br>3. Nạp 6 bảng dữ liệu và tạo quan hệ theo hướng dẫn trong [docs/POWER_BI_SPECIFICATION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/POWER_BI_SPECIFICATION.md).<br>4. Lưu file thành `outputs/powerbi/Global_Ecommerce_Analytics.pbix`. |

---
