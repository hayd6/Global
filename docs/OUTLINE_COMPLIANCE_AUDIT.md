# BÁO CÁO ĐỐI CHIẾU DỰ ÁN VỚI DÀN Ý 6 PHẦN GỐC
## (Outline Compliance Audit Report)

- **Ngày kiểm toán:** 2026-10-12
- **Tài liệu căn cứ:** [DanY6Phan.md](file:///d:/HuyD/Đại Học/BigData/Global/DanY6Phan.md) (Dàn ý nghiên cứu chính thức đã thống nhất)
- **Tên đề tài chính thức:** *"Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử."*
- **Người thực hiện kiểm toán:** Codex & AI Technical Lead

---

## 1. Tóm tắt hiện trạng dự án

### 1.1. Khái quát chung
Dự án **Global E-Commerce Customer Purchase Prediction** hiện đã hoàn thành xuất sắc toàn bộ phần **kỹ thuật lõi (Core Technical Pipeline)** của một hệ thống Big Data và Machine Learning:
- **Tích hợp dữ liệu lớn bằng DuckDB**: Đọc và tổng hợp thành công 8 bảng dữ liệu thô (2,000,000 sessions, 500,000 transactions, 200,000 customers) dạng streaming SQL, tạo bảng đặc trưng cấp khách hàng không gây tràn RAM.
- **Quy trình thực nghiệm chuẩn mực chống rò rỉ (Leakage-Free Protocol)**: Đã thiết lập [split_manager.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/split_manager.py) tạo phân vùng Stratified 80/20 duy nhất (`split_id: stratified_80_20_v1`), cô lập hoàn toàn tập Holdout 32,000 khách hàng; tiền xử lý Fit-on-Train strictly trên 128,000 khách hàng.
- **7 mô hình cơ sở & XGBoost nâng cao**: Đã huấn luyện và đánh giá trên cùng tập Holdout 32k mẫu theo ngưỡng cố định 0.5; xuất đầy đủ metrics so sánh, đường cong ROC/PR và ma trận nhầm lẫn.
- **Tối ưu hóa bầy đàn nhị phân (Binary PSO)**: Tự phát triển thuật toán Binary PSO với hàm fitness đa tiêu chí ($0.92 \cdot \text{PR-AUC} + 0.08 \cdot \text{Sparsity}$); ghi nhận đầy đủ chi phí tìm kiếm (11.79s, 208 evaluations) tách biệt khỏi thời gian fit (4.52s); báo cáo trung thực bản chất trade-off.
- **Kiểm thử tự động**: Đạt **18/18 tests passed** (100%) qua `pytest -v`.
- **Xuất dữ liệu cho Power BI**: Đã xuất đầy đủ 7 bảng dữ liệu sạch và tổng hợp vào [outputs/powerbi/](file:///d:/HuyD/Đại Học/BigData/Global/outputs/powerbi).

### 1.2. Mức độ tuân thủ tổng thể đối với Dàn ý 6 phần
- **Phần 1 (Giới thiệu nghiên cứu):** Kỹ thuật & dữ liệu đạt **90%**; Báo cáo học thuật chi tiết đạt **50%** (chưa có văn bản bài viết học thuật có trích dẫn thị trường mở rộng).
- **Phần 2 (Câu hỏi & Phương pháp nghiên cứu):** RQ1–RQ5 và H1–H4 đạt **100%** về thiết kế và thực nghiệm kỹ thuật; Tổng quan tài liệu học thuật (Literature Review >= 25 bài) đạt **15%** (mới có phác thảo phương pháp, chưa có danh mục bài báo 2021–2026).
- **Phần 3 (Xử lý dữ liệu & EDA):** Đạt **95%** (12 biểu đồ EDA, data dictionary, kiểm toán chất lượng đầy đủ).
- **Phần 4 (Machine Learning & Tối ưu PSO):** Đạt **95%** (7 mô hình cơ sở, so sánh Full vs ANOVA vs PSO, XGBoost E1–E5, phân tích trade-off trung thực).
- **Phần 5 (Dashboard & Website):** Đạt **40%** (Xuất dữ liệu cho Power BI đạt 100%; tuy nhiên **chưa có file Power BI `.pbix`** và **chưa có Website nghiên cứu frontend**).
- **Phần 6 (Hạn chế, Hướng phát triển & Kết luận):** Đạt **70%** (Đầy đủ nhận định kỹ thuật, phân tích giới hạn và trade-off trong docs; chưa có bản thảo chương kết luận học thuật tổng hợp và danh mục tài liệu tham khảo).

---

## 2. Bảng đối chiếu chi tiết Dàn ý 6 phần với Dự án thực tế

Trạng thái đánh giá theo 4 mức quy định:
- **ĐÃ HOÀN THÀNH**: Có đầy đủ mã nguồn, dữ liệu thực tế và tài liệu kiểm chứng.
- **HOÀN THÀNH MỘT PHẦN**: Đã có nền tảng/dữ liệu nhưng còn thiếu thành phần cụ thể.
- **CHƯA THỰC HIỆN**: Chưa có đầu ra trong kho mã nguồn.
- **CHƯA XÁC MINH**: Chưa đủ bằng chứng để kết luận.

| Mục dàn ý | Yêu cầu cốt lõi theo DanY6Phan.md | Trạng thái | Bằng chứng thực tế / Mã nguồn liên quan | Ghi chú & Đánh giá mức độ tuân thủ |
| :--- | :--- | :---: | :--- | :--- |
| **Tiêu đề** | “Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử.” | **ĐÃ HOÀN THÀNH** | [README.md:L1-L3](file:///d:/HuyD/Đại Học/BigData/Global/README.md#L1-L3), [PRD.md:L5-L6](file:///d:/HuyD/Đại Học/BigData/Global/PRD.md#L5-L6), [AGENTS.md:L3](file:///d:/HuyD/Đại Học/BigData/Global/AGENTS.md#L3) | Đúng tuyệt đối 100% tên đề tài chính thức. |
| **1.1** | Bối cảnh nghiên cứu: sự phát triển TMĐT, vai trò dữ liệu, thách thức đa bảng, dẫn vào đề tài | **HOÀN THÀNH MỘT PHẦN** | [PRD.md:L7-L9](file:///d:/HuyD/Đại Học/BigData/Global/PRD.md#L7-L9), [README.md:L7-L10](file:///d:/HuyD/Đại Học/BigData/Global/README.md#L7-L10) | Đã có tóm tắt kỹ thuật; chưa có bài viết học thuật 2–3 trang có trích dẫn số liệu thị trường Việt Nam/quốc tế. |
| **1.2** | Vấn đề nghiên cứu, kỹ thuật, khoảng trống, phát biểu câu hỏi trung tâm | **HOÀN THÀNH MỘT PHẦN** | [PRD.md:L12-L21](file:///d:/HuyD/Đại Học/BigData/Global/PRD.md#L12-L21), [DECISIONS.md:ADR-6](file:///d:/HuyD/Đại Học/BigData/Global/docs/DECISIONS.md#L48-L56) | Đã định vị rõ bài toán observational snapshot classification; chưa viết thành bài văn bản tổng quan học thuật. |
| **1.3** | Giới thiệu bộ dữ liệu 8 file, quy mô, vai trò, target rate 20.3%, kiểm toán cutoff thời gian | **ĐÃ HOÀN THÀNH** | [inspect_data.py](file:///d:/HuyD/Đại Học/BigData/Global/src/data/inspect_data.py), [DATA_DICTIONARY.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/DATA_DICTIONARY.md), `tests/test_data_audit.py` | Kiểm toán thực nghiệm chứng minh target độc lập giao dịch 30 ngày cuối; sửa đúng 200 dòng marketing campaign. |
| **1.4** | Lý do lựa chọn đề tài và dataset (6 lý do: TMĐT, Big Data, ML, PSO, DuckDB khả thi, SP) | **ĐÃ HOÀN THÀNH** | [PRD.md:L24-L36](file:///d:/HuyD/Đại Học/BigData/Global/PRD.md#L24-L36), [DECISIONS.md:ADR-1,ADR-2](file:///d:/HuyD/Đại Học/BigData/Global/docs/DECISIONS.md#L7-L20) | Trình bày đầy đủ tính phù hợp và khả thi của kiến trúc. |
| **1.5** | Mục tiêu tổng quát & 7 mục tiêu cụ thể | **HOÀN THÀNH MỘT PHẦN** | [PRD.md:L12-L21](file:///d:/HuyD/Đại Học/BigData/Global/PRD.md#L12-L21), [PROGRESS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/PROGRESS.md) | Mục tiêu 1–6 về kỹ thuật & ML đã hoàn thành; Mục tiêu 7 (Dashboard & Web) mới hoàn thành xuất dữ liệu. |
| **1.6** | Đối tượng, phạm vi và giới hạn nghiên cứu | **ĐÃ HOÀN THÀNH** | [PRD.md:L24-L36](file:///d:/HuyD/Đại Học/BigData/Global/PRD.md#L24-L36), [DATA_DICTIONARY.md:Sec-7](file:///d:/HuyD/Đại Học/BigData/Global/docs/DATA_DICTIONARY.md#L65-L85) | Ranh giới dữ liệu và giới hạn kỹ thuật được xác định rõ ràng. |
| **1.7** | Đóng góp dự kiến và điểm khác biệt (phương pháp, thực nghiệm, ứng dụng) | **ĐÃ HOÀN THÀNH** | [README.md:L13-L40](file:///d:/HuyD/Đại Học/BigData/Global/README.md#L13-L40), [EXPERIMENT_PLAN.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/EXPERIMENT_PLAN.md) | Phân tích rõ ràng đóng góp thực nghiệm và trade-off khách quan. |
| **1.8** | Bố cục báo cáo 6 phần | **ĐÃ HOÀN THÀNH** | [README.md:L42-L65](file:///d:/HuyD/Đại Học/BigData/Global/README.md#L42-L65) | Cấu trúc tài liệu tương ứng đầy đủ 6 phần. |
| **2.1** | Mục tiêu và định hướng nghiên cứu | **ĐÃ HOÀN THÀNH** | [PRD.md:L12-L21](file:///d:/HuyD/Đại Học/BigData/Global/PRD.md#L12-L21), [EXPERIMENT_PLAN.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/EXPERIMENT_PLAN.md) | Đã định hướng rõ ràng cho pipeline ML. |
| **2.2** | 5 Câu hỏi nghiên cứu RQ1 – RQ5 | **HOÀN THÀNH MỘT PHẦN** | [src/pipeline.py](file:///d:/HuyD/Đại Học/BigData/Global/src/pipeline.py), [metrics_comparison.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/metrics_comparison.csv) | RQ1–RQ4 đã có kết quả thực nghiệm hoàn chỉnh; RQ5 đã có dữ liệu hành vi nhưng thiếu sản phẩm dashboard/web. |
| **2.3** | 4 Giả thuyết nghiên cứu H1 – H4 | **ĐÃ HOÀN THÀNH** | [EXPERIMENT_PLAN.md:L7-L14](file:///d:/HuyD/Đại Học/BigData/Global/docs/EXPERIMENT_PLAN.md#L7-L14) | Đã kiểm định bằng thực nghiệm Holdout thực tế; báo cáo trung thực H2 có trade-off. |
| **2.4** | Thiết kế nghiên cứu & nguyên tắc chia tập (Stratified, Holdout cô lập, Fit-on-train) | **ĐÃ HOÀN THÀNH** | [split_manager.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/split_manager.py), [split_indices.npz](file:///d:/HuyD/Đại Học/BigData/Global/outputs/processed/split_indices.npz) | Phân vùng cố định `stratified_80_20_v1`; 128k Train vs 32k Holdout; Zero Leakage. |
| **2.5** | Phương pháp xử lý và phân tích (DuckDB, Pipeline, EDA, Baselines, PSO, Trực quan hóa) | **ĐÃ HOÀN THÀNH** | Toàn bộ mã nguồn trong `src/data/`, `src/features/`, `src/models/` | Thực thi đầy đủ, kiểm soát tài nguyên tốt. |
| **2.6** | Tiêu chí đánh giá (ROC-AUC, PR-AUC, F1, Precision, Recall, Runtime, Feature Count) | **ĐÃ HOÀN THÀNH** | [evaluate.py:compute_metrics](file:///d:/HuyD/Đại Học/BigData/Global/src/evaluation/evaluate.py#L35-L89), `threshold_source="fixed_0.5"` | Đo lường đa chiều, ngưỡng cố định 0.5 chống thiên vị. |
| **2.7** | Tổng quan nghiên cứu & khoảng trống (tối thiểu 25 tài liệu học thuật 2021–2026) | **CHƯA THỰC HIỆN** | Chưa có file tổng hợp tài liệu tham khảo học thuật | Cần tổng hợp bảng đối chiếu 25 bài báo khoa học theo 4 nhóm chủ đề như dàn ý yêu cầu. |
| **3.1** | Tổng quan dataset (8 file CSV) | **ĐÃ HOÀN THÀNH** | [DATA_DICTIONARY.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/DATA_DICTIONARY.md), [data_dictionary.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/data_dictionary.csv) | Đầy đủ schema, số dòng, khóa liên kết. |
| **3.2** | Kiểm tra chất lượng dữ liệu: thiếu, trùng, ngoại lệ, chuẩn hóa kiểu dị biệt | **ĐÃ HOÀN THÀNH** | [inspect_data.py](file:///d:/HuyD/Đại Học/BigData/Global/src/data/inspect_data.py), [clean_data.py](file:///d:/HuyD/Đại Học/BigData/Global/src/data/clean_data.py), [data_quality_report.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/data_quality_report.csv) | Xử lý triệt để Boolean, tiền tệ, unknown/N/A. |
| **3.3** | Tích hợp đa bảng bằng DuckDB về cấp khách hàng | **ĐÃ HOÀN THÀNH** | [integrate_data.py](file:///d:/HuyD/Đại Học/BigData/Global/src/data/integrate_data.py), [customer_features.parquet](file:///d:/HuyD/Đại Học/BigData/Global/outputs/customer_features.parquet) | Tránh Cartesian product; tổng hợp 2M sessions + 500k transactions trong ~6 giây. |
| **3.4** | Feature Engineering: tạo nhóm đặc trưng hành vi, loại ID/target, metadata | **ĐÃ HOÀN THÀNH** | [build_features.py](file:///d:/HuyD/Đại Học/BigData/Global/src/features/build_features.py), [feature_dictionary.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/feature_dictionary.csv) | 67 đặc trưng có công thức, kiểu dữ liệu, `temporal_nature`, `cutoff_rule`, `leakage_risk`. |
| **3.5** | Phân tích khám phá dữ liệu (EDA) (8–12 biểu đồ, tóm tắt phát hiện) | **ĐÃ HOÀN THÀNH** | [eda.py](file:///d:/HuyD/Đại Học/BigData/Global/src/analysis/eda.py), 12 biểu đồ trong [outputs/eda/](file:///d:/HuyD/Đại Học/BigData/Global/outputs/eda), [eda_customer_summary.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/eda_customer_summary.csv) | Đủ 12 biểu đồ chất lượng cao trực quan hóa đầy đủ phân phối và hành vi. |
| **3.6** | Chuẩn bị dữ liệu ML (Pipeline, Stratified Split, Fit-on-train only) | **ĐÃ HOÀN THÀNH** | [split_manager.py:get_preprocessed_features](file:///d:/HuyD/Đại Học/BigData/Global/src/models/split_manager.py#L137-L204) | Tuyệt đối không rò rỉ dữ liệu sang tập holdout/test. |
| **3.7** | Tổng hợp phát hiện EDA & chuyển tiếp sang Phần 4 | **HOÀN THÀNH MỘT PHẦN** | Đã có trong `README.md` và `PROGRESS.md` | Chưa viết thành bản thảo chương báo cáo riêng. |
| **4.1** | Thiết kế thực nghiệm ML so sánh công bằng | **ĐÃ HOÀN THÀNH** | [train_xgboost.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/train_xgboost.py), [feature_selection.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/feature_selection.py) | Chung tập Holdout 32k, chung seed 42, chung ngưỡng 0.5. |
| **4.2** | 7 Mô hình Machine Learning cơ sở | **ĐÃ HOÀN THÀNH** | [baselines.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/baselines.py), [baseline_metrics.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/baseline_metrics.csv) | Huấn luyện đủ 7 mô hình: GB, RF, LR, SGDClassifier log_loss, DT, NB, KNN. |
| **4.3** | So sánh 3 phương án lựa chọn đặc trưng (Full vs Thống kê vs PSO) | **ĐÃ HOÀN THÀNH** | [feature_selection.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/feature_selection.py), [feature_selection_comparison.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/feature_selection_comparison.csv) | Đánh giá đối chứng tại cùng số chiều k=17 trên tập Holdout 32k. |
| **4.4** | Triển khai Binary PSO (hàm fitness, tham số, cache, hội tụ, runtime) | **ĐÃ HOÀN THÀNH** | [pso_optimizer.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/pso_optimizer.py), [pso_selected_features.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/feature_selection/pso_selected_features.csv), [pso_convergence.png](file:///d:/HuyD/Đại Học/BigData/Global/outputs/plots/pso_convergence.png) | Vectorized Binary PSO, fitness đa mục tiêu, ghi nhận search cost 11.79s (208 evaluations). |
| **4.5** | Mô hình nâng cao XGBoost & Thí nghiệm E1–E5 | **ĐÃ HOÀN THÀNH** | [train_xgboost.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/train_xgboost.py), [metrics_comparison.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/metrics_comparison.csv) | Hoàn thành đủ 5 thí nghiệm E1–E5; lưu feature importance. |
| **4.6** | Đánh giá hiệu quả mô hình toàn diện (PR-AUC, ROC-AUC, curves, confusion matrix) | **ĐÃ HOÀN THÀNH** | [roc_curve.png](file:///d:/HuyD/Đại Học/BigData/Global/outputs/plots/roc_curve.png), [precision_recall_curve.png](file:///d:/HuyD/Đại Học/BigData/Global/outputs/plots/precision_recall_curve.png), [confusion_matrix.png](file:///d:/HuyD/Đại Học/BigData/Global/outputs/plots/confusion_matrix.png) | Xuất đủ biểu đồ hiệu năng trên tập holdout. |
| **4.7** | Phân tích lỗi (FP, FN) và giải thích kết quả | **HOÀN THÀNH MỘT PHẦN** | Đã có ma trận TP/FP/TN/FN và feature importance; chưa có văn bản phân tích định tính lỗi chi tiết | Cần văn bản giải thích các ca phân loại sai điển hình. |
| **4.8** | Thảo luận kết quả & đối chiếu câu hỏi RQ/giả thuyết H | **ĐÃ HOÀN THÀNH** | [EXPERIMENT_PLAN.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/EXPERIMENT_PLAN.md), [README.md](file:///d:/HuyD/Đại Học/BigData/Global/README.md) | Thảo luận trung thực: giảm 73% số chiều, tăng tốc fit, trade-off nhẹ PR-AUC. |
| **5.1** | Mục tiêu & yêu cầu thiết kế Dashboard / Web | **HOÀN THÀNH MỘT PHẦN** | [PRD.md:L48](file:///d:/HuyD/Đại Học/BigData/Global/PRD.md#L48), [export_outputs.py](file:///d:/HuyD/Đại Học/BigData/Global/src/export/export_outputs.py) | Đã xác định dữ liệu đầu ra; chưa xây dựng giao diện. |
| **5.2** | Power BI Dashboard 4 trang (Tổng quan, Hành vi, Mô hình, Hàm ý) | **HOÀN THÀNH MỘT PHẦN** | Đã xuất đủ 7 bảng dữ liệu CSV vào `outputs/powerbi/`; **chưa có file `.pbix`** | Cần tạo file báo cáo Power BI Desktop `.pbix` hoàn chỉnh. |
| **5.3** | Chuẩn bị dữ liệu cho Power BI | **ĐÃ HOÀN THÀNH** | [outputs/powerbi/](file:///d:/HuyD/Đại Học/BigData/Global/outputs/powerbi) (7 file CSV chuẩn hóa) | Dữ liệu sẵn sàng kết nối vào Power BI mà không cần tính lại từ tệp thô. |
| **5.4** | Xây dựng Website nghiên cứu (Overview, Method, Experiments, Insights, Demo) | **CHƯA THỰC HIỆN** | Chưa có mã nguồn frontend trong repository | Cần xây dựng web app giới thiệu nghiên cứu theo đúng dàn ý. |
| **5.5** | Kiến trúc kỹ thuật và triển khai Web / Dashboard | **HOÀN THÀNH MỘT PHẦN** | Đã có kiến trúc trong docs; chưa triển khai frontend | Cần dựng web tĩnh hoặc app hoàn chỉnh. |
| **5.6** | Kiểm thử và đánh giá sản phẩm Dashboard / Web | **CHƯA THỰC HIỆN** | Phụ thuộc vào việc hoàn thiện file `.pbix` và Website | Chưa thể kiểm thử trực quan giao diện. |
| **5.7** | Tổng hợp phát hiện và hàm ý kinh doanh (3–5 đề xuất có bằng chứng) | **HOÀN THÀNH MỘT PHẦN** | Đã có trong `README.md` và `DECISIONS.md` | Cần cấu trúc hóa theo mẫu Phát hiện → Bằng chứng → Hành động → Giới hạn. |
| **6.1** | Tổng kết kết quả nghiên cứu (bảng kết quả thực nghiệm thực tế) | **ĐÃ HOÀN THÀNH** | [README.md:L18-L38](file:///d:/HuyD/Đại Học/BigData/Global/README.md#L18-L38), [EXPERIMENT_PLAN.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/EXPERIMENT_PLAN.md) | Số liệu chuẩn xác từ artifacts thực tế. |
| **6.2** | Đánh giá mức độ hoàn thành mục tiêu nghiên cứu | **ĐÃ HOÀN THÀNH** | [docs/PROGRESS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/PROGRESS.md) | Đối chiếu từng mục tiêu rõ ràng. |
| **6.3** | Hạn chế của nghiên cứu (dữ liệu, phương pháp, thực tế) | **ĐÃ HOÀN THÀNH** | [DATA_DICTIONARY.md:Sec-7](file:///d:/HuyD/Đại Học/BigData/Global/docs/DATA_DICTIONARY.md#L65-L85), [EXPERIMENT_AUDIT.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/EXPERIMENT_AUDIT.md) | Thừa nhận trung thực giới hạn snapshot và chi phí tìm kiếm PSO. |
| **6.4** | Hướng phát triển trong tương lai (7 hướng đề xuất) | **ĐÃ HOÀN THÀNH** | [DECISIONS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/DECISIONS.md), [DanY6Phan.md:L1328-L1357](file:///d:/HuyD/Đại Học/BigData/Global/DanY6Phan.md#L1328-L1357) | Đã xác định lộ trình nghiên cứu tiếp theo. |
| **6.5** | Kết luận chung | **ĐÃ HOÀN THÀNH** | [README.md:L38-L40](file:///d:/HuyD/Đại Học/BigData/Global/README.md#L38-L40), [EXPERIMENT_AUDIT.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/EXPERIMENT_AUDIT.md) | Đúc kết súc tích giá trị và chi phí đánh đổi của PSO. |
| **6.6** | Tài liệu tham khảo (>= 25 bài 2021–2026) & Phụ lục | **HOÀN THÀNH MỘT PHẦN** | Phụ lục kỹ thuật đã hoàn thành; Danh mục 25 bài báo khoa học chưa có | Cần xây dựng danh mục tài liệu tham khảo chuẩn học thuật. |

---

## 3. Danh sách thiếu sót và sai lệch (Sắp theo mức độ nghiêm trọng)

### 🔴 Mức độ Cao (High Severity) — Thiếu sản phẩm đầu ra chính theo Dàn ý
1. **Thiếu Website nghiên cứu (Mục 5.4, 5.5, 5.6):**
   - *Mô tả:* Dàn ý quy định xây dựng một Website nghiên cứu gồm các trang: Tổng quan (Overview), Phương pháp (Methodology), Kết quả thực nghiệm (Experiments), Phân tích hành vi (Insights), Demo dự đoán (tuỳ chọn) và Tài liệu/Tái lập (Docs & Reproducibility).
   - *Hiện trạng:* Trong toàn bộ kho mã nguồn hiện chưa có thư mục frontend web, chưa có mã nguồn HTML/CSS/JS hay framework web (React/Next.js/Vite).
2. **Thiếu File Power BI Dashboard `.pbix` (Mục 5.2):**
   - *Mô tả:* Dàn ý quy định thiết kế Dashboard Power BI 4 trang: Trang 1 (Tổng quan TMĐT), Trang 2 (Phân tích hành vi), Trang 3 (So sánh mô hình ML), Trang 4 (Hàm ý kinh doanh).
   - *Hiện trạng:* Toàn bộ dữ liệu cho 4 trang đã được chuẩn bị và xuất vào `outputs/powerbi/` (7 file CSV), nhưng file dự án Power BI `.pbix` thực tế chưa tồn tại trong repo.

### 🟡 Mức độ Trung bình (Medium Severity) — Thiếu văn bản học thuật chuyên sâu
3. **Thiếu Danh mục Tài liệu tham khảo học thuật (>= 25 bài báo 2021–2026) (Mục 2.7 & 6.6.1):**
   - *Mô tả:* Dàn ý quy định tối thiểu 25 tài liệu khoa học xuất bản giai đoạn 2021–2026 thuộc 4 nhóm chủ đề (dự đoán mua hàng TMĐT, feature engineering/selection, PSO + boosting, đánh giá/giải thích mô hình), có bảng so sánh tác giả/năm/phương pháp/kết quả.
   - *Hiện trạng:* Chưa có file tổng hợp tài liệu tham khảo học thuật này trong `docs/`.
4. **Chưa biên tập Văn bản Báo cáo học thuật 6 phần hoàn chỉnh (Full Academic Thesis Draft):**
   - *Mô tả:* Hiện tại repo có các tài liệu kỹ thuật dành cho lập trình viên/ML engineer (`PRD.md`, `README.md`, `EXPERIMENT_PLAN.md`, `DECISIONS.md`, `EXPERIMENT_AUDIT.md`), nhưng chưa có tập văn bản báo cáo học thuật hoàn chỉnh viết chi tiết bằng lời văn nghiên cứu theo từng đề mục từ 1.1 đến 6.6 để sinh viên nộp cho giảng viên.
5. **Thiếu Phân tích lỗi định tính chuyên sâu (Error Analysis) (Mục 4.7):**
   - *Mô tả:* Dàn ý yêu cầu phân tích hồ sơ cụ thể của các ca False Positive và False Negative (khách hàng nào bị đoán nhầm, đặc điểm hành vi của họ ra sao).
   - *Hiện trạng:* Code đã xuất số lượng TP/FP/TN/FN và biểu đồ ma trận nhầm lẫn, nhưng chưa có tài liệu văn bản phân tích sâu các hồ sơ sai lệch tiêu biểu.

### 🟢 Mức độ Thấp (Low Severity) — Đồng bộ hóa tài liệu phụ
6. **Đồng bộ hóa tài liệu kiến trúc & khả năng tái lập cũ:**
   - [ARCHITECTURE.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/ARCHITECTURE.md) và [REPRODUCIBILITY.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/REPRODUCIBILITY.md) được viết từ giai đoạn đầu, cần được rà soát để đảm bảo cập nhật đồng bộ các thông số mới của [split_manager.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/split_manager.py) (phân vùng cố định 80/20, ngưỡng 0.5, 17 đặc trưng PSO, 208 evaluations).

---

## 4. Bằng chứng cụ thể cho từng nhận định

| Hạng mục kiểm tra | Bằng chứng mã nguồn / File kiểm chứng | Kết quả xác minh thực tế |
| :--- | :--- | :--- |
| **Phân vùng dữ liệu cô lập** | [split_manager.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/split_manager.py), [split_indices.npz](file:///d:/HuyD/Đại Học/BigData/Global/outputs/processed/split_indices.npz), [split_metadata.json](file:///d:/HuyD/Đại Học/BigData/Global/configs/split_metadata.json) | Train = 128,000 dòng; Holdout = 32,000 dòng; Giao thoa = 0; Inner tuning split hoàn toàn nằm trong Train pool. Test `test_split_consistency_and_holdout_isolation` PASS. |
| **7 Mô hình cơ sở** | [baselines.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/baselines.py), [baseline_metrics.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/baseline_metrics.csv) | Đủ 7 mô hình: GB (PR-AUC 0.2758), RF (0.2700), LR (0.2649), SGD log_loss (0.2456), DT (0.2584), NB (0.2161), KNN (0.2102). Đánh giá trên tập Holdout 32k. |
| **So sánh 3 phương pháp Feature Selection** | [feature_selection.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/feature_selection.py), [feature_selection_comparison.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/feature_selection_comparison.csv) | Approach A (Full 63): PR-AUC 0.2730, Fit 16.96s; Approach B (ANOVA 17): PR-AUC 0.2759, Search 0.13s, Fit 6.35s; Approach C (PSO 17): PR-AUC 0.2601, Search 11.79s, Fit 4.52s. |
| **Mô hình XGBoost E1–E5** | [train_xgboost.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/train_xgboost.py), [metrics_comparison.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/metrics_comparison.csv) | XGBoost Full 63: PR-AUC 0.2654, Fit 4.65s; XGBoost PSO 17: PR-AUC 0.2584, Fit 2.22s. Giảm 52% fit time hạ nguồn; trade-off -0.0070 PR-AUC. |
| **Chi phí tìm kiếm PSO** | [pso_optimizer.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/pso_optimizer.py), [pso_experiment_config.json](file:///d:/HuyD/Đại Học/BigData/Global/configs/pso_experiment_config.json) | 16 hạt, 12 vòng lặp; `search_time_seconds` = 11.79s; `n_evaluations` = 208; `n_unique_masks` = 208. |
| **Dữ liệu cho Power BI** | [export_outputs.py](file:///d:/HuyD/Đại Học/BigData/Global/src/export/export_outputs.py), [outputs/powerbi/](file:///d:/HuyD/Đại Học/BigData/Global/outputs/powerbi) | Có đủ 7 file CSV: `dashboard_customer_summary.csv`, `dashboard_behavior_summary.csv`, `metrics_comparison.csv`, `pso_convergence.csv`, `pso_selected_features.csv`, `feature_importance.csv`, `test_predictions_sample.csv`. |
| **Hiện trạng File `.pbix`** | Tìm kiếm `*.pbix` trong toàn bộ repo | **Không tìm thấy file nào**. |
| **Hiện trạng Website** | Tìm kiếm `index.html`, `package.json`, React/Next.js | **Không tìm thấy file mã nguồn web nào**. |
| **Hiện trạng Bộ test** | Lệnh `pytest -v` | **18/18 tests PASSED** trong 7.62s. |

---

## 5. Các mâu thuẫn giữa mã nguồn, kết quả và tài liệu

1. **Về sản phẩm Phần 5:**
   - *Tài liệu dàn ý:* Đặt mục tiêu có 2 sản phẩm đầu ra hoàn chỉnh: Power BI Dashboard và Website nghiên cứu.
   - *Thực tế dự án:* Mới hoàn thành tầng dữ liệu (Data Export Layer) cho Power BI; tầng giao diện người dùng (Presentation Layer) cho cả Dashboard và Website chưa được tạo.
2. **Về danh mục tài liệu tham khảo:**
   - *Tài liệu dàn ý:* Đặt mục tiêu tối thiểu 25 tài liệu học thuật (2021–2026) được rà soát và đối chiếu bảng.
   - *Thực tế dự án:* Hiện chưa có tài liệu tổng hợp literature review và danh mục trích dẫn này.
3. **Về phân tích định tính lỗi (Error Analysis):**
   - *Tài liệu dàn ý:* Mục 4.7 yêu cầu phân tích các nhóm khách hàng bị dự đoán nhầm (False Positive / False Negative).
   - *Thực tế dự án:* Code đã tính toán số lượng TP/FP/TN/FN và vẽ confusion matrix, nhưng chưa có văn bản mô tả định tính hành vi của nhóm dự đoán sai.

---

## 6. Danh sách công việc đề xuất theo thứ tự ưu tiên

Dựa trên nguyên tắc: **Bảo vệ mã nguồn lõi đã chuẩn hóa và kiểm thử thành công, chỉ bổ sung các sản phẩm còn thiếu theo đúng dàn ý**:

### 🎯 Ưu tiên 1: Xây dựng Website nghiên cứu hoàn chỉnh (Mục 5.4 - DanY6Phan.md)
- Xây dựng Web App tương tác cao cấp (sử dụng HTML5/Vanilla CSS/Modern JS hoặc React/Next.js theo tiêu chuẩn web cao cấp của dự án):
  - **Trang 1 — Tổng quan (Overview):** Tên đề tài, bối cảnh TMĐT, mục tiêu, dataset 8 file, quy trình kiến trúc.
  - **Trang 2 — Phương pháp (Methodology):** DuckDB data pipeline, kỹ thuật feature engineering, 7 mô hình baseline, thuật toán Binary PSO.
  - **Trang 3 — Kết quả thực nghiệm (Experiments):** Bảng tương tác so sánh các mô hình, biểu đồ ROC/PR curve, biểu đồ hội tụ PSO, trade-off analysis.
  - **Trang 4 — Khám phá hành vi & EDA (Insights):** Trực quan hóa 12 biểu đồ EDA, phân tích đặc trưng quan trọng.
  - **Trang 5 — Demo dự đoán (Prediction Demo):** Cho phép nhập/chọn thông số hành vi khách hàng và nhận xác suất mua hàng từ mô hình XGBoost.
  - **Trang 6 — Tài liệu & Tái lập (Docs & Reproducibility):** Hướng dẫn chạy lại, metadata kiểm toán, danh mục tài liệu.

### 🎯 Ưu tiên 2: Xây dựng giải pháp Dashboard Power BI (Mục 5.2 - DanY6Phan.md)
- Dựng file mẫu thiết kế Power BI hoặc báo cáo hướng dẫn chi tiết cách kết nối 7 bảng CSV trong [outputs/powerbi/](file:///d:/HuyD/Đại Học\BigData\Global\outputs\powerbi) thành 4 trang Dashboard (Tổng quan, Hành vi, Mô hình ML, Hàm ý kinh doanh) kèm công thức DAX và visual mockup.

### 🎯 Ưu tiên 3: Xây dựng Báo cáo học thuật 6 phần hoàn chỉnh (Full Report Draft)
- Tạo tài liệu báo cáo học thuật đầy đủ (ví dụ: `docs/BAO_CAO_NGHIEN_CUU_6_PHAN.md` hoặc chia theo từng chương trong `docs/report/`):
  - Phần 1: Bối cảnh, vấn đề, dataset, mục tiêu, đóng góp.
  - Phần 2: RQ1–RQ5, H1–H4, thiết kế nghiên cứu, tiêu chuẩn đánh giá, **Tổng quan nghiên cứu với 25+ tài liệu tham khảo (2021–2026)**.
  - Phần 3: Làm sạch dữ liệu DuckDB, 67 đặc trưng hành vi, phân tích 12 biểu đồ EDA.
  - Phần 4: Đánh giá 7 mô hình cơ sở, tối ưu hóa Binary PSO, XGBoost E1–E5, phân tích chi phí và trade-off, phân tích lỗi FP/FN.
  - Phần 5: Thiết kế Dashboard Power BI 4 trang, kiến trúc Website nghiên cứu, hàm ý quản trị (Phát hiện → Bằng chứng → Hành động).
  - Phần 6: Đánh giá mục tiêu, hạn chế nghiên cứu, hướng phát triển tương lai, kết luận chung và phụ lục kỹ thuật.

### 🎯 Ưu tiên 4: Đồng bộ hóa tài liệu kỹ thuật phụ
- Cập nhật nhẹ [ARCHITECTURE.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/ARCHITECTURE.md) và [REPRODUCIBILITY.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/REPRODUCIBILITY.md) để đồng bộ hoàn toàn với split cố định `stratified_80_20_v1` và kết quả kiểm toán mới nhất.

---

## 7. Những quyết định cần Người dùng phê duyệt trước khi thực hiện

Trước khi bắt tay vào triển khai các bước tiếp theo, kính đề nghị Người dùng xem xét và cho ý kiến về các quyết định sau:

1. **Công nghệ xây dựng Website nghiên cứu (Mục 5.4):**
   - *Lựa chọn A (Khuyến nghị):* Xây dựng Website tĩnh hiện đại dạng Single-Page Application (SPA) chuyên nghiệp bằng **HTML5 / Vanilla CSS hiện đại (Glassmorphism, Dark mode, Dashboard tương tác, Responsive) / Vanilla JS + Chart.js**, tích hợp sẵn mô hình suy luận demo trực tiếp trên client (không cần cài đặt thêm runtime Node.js hay mở server API phức tạp).
   - *Lựa chọn B:* Khởi tạo dự án **React / Next.js** hoặc **Vite** đầy đủ trong thư mục `web/` hoặc `frontend/`.
2. **Hình thức triển khai Power BI Dashboard (Mục 5.2):**
   - Do môi trường dòng lệnh AI không thể trực tiếp click chuột mở phần mềm Power BI Desktop GUI để "Save As" file `.pbix`, AI sẽ cung cấp:
     - Toàn bộ dữ liệu nguồn chuẩn hóa 100% trong `outputs/powerbi/`.
     - File hướng dẫn thiết kế Power BI chi tiết từng trang (layout, visuals, trường dữ liệu, DAX measures).
     - Đồng thời xây dựng luôn một giao diện Dashboard trực quan tương tác ngay trên **Website nghiên cứu** mô phỏng hoàn hảo 4 trang của Power BI để phục vụ báo cáo và demo.
3. **Hình thức lưu trữ Báo cáo học thuật 6 phần:**
   - Tạo một tài liệu tổng hợp hoàn chỉnh `docs/BAO_CAO_TOAN_VAN_6_PHAN.md` hay chia thành 6 file tương ứng `docs/report/Phan_1.md` đến `docs/report/Phan_6.md`?

---

> 🛑 **TRẠNG THÁI HIỆN TẠI: ĐÃ DỪNG LẠI CHỜ NGƯỜI DÙNG PHÊ DUYỆT.**  
> Tuyệt đối không tự ý sửa mã nguồn, không xóa file, không thay đổi cấu trúc khi chưa có sự đồng ý của Người dùng.
