# QUYẾT ĐỊNH KIỂM ĐỊNH CUỐI CÙNG VÀ CHỐT HỒ SƠ NGHIÊN CỨU
## (FINAL DATA VALIDATION & RESEARCH ASSET LOCK DECISION)

**Dự án:** Global E-Commerce Customer Purchase Prediction (`hayd6/Global`)  
**Đề tài nghiên cứu:** Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử  
**Người thực hiện thẩm định:** Senior Data Scientist, ML Engineer & Data Auditor  
**Ngày phê duyệt:** 12/10/2026  
**Căn cứ pháp lý & kỹ thuật:**
- Báo cáo kiểm định độc lập: [docs/INDEPENDENT_DATA_VALIDATION_REPORT.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/INDEPENDENT_DATA_VALIDATION_REPORT.md)
- Bộ dữ liệu chuẩn kiểm soát: `outputs/controlled_benchmark/`
- Bộ kiểm thử tự động toàn diện: `tests/` (48/48 tests PASS)
- Bản đặc tả đầu vào báo cáo Word: [docs/WORD_REPORT_INPUT_SPECIFICATION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/WORD_REPORT_INPUT_SPECIFICATION.md)

---

## 1. NGUYÊN TẮC RA QUYẾT ĐỊNH (GOVERNING PRINCIPLES)

1. **Tuyệt đối trung thực khoa học:** Không sửa đổi, tinh chỉnh số liệu hoặc thay đổi tham số thuật toán để làm kết quả "đẹp hơn" hoặc cố tình chứng minh PSO vượt trội ANOVA.
2. **Nguyên tắc "Chỉ sửa khi có lỗi cụ thể được xác nhận":** Không tái sinh dữ liệu, không sửa code pipeline và không chạy lại thực nghiệm nếu không phát hiện lỗi kỹ thuật hoặc rò rỉ phương pháp luận.
3. **Phân biệt rành mạch giữa Tính đúng của Code và Tính hợp lý của Đặc tả:** Thừa nhận rõ ràng dataset là mô hình tham số mô phỏng có kiểm soát (Controlled Longitudinal Synthetic Benchmark), không mạo nhận là dữ liệu giao dịch thực tế của doanh nghiệp.
4. **Bảo tồn tính tái lập tuyệt đối:** Mọi artifact đã xác minh phải được giữ nguyên vẹn mã băm SHA-256 để phục vụ đối chiếu độc lập trong quá trình bảo vệ đồ án.

---

## 2. BẢNG QUYẾT ĐỊNH HẠNG MỤC (MASTER DECISION MATRIX)

| STT | Hạng mục thẩm định | Bằng chứng kiểm định hiện có | Lỗi đã xác nhận hay chưa | Có cần sửa Code / Dữ liệu không? | Cách kiểm tra sau sửa (nếu có) | Điều kiện nghiệm thu đạt chuẩn | Quyết định chính thức |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- | :---: |
| **1** | **Bộ dữ liệu chuẩn kiểm soát (`outputs/controlled_benchmark/`)** | Khớp 6/6 mã hash SHA-256 với manifest. 0 trùng PK trên 6 bảng. 0 bản ghi mồ côi (FK). Min items = 1, Max = 15. Min order value = $18.05. 0 phiên/giao dịch trước ngày mở tài khoản. Min account age = 45 ngày. | **KHÔNG CÓ LỖI** | **KHÔNG SỬA** | Không áp dụng (Giữ nguyên vẹn). | 100% ràng buộc schema, tính toàn vẹn và nhân quả thời gian được bảo toàn. | **LOCK (KHÓA DỮ LIỆU)** |
| **2** | **Quy tắc sinh dữ liệu & Cấu trúc tham số (`generate_controlled_benchmark.py`)** | Code thực thi chính xác 100% 9 quy tắc sinh dữ liệu theo phân phối toán học định sẵn. Các thuộc tính tiềm ẩn $z_i \sim \mathcal{N}(0, 1)$, Poisson session intensity, Logistic buy probability được sinh đúng đặc tả. | **KHÔNG CÓ LỖI MÃ NGUỒN** (Giới hạn: Là mô hình tham số giả lập, không có dữ liệu thực tế ngoài đời đối chứng). | **KHÔNG SỬA** (Không chạy lại script để tránh làm lệch hash). | Không áp dụng. | Ghi rõ bản chất dữ liệu là Controlled Synthetic Benchmark trong văn bản báo cáo. | **ACCEPTED AS IS (CHẤP NHẬN)** |
| **3** | **Tạo nhãn mục tiêu PIT (`customer_labels_pit.csv`)** | Tái tính toán độc lập bằng DuckDB từ bảng `transactions.csv` khớp 25,000 / 25,000 khách hàng (0 dòng lệch). Nhãn dương: 2,195 (8.7800%), Nhãn âm: 22,805. Ranh giới $(t_0, t_0+30\text{d}]$ chuẩn tắc. 97 giao dịch tại $t_0$ tính vào quá khứ. | **KHÔNG CÓ LỖI** | **KHÔNG SỬA** | Không áp dụng. | Nhãn mục tiêu phản ánh đúng giao dịch tương lai, không có lookahead bias. | **LOCK (KHÓA NHÃN)** |
| **4** | **Trích xuất đặc trưng & Chống rò rỉ thời gian (Anti-Leakage)** | Kiểm định tiêm dữ liệu tương lai trên 100 khách hàng: toàn bộ 69 cột đặc trưng giữ nguyên giá trị (0 sai lệch). Biến khoảng cách thời gian cố định theo $t_0 = \text{2024-06-01}$. | **KHÔNG CÓ LỖI** | **KHÔNG SỬA** | Không áp dụng. | 100% đặc trưng bất biến trước các sự kiện phát sinh sau mốc chốt $t_0$. | **PASSED & FROZEN** |
| **5** | **Số chiều không gian đặc trưng (64, 68, 71, 83)** | Đã chứng minh nguồn gốc đại số: $71 = 3\text{ admin} + 68\text{ candidate} = 3 + 4\text{ cat} + 64\text{ continuous}$. One-Hot 4 biến phân loại sinh thêm 19 cột, tổng $64 + 19 = 83$ đặc trưng đầu vào baseline. | **KHÔNG CÓ LỖI** (Các con số đại diện cho các không gian khác nhau). | **KHÔNG SỬA** | Không áp dụng. | Đưa bảng giải thích số chiều vào Chương 3 và 4 của báo cáo Word. | **VERIFIED (ĐÃ GIẢI MÃ)** |
| **6** | **Phân tách Train/Validation/Holdout** | 20,000 Train (8.781%), 5,000 Holdout (8.780%). Giao tập index = 0, giao tập ID = 0. Bộ tiền xử lý chỉ fit trên Train. PSO chạy Inner Train (15k) và Inner Val (5k) nằm trong Train (20k), không chạm Holdout. | **KHÔNG CÓ LỖI** | **KHÔNG SỬA** | Không áp dụng. | Tập Holdout hoàn toàn độc lập, đảm bảo tính khách quan trong đánh giá. | **PASSED & COMPLIANT** |
| **7** | **Giải thuật tối ưu PSO và ANOVA F-test** | Cả hai loại bỏ 7/7 biến nhiễu tại seed=42. ANOVA đạt PR-AUC cao hơn (+0.0485 trên Gradient Boosting), chạy trong 0.03s. BPSO giảm 75% số chiều (16/64), tăng tốc XGBoost lên 0.47s (1.68 lần). Đã ghi nhận tính stochastic của BPSO trên đa seed. | **KHÔNG CÓ LỖI THUẬT TOÁN** | **KHÔNG SỬA** (Không đổi seed hoặc tham số để cố tình nâng metrics PSO). | Không áp dụng. | Thừa nhận trung thực ưu thế PR-AUC của ANOVA và ưu thế tăng tốc của BPSO trong báo cáo. | **ACCEPTED AS IS (CHẤP NHẬN)** |
| **8** | **Chỉ số hiệu năng mô hình Holdout Test (Metrics)** | Tái tính toán độc lập khớp 100%: TN=3,641, FP=920, FN=194, TP=245. PR-AUC=0.2590, ROC-AUC=0.7659, F1=0.3055, Acc=0.7772. Khớp đúng giữa CSV dự đoán, JSON metadata và web metrics. | **KHÔNG CÓ LỖI TÍNH TOÁN** | **KHÔNG SỬA** | Không áp dụng. | Giữ nguyên vẹn toàn bộ số liệu đo đạc thực tế, không bịa đặt số liệu. | **FINALIZED (CHỐT SỐ LIỆU)** |
| **9** | **Danh mục 28 Tài liệu tham khảo và Phân giải DOI** | 28/28 tài liệu đã được xác minh thành công (25 tài liệu gốc PASS; 3 tài liệu 15, 18, 22 đã được xác minh thủ công qua MDPI, TechScience, arXiv và cập nhật mã định danh chuẩn). | **ĐÃ GIẢI QUYẾT TRIỆT ĐỂ** | **KHÔNG SỬA CODE/DATA.** (Đã cập nhật đúng siêu dữ liệu trong `WORD_REPORT_INPUT_SPECIFICATION.md`). | Kiểm tra HTTP/HEAD trên doi.org và trang nhà xuất bản. | 100% trích dẫn được xác thực trước khi xuất bản bản in luận văn chính thức. | **VERIFIED & READY** |

---

## 3. TRẢ LỜI DỨT ĐIỂM 5 CÂU HỎI KẾT LUẬN

### Câu hỏi 1: Dataset hiện tại có thể dùng làm dữ liệu thực nghiệm chính thức theo thiết kế nghiên cứu hay chưa?
**TRẢ LỜI: CÓ, ĐÃ HOÀN TOÀN ĐỦ ĐIỀU KIỆN ĐỂ SỬ DỤNG.**
- *Căn cứ:* Bộ dữ liệu `outputs/controlled_benchmark/` đã khắc phục triệt để mọi lỗi logic và khuyết tật chất lượng dữ liệu của bộ dữ liệu gốc Kaggle (nghịch lý nhãn mua hàng không liên quan đến chi tiêu, đảo lộn trật tự thời gian 49.8% phiên trước ngày mở tài khoản, số lượng hàng âm, rò rỉ dữ liệu tương lai).
- *Tính hợp lệ phương pháp luận:* Cấu trúc Point-in-Time với mốc chốt $t_0 = \text{2024-06-01}$ và cửa sổ nhãn 30 ngày $(t_0, t_0+30\text{d}]$ tuân thủ chuẩn mực thiết kế nghiên cứu Machine Learning chuỗi thời gian quốc tế.
- *Phạm vi áp dụng:* Dataset đóng vai trò là **Controlled Synthetic Benchmark Dataset** để kiểm chứng quy trình Big Data và thuật toán metaheuristic BPSO.

### Câu hỏi 2: Những gì đã được xác minh là đúng?
**TRẢ LỜI: CÁC NỘI DUNG SAU ĐÃ ĐƯỢC XÁC MINH ĐÚNG BẰNG BẰNG CHỨNG ĐO ĐẠC ĐỘC LẬP (PASS):**
1. **Toàn vẹn tệp tin và Schema:** 6/6 file CSV khớp 100% mã hash SHA-256; 0 duplicate khóa chính; 0 bản ghi mồ côi khóa ngoại.
2. **Logic kinh doanh và Nhân quả thời gian:** 100% phiên truy cập và giao dịch diễn ra sau ngày đăng ký tài khoản; 100% phiên quảng cáo nằm trong thời hạn chiến dịch; 100% đơn hàng có $items\_count \ge 1$; 100% khách hàng có độ tuổi tài khoản $\ge 45$ ngày tại $t_0$.
3. **Nhãn mục tiêu Point-in-Time:** Tái tính toán độc lập khớp 25,000 / 25,000 khách hàng; tỷ lệ dương tính đạt chuẩn mất cân bằng thực tế 8.7800% (2,195 khách hàng dương tính).
4. **Tính trơ thời gian (Anti-Leakage):** Đã kiểm định toàn diện trên 69 cột đặc trưng nghiệp vụ qua kịch bản tiêm dữ liệu tương lai; 0 / 69 cột bị thay đổi giá trị.
5. **Cách ly phân tập dữ liệu:** Tập Train (20,000) và Holdout (5,000) hoàn toàn độc lập (0 ID trùng lặp); bộ tiền xử lý chỉ fit trên Train; BPSO chỉ tối ưu trên Inner Train và Inner Val.
6. **Tái tính toán metrics:** Toàn bộ chỉ số ma trận nhầm lẫn (TN=3641, FP=920, FN=194, TP=245), Accuracy (77.72%), F1 (0.3055), PR-AUC (0.2590) và ROC-AUC (0.7659) khớp đúng giữa file dự đoán, file metadata và giao diện Web.
7. **Năng lực đào thải biến nhiễu:** Cả ANOVA và BPSO (tại seed=42) đào thải 7/7 biến nhiễu nhân tạo.
8. **Danh mục tài liệu học thuật:** 28/28 tài liệu (100%) có đầy đủ tác giả, năm, tên bài và mã DOI/URL hợp lệ.
9. **Kiểm thử tự động:** 48/48 bài kiểm thử `pytest` đạt trạng thái PASS trong 15.27 giây.

### Câu hỏi 3: Những gì còn thiếu bằng chứng?
**TRẢ LỜI: CÁC GIỚI HẠN VÀ NỘI DUNG CÒN THIẾU BẰNG CHỨNG GỒM:**
1. **Tính đại diện thị trường thực tế (Empirical Market Realism):** Dataset được sinh từ mô hình tham số giả lập ($z_i \sim \mathcal{N}(0, 1)$, Poisson, Logistic). Mặc dù tuân thủ đúng code, các phân phối này chưa được đối chiếu hoặc hiệu chuẩn từ nhật ký log của một doanh nghiệp TMĐT thực tế bên ngoài (`INSUFFICIENT EVIDENCE`).
2. **Độ ổn định loại bỏ biến nhiễu trên mọi seed của PSO:** Tại seed=42, PSO loại bỏ 100% biến nhiễu; tuy nhiên khi thử nghiệm trên seed 43 và 44, do số lượng hạt (16) và vòng lặp (12) bị giới hạn để chạy trên CPU thông thường, 2–3 biến nhiễu có thể chưa bị đào thải hoàn toàn.
3. **Tải dữ liệu clickstream 10GB từ Internet:** Bị chặn do môi trường máy trạm nội bộ không có tài khoản đám mây ngoài (`BLOCKED`).

### Câu hỏi 4: Có lỗi nào bắt buộc phải sửa không?
**TRẢ LỜI: KHÔNG CÓ BẤT KỲ LỖI BẮT BUỘC NÀO TRONG MÃ NGUỒN, DỮ LIỆU HOẶC HỒ SƠ TÀI LIỆU CẦN SỬA.**
- Không có lỗi cú pháp, không có lỗi rò rỉ dữ liệu, không có lỗi tính toán chỉ số, không có vi phạm khóa quan hệ hay trật tự thời gian.
- Toàn bộ danh mục 28 tài liệu học thuật đã được chuẩn hóa và kiểm tra phân giải thành công. Toàn bộ hồ sơ đã hoàn thiện 100%.

### Câu hỏi 5: Nếu không còn lỗi bắt buộc, xác nhận có thể khóa phiên bản dữ liệu và chuyển sang viết báo cáo Word hay chưa?
**TRẢ LỜI: XÁC NHẬN CHÍNH THỨC — ĐÃ ĐỦ ĐIỀU KIỆN KHÓA TOÀN BỘ PHIÊN BẢN DỮ LIỆU VÀ CHUYỂN SANG VIẾT BÁO CÁO WORD.**
- **Trạng thái Dữ liệu:** ĐÓNG BĂNG HOÀN TOÀN (FROZEN). Mọi tệp trong `outputs/controlled_benchmark/` giữ nguyên mã hash SHA-256 hiện tại.
- **Trạng thái Mã nguồn:** KHÓA PIPELINE (LOCKED). Không thay đổi logic tiền xử lý, trích xuất đặc trưng và mô hình hóa.
- **Trạng thái Báo cáo:** Hồ sơ số liệu, bảng biểu, công thức toán học và cấu trúc 6 phần đã được chuẩn bị đầy đủ và đồng bộ tại [WORD_REPORT_INPUT_SPECIFICATION.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/WORD_REPORT_INPUT_SPECIFICATION.md).
- **Hành động tiếp theo:** Chuyển sang giai đoạn viết báo cáo Word chính thức theo đúng dàn ý 6 phần trong `DanY6Phan.md`.
