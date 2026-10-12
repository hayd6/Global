# PROGRESS TRACKER — TIẾN ĐỘ THỰC HIỆN DỰ ÁN

| Giai đoạn | Nội dung công việc | Trạng thái | Ghi chú & Đầu ra |
| :--- | :--- | :--- | :--- |
| **Khởi tạo** | Kiểm tra môi trường, 8 CSV, tạo PRD & docs nền tảng | **HOÀN THÀNH** | `PRD.md`, `AGENTS.md`, `README.md`, `requirements.txt`, `docs/*` |
| **Giai đoạn 1** | Kiểm toán dữ liệu (Data Audit) & Báo cáo chất lượng | **HOÀN THÀNH** | `inspect_data.py`, `outputs/data_quality_report.csv`, `outputs/referential_integrity_report.csv`, `outputs/target_distribution.csv` |
| **Giai đoạn 2** | Làm sạch & Tích hợp bảng lớn bằng DuckDB | **HOÀN THÀNH** | `clean_data.py`, `integrate_data.py`, `outputs/processed/clean_customer_features.parquet` (200k khách hàng duy nhất) |
| **Giai đoạn 3** | Kiểm tra Target & Chống rò rỉ dữ liệu (Leakage Audit) | **HOÀN THÀNH** | Kiểm toán `high_value_flag`, loại ID, bảo đảm mốc thời gian, tách Train 80/20 Stratified và Test 40k độc lập |
| **Giai đoạn 4** | Feature Engineering & EDA (9 biểu đồ chuyên sâu) | **HOÀN THÀNH** | `build_features.py`, `eda.py`, `outputs/feature_dictionary.csv`, `outputs/eda/*.png`, `outputs/eda_customer_summary.csv` |
| **Giai đoạn 5** | Thiết lập đánh giá (Stratified Train/Val Split) | **HOÀN THÀNH** | Cố định `random_state=42`, Scikit-Learn Pipeline Fit-on-Train only |
| **Giai đoạn 6** | Huấn luyện 7 mô hình cơ sở (Baselines) | **HOÀN THÀNH** | `baselines.py`, `outputs/metrics/baseline_metrics.csv` (GB, RF, LR, SVM, DT, NB, KNN) |
| **Giai đoạn 7** | Lựa chọn đặc trưng & Tối ưu hóa Binary PSO | **HOÀN THÀNH** | `pso_optimizer.py`, `feature_selection.py`, `pso_selected_features.csv`, `pso_convergence.csv`, `pso_convergence.png` |
| **Giai đoạn 8** | Huấn luyện XGBoost & Thí nghiệm đối chứng | **HOÀN THÀNH** | `train_xgboost.py`, `metrics_comparison.csv`, `roc_curve.png`, `precision_recall_curve.png`, `confusion_matrix.png`, `feature_importance.csv` |
| **Giai đoạn 9** | Xuất kết quả cho Power BI và Web | **HOÀN THÀNH** | `export_outputs.py`, thư mục `outputs/powerbi/` (6 bảng CSV chuẩn hóa) |
| **Giai đoạn 10** | Kiểm thử tự động pytest & Hoàn thiện tài liệu | **HOÀN THÀNH** | `tests/` (18 tests passed 100%), hoàn thiện toàn bộ báo cáo và hướng dẫn |
| **Audit Khắc phục 1** | Xác minh định nghĩa bài toán & kiểm toán cutoff | **HOÀN THÀNH** | Chứng minh thực nghiệm target độc lập với GD 30 ngày cuối; chuẩn hóa phạm vi Observational Snapshot Propensity Classification |
| **Audit Khắc phục 2** | Sửa quy trình thí nghiệm & Quản lý phân vùng tập trung | **HOÀN THÀNH** | Tạo `split_manager.py`, cô lập 32k Holdout, tiền xử lý Fit-on-Train only, chuẩn hóa split IDs |
| **Audit Khắc phục 3** | Kiểm tra PSO & Báo cáo trung thực Trade-off | **HOÀN THÀNH** | Tách riêng search time (11.79s) và fit time (4.52s); báo cáo khách quan: giảm 73% số chiều, tăng tốc fit, trade-off nhẹ PR-AUC |
