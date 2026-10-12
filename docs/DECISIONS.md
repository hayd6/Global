# ARCHITECTURAL & TECHNICAL DECISIONS LOG (ADR)

Tài liệu này ghi lại các quyết định kỹ thuật trọng yếu được đưa ra trong quá trình phát triển dự án **Global E-Commerce Customer Purchase Prediction**.

---

## Quyết định 1: Sử dụng DuckDB cho tầng trích xuất và tổng hợp dữ liệu lớn
- **Ngày quyết định**: 2026-10-12
- **Bối cảnh**: `sessions.csv` có 2 triệu dòng, `transactions.csv` có 500,000 dòng. Việc đọc toàn bộ bằng Pandas thông thường có thể chiếm 4-8GB RAM và JOIN trực tiếp tạo ra tích Descartes (Cartesian product) phình to bảng dữ liệu.
- **Quyết định**: Sử dụng công cụ truy vấn SQL **DuckDB** để tính toán tổng hợp (GROUP BY theo `customer_id`) trực tiếp trên file CSV dạng columnar/vectorized streaming.
- **Hệ quả**: Giảm tiêu thụ RAM từ nhiều Gigabyte xuống dưới 300MB, tốc độ tính toán tích hợp toàn bộ 200,000 khách hàng hoàn thành chỉ trong **6 giây** mà không cần cài đặt máy chủ cơ sở dữ liệu bên ngoài.

---

## Quyết định 2: Tự triển khai Binary PSO (Custom Vectorized Binary PSO)
- **Ngày quyết định**: 2026-10-12
- **Bối cảnh**: Dự án đang chạy trên Python 3.14. Các thư viện PSO cũ như `pyswarms` hoặc `optunity` thường gặp vấn đề tương thích với NumPy 2.x / Python 3.14 và không hỗ trợ trực tiếp hàm fitness nhị phân tích hợp phạt độ thưa (sparsity regularization) cùng Scikit-Learn Pipeline.
- **Quyết định**: Tự xây dựng module `BinaryPSO` thuần túy bằng NumPy và Scikit-Learn trong `src/models/pso_optimizer.py`.
- **Hệ quả**: Mã nguồn gọn gàng, hoàn toàn tương thích Python 3.14, kiểm soát 100% logic hàm fitness, cơ chế sigmoid transfer function, lưu checkpointing và trực quan hóa tiến trình hội tụ chi tiết.

---

## Quyết định 3: Thiết kế hàm mục tiêu (Fitness) ưu tiên PR-AUC kết hợp phạt số chiều
- **Ngày quyết định**: 2026-10-12
- **Bối cảnh**: Tỷ lệ nhãn dương trong `train.csv` chỉ là 20.30% (mất cân bằng). Nếu dùng Accuracy hoặc ROC-AUC đơn thuần, mô hình có thể bị bias về lớp đa số (không mua hàng). Khi thử nghiệm với $\alpha=0.85$, phần thưởng độ thưa chiếm tỷ trọng khá lớn làm thuật toán có xu hướng cắt giảm cả các biến quan trọng; sau khi tinh chỉnh lên $\alpha=0.92$, thuật toán cân bằng hoàn hảo giữa PR-AUC và tính tinh gọn.
- **Quyết định**: Hàm fitness được định nghĩa như sau:
  $$\text{Fitness} = 0.92 \cdot \text{PR-AUC} + 0.08 \cdot \left(1 - \frac{\text{k\_selected}}{\text{total\_features}}\right)$$
- **Hệ quả**: Thuật toán bầy đàn giảm số đặc trưng từ 63 xuống 17 đặc trưng (giảm 73.02% số chiều), giúp giảm thời gian fit của mô hình hạ nguồn từ 16.96s xuống 4.52s (giảm 73% fit time cho baseline; từ 4.65s xuống 2.22s cho XGBoost). Chi phí tìm kiếm PSO là 11.79s (đầu tư offline 208 mặt nạ). Trên tập holdout 32k độc lập, hiệu năng phân biệt có sự đánh đổi nhẹ (-0.0129 PR-AUC trên baseline, -0.0070 PR-AUC trên XGBoost) để đổi lấy sự tối giản vượt trội về số chiều.

---

## Quyết định 4: Xử lý các trường dữ liệu dị biệt bằng chuẩn hóa xác định (Deterministic Cleaning)
- **Ngày quyết định**: 2026-10-12
- **Bối cảnh**: `bounce_flag` và `discount_applied` có chứa 6 giá trị khác nhau: `'Yes'`, `'No'`, `'1'`, `'0'`, `'TRUE'`, `'FALSE'`. `order_value`, `credit_limit` và `campaign_budget` chứa ký tự tiền tệ `$`, `,`. `age` chứa chuỗi `'unknown'`. `pages_viewed` chứa chuỗi `'N/A'`. Trong `transactions.csv` có 21 đơn hàng miễn phí giá trị `$0.00`.
- **Quyết định**: Chuẩn hóa rõ ràng bằng các biểu thức CASE WHEN SQL trong DuckDB và chuyển đổi tường minh sang BOOLEAN / FLOAT / INT. Giá trị `'unknown'` và `'N/A'` được chuyển thành NULL trước khi thực hiện quy trình Imputation trong Scikit-Learn Pipeline.
- **Hệ quả**: Dữ liệu sạch, đồng nhất, không gây lỗi kiểu dữ liệu khi đưa vào thuật toán ML.

---

## Quyết định 5: Chiến lược chống rò rỉ dữ liệu (Anti-Leakage Strategy)
- **Ngày quyết định**: 2026-10-12
- **Bối cảnh**: `train.csv` (160k dòng) và `test.csv` (40k dòng) cùng chia sẻ bảng `customers`, `sessions`, `transactions` có mốc thời gian tối đa đến 2024-09-26.
- **Quyết định**:
  1. `customer_id` tuyệt đối không được đưa vào vector đặc trưng đầu vào của mô hình.
  2. Toàn bộ các bộ tiền xử lý (Imputer, Scaler, Encoder) chỉ được `fit` trên 80% tập Train (128,000 dòng), sau đó `transform` trên 20% tập Validation (32,000 dòng) và tập Test (40,000 dòng).
  3. Tập `test.csv` chỉ dùng để tạo bảng dự đoán cuối cùng `outputs/test_predictions.csv`, không tham gia vào bất kỳ bước chọn đặc trưng hay tinh chỉnh mô hình nào.

---

## Quyết định 6: Quản lý phân vùng tập trung (Unified Split Manager) & Giới hạn phạm vi nghiên cứu
- **Ngày quyết định**: 2026-10-12
- **Bối cảnh**: Kiểm toán độc lập phát hiện các mô hình baseline, ANOVA và PSO từng sử dụng phương thức phân chia (split) và tiền xử lý không đồng nhất; nhãn `target` không có thông tin cutoff sinh nhãn trong dữ liệu nguồn.
- **Quyết định**:
  1. Xây dựng module `src/models/split_manager.py` tạo một phân vùng Stratified 80/20 duy nhất (`split_id: stratified_80_20_v1`), cố định chỉ số khách hàng vào `outputs/processed/split_indices.npz` và lưu metadata vào `configs/split_metadata.json`. Phân vùng inner tuning cho PSO được trích xuất hoàn toàn từ tập Train pool 128k mẫu, tuyệt đối không chạm vào 32k mẫu Holdout.
  2. Xác định phạm vi nghiên cứu chính thức là: **Bài toán phân loại xu hướng mua hàng (Purchase Propensity Classification) trên ảnh chụp quan sát đa bảng (Observational Snapshot)**, loại bỏ các giả định không có bằng chứng về chuỗi thời gian hay cửa sổ dự đoán tương lai 30 ngày.
- **Hệ quả**: Đảm bảo 100% tính công bằng, triệt tiêu rò rỉ dữ liệu, và kết luận nghiên cứu trung thực về mặt khoa học.
