# AGENTS.md — Quy tắc lập trình và Quy trình làm việc cho AI Agent

Tài liệu này quy định các nguyên tắc bắt buộc khi AI Agent làm việc trên kho mã nguồn **Global E-Commerce Customer Purchase Prediction**.

---

## 1. Nguyên tắc cốt lõi

1. **Bảo vệ dữ liệu gốc tuyệt đối**:
   - Thư mục `dataset/` là dữ liệu nguồn chỉ đọc (READ-ONLY).
   - Nghiêm cấm mọi hành vi sửa, ghi đè, xóa hoặc di chuyển các file trong `dataset/`.
   - Mọi dữ liệu trung gian và kết quả phải được lưu trong thư mục dẫn xuất (`outputs/` hoặc `data/processed/`).

2. **Trung thực về dữ liệu và thực nghiệm**:
   - Không bịa đặt chỉ số hiệu năng (AUC, F1, Accuracy...).
   - Không tạo dữ liệu giả thay thế cho dữ liệu thật.
   - Khi có trường dữ liệu chưa xác minh được nguồn gốc hoặc ý nghĩa, ghi rõ `"chưa xác minh"`.

3. **Chống rò rỉ dữ liệu (Anti-Leakage First)**:
   - Tuyệt đối không dùng `customer_id` hoặc nhãn `target` làm đặc trưng đầu vào.
   - Phân chia tập Train/Validation một cách nghiêm ngặt.
   - Giữ tập `test.csv` hoàn toàn độc lập, chỉ dùng để dự đoán cuối cùng nếu cần, không dùng trong chọn đặc trưng hoặc tối ưu tham số.
   - Bộ tiền xử lý (Imputer, Scaler, Encoder) chỉ được `fit` trên tập Train, sau đó `transform` trên Validation và Test.

4. **Hiệu quả tài nguyên (Resource-conscious)**:
   - Dự án chạy trên máy tính cá nhân (môi trường Windows, CPU thông thường).
   - Sử dụng **DuckDB** để truy vấn và tính toán tổng hợp trên bảng lớn (hàng triệu dòng) thay vì tải toàn bộ bảng thô vào RAM Pandas.
   - Không in toàn bộ bảng dữ liệu lớn ra terminal.
   - Các thuật toán tìm kiếm như PSO phải có cấu hình kiểm soát (số hạt, số vòng lặp) và checkpointing/logging để tránh chạy vô hạn.

5. **Tính tái lập (Reproducibility)**:
   - Cố định `random_state` / `seed` trong toàn bộ pipeline (chia tập, mô hình, PSO).
   - Lưu cấu hình thực nghiệm vào thư mục `configs/` hoặc file metadata tương ứng.

---

## 2. Quy chuẩn mã nguồn

- **Ngôn ngữ**: Python 3.10+ (đang chạy Python 3.14).
- **Cấu trúc module hóa**: Phân tách rõ ràng giữa cấu hình, xử lý dữ liệu, trích xuất đặc trưng, tối ưu mô hình, đánh giá và xuất kết quả.
- **Xử lý ngoại lệ & Logging**: Sử dụng module `logging` của Python thay vì `print` bừa bãi. Ghi log có mức độ (`INFO`, `WARNING`, `ERROR`).
- **Kiểm thử**: Viết bài kiểm thử tự động với `pytest` cho từng module xử lý dữ liệu, kiểm tra leakage, tính toán đặc trưng và huấn luyện.

---

## 3. Báo cáo định kỳ sau mỗi giai đoạn

Sau mỗi giai đoạn, AI Agent phải tổng kết:
- Danh sách công việc đã hoàn thành.
- Các file đã tạo hoặc cập nhật.
- Lệnh đã chạy trong terminal và kết quả kiểm tra.
- Các vấn đề / lỗi còn tồn tại (nếu có).
- Kế hoạch bước tiếp theo.
