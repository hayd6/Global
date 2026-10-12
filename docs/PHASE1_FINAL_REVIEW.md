# BÁO CÁO RÀ SOÁT VÀ HIỆU CHỈNH CUỐI CÙNG GIAI ĐOẠN 1
## (Phase 1 Final Review & Scientific Calibration Report)

- **Tên đề tài chính thức:** *"Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử."*
- **Tài liệu căn cứ tối cao:** [DanY6Phan.md](file:///d:/HuyD/Đại Học/BigData/Global/DanY6Phan.md) (Dàn ý nghiên cứu gốc 6 phần)
- **Tài liệu liên quan:** [OUTLINE_COMPLIANCE_AUDIT.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/OUTLINE_COMPLIANCE_AUDIT.md), [IMPLEMENTATION_PLAN.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/IMPLEMENTATION_PLAN.md) (v2.0), [PROGRESS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/PROGRESS.md)
- **Ngày thực hiện:** 2026-10-12
- **Trạng thái:** Hoàn tất rà soát Giai đoạn 1 — Đang dừng chờ phê duyệt, chưa bắt đầu Giai đoạn 2.

---

## 1. Mục đích văn bản

Văn bản này tổng kết toàn diện các nội dung hiệu chỉnh khoa học đối với kế hoạch triển khai dự án sau khi tiếp thu các chỉ đạo rà soát:
1. Loại bỏ triệt để các tuyên bố tuyệt đối không có căn cứ kiểm chứng khoa học.
2. Thiết lập hệ thống phân loại trạng thái khách quan dựa trên mức độ sẵn sàng thực tế của sản phẩm (không coi việc có code/số liệu là hoàn thành bài báo khoa học).
3. Thừa nhận trung thực kết quả thực nghiệm về sự đánh đổi của thuật toán PSO so với ANOVA F-test và Full Features.
4. Chuẩn hóa tiêu chí thẩm định tài liệu học thuật, phân tích lỗi định tính FP/FN và phân lập độc lập hai sản phẩm Power BI vs Website.

---

## 2. Chi tiết 8 nội dung hiệu chỉnh quan trọng

### 2.1. Hiệu chỉnh tuyên bố về rò rỉ dữ liệu (Data Leakage Calibration)
- **Hiện trạng cũ:** Từng xuất hiện các tuyên bố tuyệt đối như *"đã triệt tiêu 100% Cross-Split Data Leakage"* hoặc *"Leakage-Free Protocol"*.
- **Hiệu chỉnh mới:**
  - **Cross-Split Data Leakage:** Được xác định là *kiểm chứng trong phạm vi pipeline Scikit-Learn và [split_manager.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/split_manager.py) hiện có*. Các bộ biến đổi (`StandardScaler`, `SimpleImputer`, `OneHotEncoder`, `SelectKBest`) chỉ được `fit` trên 128,000 dòng tập Train; không phát hiện trùng lặp chỉ số giữa Train 128k và Holdout 32k (`test_split_consistency_and_holdout_isolation` PASS). Ranh giới này được giới hạn rõ trong các bước tiền xử lý đã mã hóa.
  - **Temporal Leakage:** **CHƯA THỂ LOẠI TRỪ**. Việc `target` không tương quan với số giao dịch trong 30 ngày cuối ($p > 0.05$) chỉ chứng minh target không được tính đơn thuần từ số lượng giao dịch 30 ngày cuối. Do bộ dữ liệu Kaggle là ảnh chụp quan sát đa bảng tĩnh không cung cấp mốc thời gian cắt dự đoán (Prediction Cutoff Timestamp), các biến đặc trưng tích lũy toàn thời gian (Lifetime aggregations) vẫn có rủi ro tiềm ẩn chứa thông tin phát sinh sau thời điểm nhãn được xác định nếu nhãn được gán trong quá khứ.
  - **Chuẩn hóa định danh bài toán:** Bắt buộc sử dụng thuật ngữ: **"Phân loại độ nghiêng mua hàng trên ảnh chụp dữ liệu quan sát đa bảng (Observational Snapshot Purchase Propensity Classification)"**. Tuyệt đối không tuyên bố là bài toán dự báo tương lai 30 ngày đã chứng minh phi rò rỉ thời gian.

### 2.2. Phân biệt 4 cấp độ sẵn sàng (Artifact Readiness Levels - ARL)
Để tránh nhầm lẫn giữa việc hoàn thành tầng kỹ thuật với việc hoàn thành bài báo khoa học, toàn bộ các hạng mục trong [IMPLEMENTATION_PLAN.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/IMPLEMENTATION_PLAN.md) được phân định theo 4 cấp độ:
- **ARL Mức 1 — Kế hoạch & Cấu trúc (Plan & Schema):** Bản đặc tả, sơ đồ, phân rã công việc.
- **ARL Mức 2 — Artifact kỹ thuật (Technical Artifacts):** Mã nguồn, Parquet, CSV, metrics, plots.
- **ARL Mức 3 — Văn bản học thuật (Academic Narrative):** Bản thảo bài báo khoa học chi tiết trong `docs/report/` có lập luận, trích dẫn, bảng số liệu và phân tích giới hạn.
- **ARL Mức 4 — Kiểm chứng độc lập (Verified & Audited):** Đạt kiểm thử tự động, kiểm toán chéo và tái lập độc lập.

*Hệ quả:* Tất cả các hạng mục của Phần 1, 2, 3, 4, 6 dù đã có mã nguồn hoặc kết quả thực nghiệm Mức 2 đều được chuyển chính xác sang trạng thái: **"Hoàn thành một phần (Đã có artifact kỹ thuật Mức 2, Chưa có văn bản học thuật Mức 3)"**.

### 2.3. Báo cáo trung thực kết quả so sánh PSO vs ANOVA vs Full Features
- **Số liệu thực tế đã kiểm chứng trên tập Holdout 32,000 khách hàng (ngưỡng 0.5):**
  - **Baseline Gradient Boosting:**
    - *Full Features (63 biến):* PR-AUC = `0.2730`, ROC-AUC = `0.6078`, Fit = `16.96s`, Search = `0.0s`, Tổng chi phí = `16.96s`.
    - *ANOVA F-test (17 biến):* PR-AUC = `0.2759`, ROC-AUC = `0.6105`, Fit = `6.35s`, Search = `0.13s`, Tổng chi phí = `6.48s`.
    - *Binary PSO (17 biến):* PR-AUC = `0.2601`, ROC-AUC = `0.5894`, Fit = `4.52s`, Search = `11.79s`, Tổng chi phí = `16.31s`.
  - **XGBoost nâng cao:**
    - *XGBoost Full (63 biến):* PR-AUC = `0.2654`, ROC-AUC = `0.6006`, Fit = `4.65s`, Search = `0.0s`, Tổng chi phí = `4.65s`.
    - *XGBoost PSO (17 biến):* PR-AUC = `0.2584`, ROC-AUC = `0.5846`, Fit = `2.22s`, Search = `11.79s`, Tổng chi phí = `14.01s`.
- **Kết luận:** PSO **không vượt trội** ANOVA F-test hay Full Features về chỉ số dự đoán trên bộ dữ liệu này. Giá trị thực tế của PSO là tối ưu đa tiêu chí trong không gian rời rạc, giúp **giảm 73.02% số chiều đặc trưng** và **giảm hơn 50% thời gian huấn luyện mô hình hạ nguồn** (từ 4.65s xuống 2.22s trên XGBoost), nhưng phải trả chi phí tìm kiếm ban đầu (`11.79s`) và chấp nhận sụt giảm nhẹ PR-AUC (`-0.0070`).

### 2.4. Tiêu chuẩn phân tích lỗi định tính FP/FN trên tập Holdout
- Bắt buộc thực hiện trên tập 32,000 dòng Holdout thực tế từ [metrics_comparison.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/metrics_comparison.csv) (TP: 3,419; FP: 9,763; TN: 15,740; FN: 3,078 đối với XGBoost Full).
- Phân tích dựa trên phân vị thống kê (Min, Q25, Median, Q75, Max) của các biến hành vi quan trọng (`cart_additions_sum`, `order_value_sum`, `session_duration_mean`, `recency`).
- Tuyệt đối không bịa đặt hồ sơ nhân vật giả định ("anh A, chị B"); không suy diễn quan hệ nhân quả; phân biệt rõ giữa tương quan thống kê và giả thuyết kinh doanh.

### 2.5. Tiêu chuẩn 5 điểm thẩm định tối thiểu 25 tài liệu học thuật (2021–2026)
- Phân bổ bắt buộc: Mua hàng TMĐT ($\ge 6$), Feature Engineering/Selection ($\ge 6$), PSO + Boosting ($\ge 7$), Đánh giá/Giải thích mô hình ($\ge 6$).
- 5 Tiêu chuẩn kiểm chứng: (1) Tác giả/Năm xác thực, (2) Tên bài/Nguồn xuất bản có thật, (3) DOI/URL truy cập được, (4) Nội dung thực sự liên quan, (5) Trích dẫn trung thực không bịa kết quả.
- *Quy tắc dự phòng:* Nếu không tìm đủ 25 bài đạt cả 5 chuẩn, phải báo cáo trung thực số lượng thực tế thẩm định được, không tạo nguồn giả.

### 2.6. Phân lập giải pháp Power BI Dashboard và Website React + Vite
- Website React + Vite và Power BI Dashboard là hai sản phẩm đầu ra hoàn toàn riêng biệt. Website **không được coi là sản phẩm thay thế** cho file `.pbix`.
- Do giới hạn môi trường dòng lệnh không có GUI để mở Power BI Desktop, gói bàn giao kỹ thuật của Power BI bao gồm:
  1. 7 bảng CSV sạch tại `outputs/powerbi/`.
  2. `DATA_MODEL_SCHEMA.md`: Đặc tả Star Schema, khóa liên kết, kiểu dữ liệu.
  3. `POWER_BI_DESIGN_GUIDE.md`: Bản thiết kế chi tiết 4 trang gồm visuals, bố cục tọa độ và bộ công thức DAX measures (đã kiểm tra khớp số liệu Python).
  4. Quy trình thao tác thủ công 5 bước để người dùng mở Power BI Desktop và lưu file `global_ecommerce_dashboard.pbix`.

### 2.7. Đối chiếu toàn diện 100% đề mục DanY6Phan.md
- Không bỏ sót bất kỳ đề mục nào từ Phần 1 đến Phần 6 (bao gồm các tiểu mục 1.1–1.8, 2.1–2.7, 3.1–3.7, 4.1–4.8, 5.1–5.7, 6.1–6.6).
- Mỗi mục đều có mã công việc, người phụ trách chính theo đúng phân công Người 1, 2, 3, 4 của dàn ý gốc.

### 2.8. Đồng bộ trạng thái với PROGRESS.md
- Đã cập nhật [docs/PROGRESS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/PROGRESS.md) thể hiện đúng trạng thái: Giai đoạn 1 đã hoàn thành rà soát v2.0 và đang dừng chờ phê duyệt; các Giai đoạn 2 đến 6 ở trạng thái "Chưa thực hiện (Chờ duyệt GĐ 1)".

---

## 3. Danh sách các điểm chưa thể xác minh (Unverified Items & Known Boundaries)

1. **Mốc thời gian cắt dự đoán (Prediction Cutoff Timestamp):** Bộ dữ liệu Kaggle không cung cấp mốc thời gian chốt nhãn -> Không thể chứng minh bằng thực nghiệm rằng mô hình đang dự báo tương lai 30 ngày.
2. **Quy tắc sinh nhãn mục tiêu của Kaggle:** Không có văn bản chính thức xác nhận cách tính `target=1` -> Phải coi là nhãn quan sát tĩnh.
3. **Hiệu quả kinh doanh và quan hệ nhân quả:** Mức độ quan trọng của đặc trưng (Feature Importance) chỉ phản ánh mức đóng góp phân tách của thuật toán cây, không chứng minh can thiệp tiếp thị vào đặc trưng đó sẽ làm tăng tỷ lệ mua hàng.
4. **File vật lý `.pbix`:** Chưa tồn tại trong kho mã nguồn do hạn chế môi trường không có giao diện đồ họa Windows Desktop.

---

## 4. Danh sách Tiêu chí Nghiệm thu Tổng thể đã hiệu chỉnh

| STT | Tiêu chí nghiệm thu | Mức ARL yêu cầu | Trạng thái hiện tại | Ghi chú & Bằng chứng |
| :---: | :--- | :---: | :---: | :--- |
| **TC-1** | Phân rã 100% đề mục DanY6Phan.md vào kế hoạch chi tiết | Mức 1 | **ĐẠT** | [docs/IMPLEMENTATION_PLAN.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/IMPLEMENTATION_PLAN.md) v2.0 |
| **TC-2** | Thẩm định tối thiểu 25 tài liệu học thuật (2021–2026) theo 5 tiêu chuẩn | Mức 3 | **Chưa thực hiện** | Dự kiến hoàn thành trong Giai đoạn 2 |
| **TC-3** | Pipeline ML, Split cố định, 7 Baselines, PSO và XGBoost vượt qua bộ test | Mức 2 & 4 | **ĐẠT** | 18/18 pytest passed; holdout isolation verified |
| **TC-4** | Phân tích định tính lỗi FP/FN trên tập Holdout 32k thực tế (không bịa đặt) | Mức 3 | **Chưa thực hiện** | Dự kiến hoàn thành trong Giai đoạn 2 |
| **TC-5** | Website nghiên cứu React + Vite hoàn chỉnh trong `web/` có demo suy luận tĩnh | Mức 2 & 4 | **Chưa thực hiện** | Dự kiến hoàn thành trong Giai đoạn 3 |
| **TC-6** | Giải pháp Power BI: 7 CSV sạch, schema quan hệ, guide thiết kế 4 trang kèm DAX | Mức 2 | **Hoàn thành một phần** | 7 CSV đã có; guide và manual build ở Giai đoạn 4 |
| **TC-7** | Tập 6 file báo cáo học thuật chuyên sâu `docs/report/Phan_1.md` đến `Phan_6.md` | Mức 3 | **Chưa thực hiện** | Dự kiến hoàn thành trong Giai đoạn 5 |
| **TC-8** | Báo cáo nghiệm thu cuối cùng `docs/FINAL_ACCEPTANCE_REPORT.md` và kiểm thử tích hợp | Mức 4 | **Chưa thực hiện** | Dự kiến hoàn thành trong Giai đoạn 6 |

---

## 5. Xác nhận trạng thái

- **Mã nguồn mô hình:** Giữ nguyên 100%, không sửa đổi.
- **Dữ liệu và kết quả thực nghiệm:** Giữ nguyên 100%, không chạy lại pipeline lớn.
- **Giai đoạn tiếp theo (Giai đoạn 2):** **CHƯA BẮT ĐẦU**.
- **Trạng thái thực tế:** Đang dừng lại tại điểm kiểm soát Giai đoạn 1 để chờ Người dùng phê duyệt toàn bộ kế hoạch và báo cáo rà soát.
