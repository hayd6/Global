# Product Requirements Document (PRD)

## 1. Giới thiệu dự án

- **Tên dự án**: Global E-Commerce Customer Purchase Prediction
- **Tên đề tài nghiên cứu**: "Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử."
- **Bối cảnh**: Dự án nghiên cứu kết hợp Big Data Engineering và Machine Learning nhằm giải quyết bài toán dự đoán hành vi mua hàng của khách hàng trên nền tảng thương mại điện tử đa quốc gia.
- **Tập dữ liệu**: Gồm 8 tập dữ liệu gốc trong `dataset/` (`customers.csv`, `geo_data.csv`, `marketing_campaigns.csv`, `sessions.csv`, `transactions.csv`, `train.csv`, `test.csv`, `sample_submission.csv`) với hơn 2 triệu lượt truy cập và hàng trăm nghìn giao dịch.

---

## 2. Mục tiêu dự án

1. **Tích hợp & Khai phá dữ liệu đa bảng**: Sử dụng DuckDB để xử lý và tổng hợp dữ liệu lớn từ 8 bảng liên kết mà không làm tràn bộ nhớ, chuẩn hóa dữ liệu bẩn và bất đồng nhất.
2. **Kiểm toán chất lượng & Chống rò rỉ dữ liệu (Data Leakage)**: Thiết lập quy trình kiểm tra toàn diện về tính toàn vẹn dữ liệu, kiểm tra mối quan hệ giữa các trường giao dịch, `high_value_flag` và `target`, đảm bảo tính hợp lệ về mặt thời gian.
3. **Khai phá đặc trưng hành vi (Feature Engineering)**: Xây dựng bộ đặc trưng phong phú ở cấp độ khách hàng (tần suất, thời lượng, giỏ hàng, tỷ lệ thoát, tỷ lệ dùng mã giảm giá, giá trị giao dịch, đặc trưng nhân khẩu học & địa lý, tương tác chiến dịch).
4. **Đánh giá 7 mô hình cơ sở**: Xây dựng benchmark công bằng trên cùng tập dữ liệu phân tách stratified giữa 7 thuật toán ML cơ bản: Logistic Regression, Naive Bayes, Decision Tree, Random Forest, Gradient Boosting, K-Nearest Neighbors, Support Vector Machine.
5. **Tối ưu hóa lựa chọn đặc trưng bằng PSO (Particle Swarm Optimization)**: Triển khai thuật toán Binary PSO với hàm mục tiêu đa tiêu chí (cân bằng giữa PR-AUC / ROC-AUC và mức độ tinh giản số đặc trưng), so sánh với phương pháp chọn đặc trưng thống kê và tập đặc trưng đầy đủ.
6. **Mô hình XGBoost nâng cao**: So sánh hiệu năng vượt trội của XGBoost trên tập đặc trưng tối ưu PSO so với tập đặc trưng ban đầu.
7. **Xuất kết quả nghiên cứu & Trực quan hóa**: Cung cấp đầy đủ các bảng dữ liệu tổng hợp, báo cáo chỉ số và biểu đồ phục vụ nghiên cứu khoa học, Power BI Dashboard và website.

---

## 3. Phạm vi sản phẩm (Scope)

### Trong phạm vi (In-Scope):
- Pipeline kỹ thuật hoàn chỉnh: Kiểm toán -> Làm sạch & Tích hợp -> Xử lý rò rỉ -> Trích xuất đặc trưng & EDA -> Huấn luyện mô hình cơ sở -> Lựa chọn đặc trưng PSO -> Đào tạo XGBoost -> Xuất kết quả Power BI & Báo cáo.
- Chạy hoàn toàn trên máy tính cá nhân qua CPU với tài nguyên tối ưu nhờ DuckDB và scikit-learn/XGBoost.
- Trực quan hóa kết luận với tối thiểu 8 biểu đồ EDA và các biểu đồ hiệu năng mô hình (ROC, PR Curve, Confusion Matrix, PSO Convergence).
- Kiểm thử tự động bằng `pytest`.

### Ngoài phạm vi (Out-of-Scope):
- Triển khai server MongoDB hoặc các cơ sở dữ liệu cloud trả phí.
- Tự động suy diễn các nhãn thời gian tương lai chưa được kiểm chứng trong dataset.
- Sửa đổi hoặc ghi đè trực tiếp các file gốc trong `dataset/`.

---

## 4. Yêu cầu chức năng (Functional Requirements)

1. **FR-1: Data Audit & Validation**: Tự động kiểm tra tính khả dụng, schema, dung lượng, missing values, duplicate keys, referential integrity và phân phối target.
2. **FR-2: Data Cleaning & Integration**: Chuẩn hóa các trường dị biệt (`bounce_flag`, `discount_applied`, `pages_viewed`, định dạng tiền tệ `$XX.XX`), xử lý missing values có quy tắc, tổng hợp sessions và transactions về mức khách hàng bằng DuckDB.
3. **FR-3: Leakage Audit**: Kiểm tra và loại bỏ các trường định danh hoặc rò rỉ thông tin trước khi huấn luyện mô hình.
4. **FR-4: Feature Engineering & EDA**: Tạo ma trận đặc trưng khách hàng (`outputs/customer_features.csv` hoặc parquet), từ điển đặc trưng và tối thiểu 8 biểu đồ phân tích trực quan có ý nghĩa.
5. **FR-5: Baseline Modeling**: Huấn luyện 7 mô hình học máy cơ sở, đánh giá theo ROC-AUC, PR-AUC, F1, Precision, Recall và thời gian xử lý.
6. **FR-6: PSO Feature Selection**: Triển khai Binary PSO có cấu hình linh hoạt (hạt, vòng lặp, quán tính, gia tốc, hàm fitness cân bằng độ chính xác và độ thưa), xuất tiến trình hội tụ và danh sách đặc trưng được chọn.
7. **FR-7: XGBoost Experiments**: Huấn luyện XGBoost trên toàn bộ đặc trưng vs đặc trưng lọc thống kê vs đặc trưng PSO, phân tích tầm quan trọng của đặc trưng (Feature Importance).
8. **FR-8: Export for Analytics & Power BI**: Xuất đầy đủ các bảng chỉ số định dạng CSV vào thư mục `outputs/powerbi/`.

---

## 5. Tiêu chí nghiệm thu (Acceptance Criteria)

- Mọi module mã nguồn đều có thể thực thi độc lập hoặc thông qua `src/pipeline.py`.
- Dữ liệu gốc trong `dataset/` được bảo toàn nguyên vẹn 100%.
- Không có bất kỳ file dữ liệu giả mạo hay chỉ số bịa đặt nào; mọi kết quả đều được tính toán từ dữ liệu thực tế.
- Các bài kiểm thử unit/integration tests bằng `pytest` đạt trạng thái PASS.
- Báo cáo và tài liệu đầy đủ, phản ánh chính xác kết quả thực nghiệm.
