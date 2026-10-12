# BÁO CÁO NGHIỆM THU BÀN GIAO GIAI ĐOẠN 2 (PHIÊN BẢN KIỂM ĐỊNH TOÀN DIỆN V2.1)
## (Phase 2 Final Acceptance & Verification Report — Academic & Empirical Rigor)

- **Tên đề tài chính thức:** *"Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử."*
- **Tài liệu căn cứ tối cao:** [DanY6Phan.md](file:///d:/HuyD/Đại Học/BigData/Global/DanY6Phan.md) (Mục 2.7, 4.7, 5.7, 6.6.1)
- **Tài liệu kế hoạch đã duyệt:** [IMPLEMENTATION_PLAN.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/IMPLEMENTATION_PLAN.md) (v2.0), [PHASE1_FINAL_REVIEW.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/PHASE1_FINAL_REVIEW.md)
- **Ngày kiểm định hoàn tất:** 2026-10-12
- **Trạng thái thực tế:** Hoàn thành toàn diện kiểm toán Giai đoạn 2 — **Đang dừng chờ phê duyệt, tuyệt đối chưa bắt đầu Giai đoạn 3**.

---

## 1. Tóm tắt Kết quả Kiểm toán & Bàn giao Giai đoạn 2

Toàn bộ công việc Giai đoạn 2 đã được rà soát, đối chiếu và hiệu chỉnh chuyên sâu theo 4 nhóm yêu cầu kiểm định:

### 1.1. Kiểm tra nguồn gốc Ma trận Nhầm lẫn, Khớp nối Khách hàng & Artifact Tái lập (Part A)
1. **Xác nhận cấu trúc `metrics_comparison.csv`:**
   - Tệp chính thức [outputs/metrics/metrics_comparison.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/metrics_comparison.csv) chứa đầy đủ **21 cột**:
     `model_name`, `feature_count`, `pr_auc`, `roc_auc`, `f1_score`, `precision`, `recall`, `accuracy`, `threshold`, `threshold_source`, `best_f1_threshold_ref`, `true_negatives`, `false_positives`, `false_negatives`, `true_positives`, `fit_time_seconds`, `search_time_seconds`, `total_time_seconds`, `split_id`, `evaluation_set`, `feature_space`.
   - **Cột 12–15 lưu trữ trực tiếp các số đếm ma trận nhầm lẫn:**
     - Dòng 5 (`XGBoost (Full Features)`): `true_negatives=15740`, `false_positives=9763`, `false_negatives=3078`, `true_positives=3419`.
     - Dòng 6 (`XGBoost (PSO Features)`): `true_negatives=16067`, `false_positives=9436`, `false_negatives=3327`, `true_positives=3170`.
2. **Chứng minh Khớp nối Khách hàng 1-1 (Rigorous Customer ID Alignment Proof):**
   - Trong `src/models/split_manager.py`, DuckDB nạp dữ liệu bằng `ORDER BY customer_id`, bảo đảm dataframe `df` được sắp xếp tất định từ dòng 0 đến 159,999.
   - Mảng `holdout_idx` (32,000 dòng) được lưu trong `outputs/processed/split_indices.npz`. Khóa băm kiểm định SHA-256 tính từ chuỗi byte `int64` của 32,000 khách hàng tập holdout là `008236ea0d8461b4d5f58b34e973766d4a696a20c97b8d28a4b9d025c99a5da2` (khớp 100% giữa artifact, ground truth DuckDB và `configs/split_metadata.json`).
   - Thứ tự dòng được chứng minh toán học và thực nghiệm là đồng nhất 100% giữa $X_{\text{holdout}}$, $y_{\text{holdout}}$, xác suất $\hat{p}$, nhãn dự đoán $\hat{y}$ và các đặc trưng vi mô của `df.iloc[holdout_idx]`. Đã kiểm chứng toàn bộ 32,000 ID, không chỉ 5 mẫu đầu tiên.
3. **Tạo lập Artifact Holdout độc lập tăng tính tái lập & Kiểm định Tự động 7 bài test:**
   - Để hỗ trợ thẩm định độc lập mà không can thiệp hay thay đổi kết quả thực nghiệm gốc, đề tài đã xuất bản tệp [outputs/holdout_predictions.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/holdout_predictions.csv) (32,000 dòng gồm `customer_id`, `y_true`, `y_proba`, `y_pred`, `error_group`) và [outputs/holdout_prediction_metadata.json](file:///d:/HuyD/Đại Học/BigData/Global/outputs/holdout_prediction_metadata.json).
   - Tệp được kiểm chứng tự động toàn diện qua bộ test [tests/test_holdout_predictions_artifact.py](file:///d:/HuyD/Đại Học/BigData/Global/tests/test_holdout_predictions_artifact.py) (7/7 tests passed):
     1. Kiểm tra cấu trúc 32,000 dòng, không null, không trùng ID, đủ 5 cột.
     2. Kiểm tra `y_true`, `y_pred` $\in \{0, 1\}$; `y_proba` hữu hạn, không NaN, trong $[0, 1]$.
     3. Kiểm tra từng dòng `error_group` khớp quy tắc phân loại TP/TN/FP/FN.
     4. Kiểm tra toàn bộ 32,000 `customer_id`, thứ tự dòng và `y_true` khớp 100% với Holdout gốc.
     5. Tự tính SHA-256 từ mảng `customer_id` theo chuẩn bytes `int64` và đối chiếu với Holdout gốc.
     6. Lọc động dòng `XGBoost (Full Features)` trong `metrics_comparison.csv` theo các khóa metadata (không dùng chỉ số dòng cố định) và đối chiếu khớp tuyệt đối TN=15,740, FP=9,763, FN=3,078, TP=3,419.
     7. Đối chiếu metadata `scale_pos_weight` với nhãn âm (102,011) và nhãn dương (25,989) của đúng tập Train được mô hình sử dụng (tỷ lệ $3.925160644888222$).

### 1.2. Kiểm tra Tham số Mô hình & Mã nguồn Thực thi (Part B)
1. **Đối chiếu mã nguồn:** Mã nguồn `src/models/train_xgboost.py:124-134` sử dụng:
   - `n_estimators=150`, `max_depth=6`, `learning_rate=0.08`, `subsample=0.85`, `colsample_bytree=0.85`, `random_state=42`, `n_jobs=-1`, `eval_metric="logloss"` (Xác nhận 100% từ mã nguồn).
2. **Giải quyết triệt để mâu thuẫn `scale_pos_weight`:**
   - Trong `src/models/train_xgboost.py:100`, tham số được tính toán động tại runtime trên 128,000 dòng tập Train:
     $$\text{pos\_weight} = \frac{\sum (y_{\text{train}} == 0)}{\sum (y_{\text{train}} == 1)} = \frac{102,011}{25,989} \approx 3.925160644888222$$
   - Giá trị thực sự được nạp vào `XGBClassifier` là số thực dấu phẩy động `3.925160644888222` (làm tròn 4 chữ số: `3.9252`). Con số `3.9261` trước đó là số làm tròn thô trong bản thảo nháp và đã được đính chính đầy đủ.
3. **Các thành phần khác:**
   - 63 đặc trưng: Xác nhận 100% từ `split_manager.py:60-69, 180-183`.
   - Tiền xử lý: Xác nhận 100% từ `split_manager.py:184-194` (SimpleImputer + StandardScaler, fit trên Train only).
   - Ngưỡng cố định $\tau = 0.50$: Xác nhận 100% từ `metrics_comparison.csv` và `train_xgboost.py:188`.

### 1.3. Kiểm toán Toàn diện 26 Tài liệu Học thuật 2021–2026 (Part C)
- Đã thẩm định và kiểm tra trực tiếp từng mã DOI trên hệ thống [doi.org](https://doi.org) và trang nhà xuất bản chính thức (ScienceDirect, IEEE Xplore, Springer Nature, MDPI, BMC, NeurIPS).
- Mỗi mã P01–P26 được gán duy nhất một trạng thái cuối cùng, giải quyết triệt để mâu thuẫn số lượng:
  - **Khớp hoàn toàn (7 bài):** P05, P07, P08, P12, P16, P22, P26.
  - **Đã hiệu chỉnh (9 bài):** P02, P03, P04, P06, P09, P11, P14, P17, P21.
  - **Thay thế (10 bài):** P01, P10, P13, P15, P18, P19, P20, P23, P24, P25.
  - **Chưa xác minh (0 bài):** Không có (0 bài).
  - **Tổng số:** Đúng **26 bài** (100% xuất bản 2021–2026, vượt yêu cầu tối thiểu $\ge 25$ bài).

### 1.4. Phân biệt Số liệu Quan sát — Giả thuyết Phân khúc — Quan hệ Nhân quả
- Gắn nhãn tường minh: Các tên gọi *"Window Shoppers / Deal Seekers"* và *"Decisive / High AOV Buyers"* được định nghĩa chính thức là **"Giả thuyết phân khúc hành vi (Behavioral Segmentation Hypotheses)"**, không phải kết luận hành vi đã được chứng minh.
- Loại bỏ triệt để suy diễn nhân quả: Không khẳng định "tiết kiệm ngân sách tiếp thị" như một sự thật hiển nhiên từ số lượng ma trận nhầm lẫn; khẳng định việc tiết kiệm ngân sách là giả định lý thuyết và bắt buộc phải qua thử nghiệm đối chứng ngẫu nhiên (A/B Testing).
- Giữ nguyên giới hạn rò rỉ thời gian: Mốc thời gian chốt nhãn (cutoff) chưa thể xác minh trong dữ liệu gốc, định vị bài toán là *Observational Snapshot Propensity Classification*.

---

## 2. Bảng đối chiếu Chi tiết Tiêu chí Nghiệm thu Giai đoạn 2

| Mã tiêu chí | Yêu cầu theo Kế hoạch & Dàn ý gốc | Kết quả thực tế sau kiểm định | Trạng thái nghiệm thu | Tài liệu / Artifact kiểm chứng |
| :---: | :--- | :--- | :---: | :--- |
| **Y2-1** | Thu thập & thẩm định $\ge 25$ tài liệu 2021–2026 theo 4 chủ đề | Đã thẩm định thành công **26 tài liệu** phân bổ 4 nhóm: TMĐT (7 bài), Kỹ nghệ đặc trưng bảng (6 bài), PSO Boosting (7 bài), Đánh giá mất cân bằng nhãn (6 bài). | **ĐẠT** (Vượt chỉ tiêu) | [docs/LITERATURE_REVIEW.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/LITERATURE_REVIEW.md) (Mục 2 & 3) |
| **Y2-2** | 5 Tiêu chuẩn kiểm chứng tài liệu (Tác giả, Nguồn, DOI thật, Nội dung, Trích dẫn trung thực) | 100% (26/26) bài viết có DOI/URL thật có thể giải quyết được trên doi.org; thông tin tác giả, năm, tên bài và kết quả được đối chiếu trang nhà xuất bản. | **ĐẠT** | [docs/LITERATURE_REVIEW.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/LITERATURE_REVIEW.md) (Mục 1 & 2) |
| **Y2-3** | Tổng hợp khoảng trống nghiên cứu (Research Gap Analysis) | Xác định rõ 4 khoảng trống kết nối với RQ1–RQ5 và H1–H4: (1) Chi phí tìm kiếm PSO, (2) Ngộ nhận dự báo snapshot, (3) Hàm fitness cho dữ liệu lệch, (4) Khoảng cách thuật toán - quản trị. | **ĐẠT** | [docs/LITERATURE_REVIEW.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/LITERATURE_REVIEW.md) (Mục 4) |
| **Y2-4** | Phân tích FP/FN bằng dự đoán và nhãn Holdout 32k thực tế | Rút trích và kiểm chứng chính xác 32,000 dòng Holdout: TN=15,740, FP=9,763, FN=3,078, TP=3,419. Khớp 100% metrics_comparison.csv. | **ĐẠT** | [docs/ERROR_ANALYSIS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/ERROR_ANALYSIS.md) (Mục 1 & 2) |
| **Y2-5** | Bảng phân vị thống kê đặc trưng hành vi trên 4 nhóm TP, TN, FP, FN | Tính toán trung vị và trung bình cho 10 đặc trưng: `loyalty_score`, `discount_usage_rate`, `cart_additions`, `session_duration`, `AOV`,... | **ĐẠT** | [docs/ERROR_ANALYSIS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/ERROR_ANALYSIS.md) (Mục 3) |
| **Y2-6** | Bóc tách cơ chế lỗi thuật toán & phân biệt giả thuyết hành vi | Làm rõ vì sao cây XGBoost bị đánh lừa bởi `loyalty_score` và `discount_usage_rate`; ghi rõ "Window Shoppers" và "Decisive Buyers" là giả thuyết phân khúc diễn giải. | **ĐẠT** | [docs/ERROR_ANALYSIS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/ERROR_ANALYSIS.md) (Mục 4 & 5) |
| **Y2-7** | So sánh trade-off sai số giữa Full Features vs PSO Features | Định lượng rõ PSO làm tăng 249 ca FN (+8.09%), giảm 327 ca FP (-3.35%), Recall giảm từ 52.62% xuống 48.79%. Có công thức tính toán tường minh. | **ĐẠT** | [docs/ERROR_ANALYSIS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/ERROR_ANALYSIS.md) (Mục 2 & 6) |
| **Y2-8** | Hàm ý quản trị chuẩn cấu trúc 5 bước, chống suy diễn nhân quả | 3 đề xuất theo chuẩn: Phát hiện $\rightarrow$ Bằng chứng $\rightarrow$ Hàm ý $\rightarrow$ Hành động $\rightarrow$ Giới hạn/Cảnh báo rủi ro; phân định rõ tương quan và nhân quả; không tự suy diễn tiết kiệm chi phí. | **ĐẠT** | [docs/ERROR_ANALYSIS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/ERROR_ANALYSIS.md) (Mục 7) |
| **Y2-9** | Không sửa code, không chạy lại pipeline lớn, không làm Web/Power BI sớm | Giữ nguyên 100% mã nguồn `src/`, dữ liệu `dataset/` và artifacts gốc `outputs/`; chưa tạo thư mục `web/`. | **ĐẠT** | Git status & Git diff kiểm tra |
| **Y2-10**| Cập nhật tiến độ và dừng chờ phê duyệt trước Giai đoạn 3 | Cập nhật `docs/PROGRESS.md`; lập báo cáo nghiệm thu `docs/PHASE2_ACCEPTANCE_REPORT.md`; dừng chờ phê duyệt. | **ĐẠT** | [docs/PROGRESS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/PROGRESS.md) |

---

## 3. Danh mục Tệp đã Cập nhật trong Đợt Kiểm định Cuối

1. [docs/LITERATURE_REVIEW.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/LITERATURE_REVIEW.md): Chuẩn hóa 4 trạng thái độc quyền (7 Khớp hoàn toàn, 9 Đã hiệu chỉnh, 10 Thay thế, 0 Chưa xác minh); cập nhật Bảng tổng hợp trạng thái và Bảng kiểm toán 26 mục.
2. [docs/ERROR_ANALYSIS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/ERROR_ANALYSIS.md): Cập nhật danh sách 21 cột của `metrics_comparison.csv`; chứng minh khớp nối khách hàng 1-1; ghi nhận việc bổ sung artifact `outputs/holdout_predictions.csv` và `outputs/holdout_prediction_metadata.json`; cập nhật công thức tính toán `pos_weight = 102,011 / 25,989 = 3.925160644888222`.
3. [outputs/holdout_predictions.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/holdout_predictions.csv) & [outputs/holdout_prediction_metadata.json](file:///d:/HuyD/Đại Học/BigData/Global/outputs/holdout_prediction_metadata.json): Tệp artifact dự đoán độc lập 32,000 dòng tập Holdout và siêu dữ liệu tái lập.
4. [tests/test_holdout_predictions_artifact.py](file:///d:/HuyD/Đại Học/BigData/Global/tests/test_holdout_predictions_artifact.py): Bộ 7 bài kiểm thử tự động toàn diện xác nhận tính vẹn toàn, phân bố giá trị, phân nhóm lỗi TP/TN/FP/FN, khớp 32,000 khách hàng với ground truth, tự tính SHA-256 đối chiếu, lọc động ma trận nhầm lẫn từ `metrics_comparison.csv` và dẫn xuất chính xác `scale_pos_weight` từ tập Train.
5. [docs/PROGRESS.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/PROGRESS.md): Cập nhật tiến độ hoàn thành đợt kiểm định cuối Giai đoạn 2.
6. [docs/PHASE2_ACCEPTANCE_REPORT.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/PHASE2_ACCEPTANCE_REPORT.md): Báo cáo nghiệm thu toàn diện v2.1.

---

## 4. Xác nhận Kỹ thuật & Cam kết Ranh giới

- **Kết quả kiểm thử tự động:** `pytest -v` đạt **25/25 tests passed** (100% trong 7.82s trên toàn bộ 5 module kiểm thử).
- **Phạm vi kiểm thử:** Bộ kiểm thử kiểm tra toàn vẹn dữ liệu, khóa chính, không rò rỉ dữ liệu, từ điển đặc trưng, các độ đo mô hình và tệp artifact holdout. Không có thay đổi nào trong mã nguồn mô hình sản phẩm (`src/`).
- **Git diff:** Xác nhận chỉ cập nhật các tệp tài liệu trong `docs/`, bổ sung tệp kiểm thử độc lập trong `tests/` và artifact dự đoán riêng biệt trong `outputs/`; không sửa `dataset/`, `configs/` hay ghi đè các tệp kết quả gốc.
- **Cam kết chuyển giao:** **DỪNG LẠI TẠI ĐÂY**, không tự ý chuyển sang Giai đoạn 3 (Xây dựng Website React + Vite) khi chưa có văn bản phê duyệt chính thức từ Quý người dùng.
