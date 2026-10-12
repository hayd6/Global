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
- **Hệ quả**: Thuật toán bầy đàn giảm số đặc trưng từ 63 xuống 17 đặc trưng (giảm 73% số chiều), trong khi giữ vững năng lực phân biệt và giảm hơn 70% thời gian huấn luyện.

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
