# PROGRESS TRACKER — TIẾN ĐỘ THỰC HIỆN DỰ ÁN

| Giai đoạn | Nội dung công việc | Trạng thái | Ghi chú & Đầu ra |
| :--- | :--- | :--- | :--- |
| **Khởi tạo** | Kiểm tra môi trường, 8 CSV, tạo PRD & docs nền tảng | **HOÀN THÀNH** | `PRD.md`, `AGENTS.md`, `README.md`, `requirements.txt`, `docs/*` |
| **Giai đoạn 1** | Kiểm toán dữ liệu (Data Audit) & Báo cáo chất lượng | **HOÀN THÀNH** | `inspect_data.py`, `outputs/data_quality_report.csv`, `outputs/referential_integrity_report.csv`, `outputs/target_distribution.csv` |
| **Giai đoạn 2** | Làm sạch & Tích hợp bảng lớn bằng DuckDB | **HOÀN THÀNH** | `clean_data.py`, `integrate_data.py`, `outputs/processed/clean_customer_features.parquet` (200k khách hàng duy nhất) |
| **Giai đoạn 3** | Kiểm tra Target & Chống rò rỉ dữ liệu (Leakage Audit) | **HOÀN THÀNH** | Kiểm toán `high_value_flag`, loại ID, bảo đảm mốc thời gian, tách Train 80/20 Stratified và Test 40k độc lập |
| **Giai đoạn 4** | Feature Engineering & EDA (9 biểu đồ chuyên sâu) | **HOÀN THÀNH** | `build_features.py`, `eda.py`, `outputs/feature_dictionary.csv`, `outputs/eda/*.png`, `outputs/eda_customer_summary.csv` |
| **Giai đoạn 5** | Thiết lập đánh giá (Stratified Train/Val Split) | **HOÀN THÀNH** | Cố định `random_state=42`, Scikit-Learn Pipeline Fit-on-Train only |
| **Giai đoạn 6** | Huấn luyện 7 mô hình cơ sở (Baselines) | **HOÀN THÀNH** | `baselines.py`, `outputs/metrics/baseline_metrics.csv` (GB, RF, LR, SGD, DT, NB, KNN) |
| **Giai đoạn 7** | Lựa chọn đặc trưng & Tối ưu hóa Binary PSO | **HOÀN THÀNH** | `pso_optimizer.py`, `feature_selection.py`, `pso_selected_features.csv`, `pso_convergence.csv`, `pso_convergence.png` |
| **Giai đoạn 8** | Huấn luyện XGBoost & Thí nghiệm đối chứng | **HOÀN THÀNH** | `train_xgboost.py`, `metrics_comparison.csv`, `roc_curve.png`, `precision_recall_curve.png`, `confusion_matrix.png`, `feature_importance.csv` |
| **Giai đoạn 9** | Xuất kết quả cho Power BI và Web | **HOÀN THÀNH** | `export_outputs.py`, thư mục `outputs/powerbi/` (6 bảng CSV chuẩn hóa) |
| **Giai đoạn 10** | Kiểm thử tự động pytest & Hoàn thiện tài liệu | **HOÀN THÀNH** | `tests/` (18 tests passed 100%), hoàn thiện toàn bộ báo cáo và hướng dẫn |
| **Audit Khắc phục 1** | Xác minh định nghĩa bài toán & kiểm toán cutoff | **HOÀN THÀNH** | Chứng minh thực nghiệm target độc lập với GD 30 ngày cuối; chuẩn hóa phạm vi Observational Snapshot Propensity Classification |
| **Audit Khắc phục 2** | Sửa quy trình thí nghiệm & Quản lý phân vùng tập trung | **HOÀN THÀNH** | Tạo `split_manager.py`, cô lập 32k Holdout, tiền xử lý Fit-on-Train only, chuẩn hóa split IDs |
| **Audit Khắc phục 3** | Kiểm tra PSO & Báo cáo trung thực Trade-off | **HOÀN THÀNH** | Tách riêng search time (11.79s) và fit time (4.52s); báo cáo khách quan: giảm 73% số chiều, tăng tốc fit, trade-off nhẹ PR-AUC |
| **Kế hoạch 6 phần — GĐ 1** | Kiểm chứng hiện trạng & Hiệu chỉnh kế hoạch (ARL Mức 1) | **ĐÃ PHÊ DUYỆT** | Phê duyệt theo docs/IMPLEMENTATION_PLAN.md v2.0 & docs/PHASE1_FINAL_REVIEW.md |
| **Kế hoạch 6 phần — GĐ 2** | Hoàn thiện nghiên cứu học thuật & Bằng chứng (ARL Mức 2-3) | **HOÀN THÀNH & ĐÃ KIỂM ĐỊNH (CHỜ DUYỆT)** | Kiểm toán 26 tài liệu 2021–2026 độc quyền 4 trạng thái (7 Khớp hoàn toàn, 9 Đã hiệu chỉnh, 10 Thay thế, 0 Chưa xác minh) trong `docs/LITERATURE_REVIEW.md`; Bằng chứng khớp nối khách hàng 1-1 trên Holdout 32k; Xuất bản artifact tái lập `outputs/holdout_predictions.csv` & `holdout_prediction_metadata.json`; Đối chiếu exact `scale_pos_weight` (102,011 / 25,989 = 3.92516...); 25/25 pytest passed (100%); Lập `docs/PHASE2_ACCEPTANCE_REPORT.md` v2.1; Dừng chờ duyệt trước Giai đoạn 3 |
| **Kế hoạch 6 phần — GĐ 3** | Xây dựng Website nghiên cứu React + Vite (ARL Mức 2-4) | *Chưa thực hiện (Chờ duyệt GĐ 2)* | Frontend web app 6 trang trong web/ độc lập với Power BI |
| **Kế hoạch 6 phần — GĐ 4** | Giải pháp Power BI Dashboard 4 trang (ARL Mức 2-3) | *Chưa thực hiện (Chờ duyệt GĐ 2)* | DATA_MODEL_SCHEMA.md, POWER_BI_DESIGN_GUIDE.md, hướng dẫn manual .pbix |
| **Kế hoạch 6 phần — GĐ 5** | Biên tập Báo cáo học thuật 6 phần hoàn chỉnh (ARL Mức 3) | *Chưa thực hiện (Chờ duyệt GĐ 2)* | 6 file docs/report/Phan_1.md đến Phan_6.md theo DanY6Phan.md |
| **Kế hoạch 6 phần — GĐ 6** | Nghiệm thu cuối & Báo cáo nghiệm thu (ARL Mức 4) | *Chưa thực hiện (Chờ duyệt GĐ 2)* | docs/FINAL_ACCEPTANCE_REPORT.md và kiểm thử tích hợp chéo |



