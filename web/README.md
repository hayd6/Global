# RESEARCH PORTAL — BEHAVIORAL FEATURE MINING & PSO OPTIMIZATION

Cổng thông tin nghiên cứu tương tác trực quan 6 trang dành cho đề tài:
**"Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử"**

---

## 1. Cấu trúc 6 Trang Nghiên cứu (`DanY6Phan.md` Mục 5.4)

1. **Trang 1 — Tổng quan (Overview)**: Giới thiệu đề tài, bối cảnh thương mại điện tử, 4 KPI cốt lõi (200k khách hàng, 2M phiên, 500k giao dịch, 20.31% nhãn mua), câu hỏi trung tâm và sơ đồ luồng dữ liệu DuckDB pipeline.
2. **Trang 2 — Phương pháp (Methodology)**: Kiến trúc tiền tổng hợp DuckDB chống nhân bản khách hàng, công thức hàm mục tiêu Binary PSO $\alpha=0.85$, 3 tầng chống rò rỉ dữ liệu (Anti-Leakage), bảng phân loại 63 đặc trưng hành vi.
3. **Trang 3 — Thực nghiệm (Experiments)**: Bảng kết quả thực nghiệm 5 mô hình cốt lõi E1–E5, hiệu năng 7 mô hình cơ sở, biểu đồ đường cong hội tụ PSO qua 10 vòng lặp (SVG) và đường cong ROC Curve trên 32.000 mẫu Holdout.
4. **Trang 4 — Hành vi & Sai số (Insights)**: Kiểm toán ma trận nhầm lẫn thực tế của mô hình chuẩn (TN=15,740, FP=9,763, FN=3,078, TP=3,419), phân tích định tính nhóm FP ("Window Shoppers") vs FN ("Decisive Buyers"), 4 hàm ý kinh doanh chiến lược.
5. **Trang 5 — Demo Dự đoán (Prediction Demo)**: Công cụ mô phỏng tính điểm xác suất mua hàng trực tiếp (Propensity Scoring) dựa trên trọng số XGBoost và 17 biến PSO với thanh trượt tham số, đồng hồ đo nguy cơ (Gauge meter), phân loại ý định mua và khuyến cáo đạo đức dữ liệu.
6. **Trang 6 — Tài liệu & Tái lập (Docs & Reproducibility)**: Cung cấp liên kết tải báo cáo Word (.docx) và Markdown (.md), lệnh tái lập pipeline sạch, tài liệu đặc tả Power BI và danh mục 26 tài liệu y văn quốc tế 2021–2026 kèm DOI.

---

## 2. Hướng dẫn Khởi chạy Ứng dụng

Ứng dụng được thiết kế theo chuẩn **Zero-Dependency Modern Web Application** (sử dụng HTML5 ngữ nghĩa, Vanilla CSS hiện đại và Vanilla JS tối ưu hóa, không phụ thuộc gói npm từ internet):

### Cách 1: Mở trực tiếp bằng trình duyệt
Nhấp đúp chuột vào tệp `index.html` trong thư mục `web/` để mở trực tiếp trên trình duyệt Chrome, Edge hoặc Firefox.

### Cách 2: Khởi chạy qua máy chủ Python tích hợp (Khuyến nghị)
Tại thư mục gốc của repository, mở terminal và chạy lệnh:
```bash
python -m http.server 3000 --directory web
```
Sau đó truy cập: [http://localhost:3000](http://localhost:3000) trên trình duyệt web.
