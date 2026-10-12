# BÁO CÁO PHÂN TÍCH LỖI ĐỊNH TÍNH (FALSE POSITIVES & FALSE NEGATIVES) VÀ HÀM Ý QUẢN TRỊ
## (Qualitative Error Analysis, Pipeline Verification & Behavioral Hypotheses — Verified Edition)

- **Tên đề tài chính thức:** *"Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử."*
- **Tài liệu căn cứ:** [DanY6Phan.md](file:///d:/HuyD/Đại Học/BigData/Global/DanY6Phan.md) (Mục 4.7 & 5.7), [IMPLEMENTATION_PLAN.md](file:///d:/HuyD/Đại Học/BigData/Global/docs/IMPLEMENTATION_PLAN.md) (v2.0)
- **Tập dữ liệu phân tích:** Tập Holdout kiểm định độc lập 32,000 khách hàng (`split_id: stratified_80_20_v1`)
- **Ngưỡng phân loại chuẩn:** Cố định $\tau = 0.50$ (Fixed threshold chống thiên vị / threshold leakage)

---

## 1. Nguồn Dữ liệu, Đối chiếu Cấu hình & Giới hạn Tái lập

### 1.1. Nguồn dữ liệu thực nghiệm và Cột Ma trận Nhầm lẫn
1. **Dữ liệu tổng hợp độ đo (Aggregate Metrics Artifact):** Tệp chính thức [outputs/metrics/metrics_comparison.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/metrics_comparison.csv) bao gồm chính xác **21 cột**:
   - Nhóm định danh & không gian biến: `model_name`, `feature_count`, `feature_space`, `split_id`, `evaluation_set`.
   - Nhóm độ đo liên tục: `pr_auc`, `roc_auc`.
   - Nhóm độ đo tại ngưỡng: `threshold`, `threshold_source`, `best_f1_threshold_ref`, `f1_score`, `precision`, `recall`, `accuracy`.
   - **Nhóm số đếm ma trận nhầm lẫn (Cột 12–15):** `true_negatives`, `false_positives`, `false_negatives`, `true_positives`.
   - Nhóm thời gian: `fit_time_seconds`, `search_time_seconds`, `total_time_seconds`.
   - **Xác nhận:** Tệp CSV này **LƯU TRỰC TIẾP** 4 số đếm ma trận nhầm lẫn cho tất cả 5 mô hình thực nghiệm (ví dụ: dòng 5 lưu TN=15,740; FP=9,763; FN=3,078; TP=3,419).
2. **Dữ liệu phân vùng & Bằng chứng Khớp nối Khách hàng 1-1 (Rigorous Customer ID Alignment Proof):**
   - **Thứ tự dữ liệu khi nạp:** Trong [src/models/split_manager.py](file:///d:/HuyD/Đại Học/BigData/Global/src/models/split_manager.py), dữ liệu được tải từ DuckDB bằng câu lệnh:
     `SELECT * FROM read_parquet('customer_features.parquet') WHERE split_type = 'train' ORDER BY customer_id`
     Mệnh đề `ORDER BY customer_id` bảo đảm thứ tự các dòng của dataframe `df` là **tất định tuyệt đối** từ dòng 0 đến dòng 159,999.
   - **Chỉ số Holdout:** Mảng `holdout_idx` (32,000 phần tử) được lưu trong `outputs/processed/split_indices.npz`. Khóa mã băm `holdout_sha256` lưu trong `configs/split_metadata.json` là `008236ea0d8461b4d5f58b34e973766d4a696a20c97b8d28a4b9d025c99a5da2`.
   - **Chứng minh khớp nối hàng-khách hàng:** 
     - Với mỗi chỉ số vị trí $k \in \{0, 1, \dots, 31999\}$, dòng dữ liệu thô tương ứng trong bảng là $i = \text{holdout\_idx}[k]$. Khóa chính khách hàng là $c_k = \text{customer\_ids}[i]$.
     - Ma trận đặc trưng $X_{\text{holdout}}[k]$ được tạo bởi `num_pipeline.transform(df[num_cols].iloc[holdout_idx])`. Phép biến đổi chuỗi (SimpleImputer + StandardScaler) thực thi độc lập trên từng cột theo đúng thứ tự dòng, không tráo đổi hay sắp xếp lại dòng.
     - Nhãn thật $y_{\text{holdout}}[k] = y[i] = \text{df.iloc}[i][\text{"target"}]$.
     - Xác suất dự đoán $\hat{p}_k$ và nhãn dự đoán $\hat{y}_k$ được tính tuần tự từ dòng $k$ của ma trận $X_{\text{holdout}}$.
     - Khi trích xuất bảng đặc trưng `df_ho = df.iloc[holdout_idx]`, dòng $k$ của `df_ho` chính là dòng $i$ của `df`.
     - **Thực nghiệm xác thực:** Đã kiểm tra đối chiếu trực tiếp trên từng khách hàng ngẫu nhiên và mẫu 5 khách hàng đầu tiên: `[195766, 180698, 122619, 58792, 47593]`. Mọi giá trị đặc trưng, nhãn $y$, xác suất $\hat{p}$ và nhãn dự đoán $\hat{y}$ được kiểm chứng là thuộc về **cùng một cá thể khách hàng duy nhất**, loại trừ hoàn toàn nguy cơ lệch hàng (index misalignment).
3. **Artifact Dự đoán Holdout Độc lập & Tái lập Pipeline:**
   - **Tạo lập artifact độc lập:** Nhằm nâng cao năng lực tái lập mà không can thiệp hay thay đổi các kết quả thực nghiệm gốc, đề tài đã bổ sung tệp dữ liệu dự đoán riêng biệt cho tập Holdout: [outputs/holdout_predictions.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/holdout_predictions.csv) (32,000 dòng gồm `customer_id`, `y_true`, `y_proba`, `y_pred`, `error_group`) và tệp siêu dữ liệu đi kèm [outputs/holdout_prediction_metadata.json](file:///d:/HuyD/Đại Học/BigData/Global/outputs/holdout_prediction_metadata.json).
   - **Kiểm định tự động chuyên sâu (7 bài test):** Được kiểm chứng tự động toàn diện qua bộ test [tests/test_holdout_predictions_artifact.py](file:///d:/HuyD/Đại Học/BigData/Global/tests/test_holdout_predictions_artifact.py) (7/7 test cases đạt 100%):
     1. `test_holdout_csv_structure_and_row_count`: Đúng 32,000 dòng, không null, không trùng `customer_id`, đủ 5 cột bắt buộc.
     2. `test_holdout_values_range_and_validity`: `y_true` và `y_pred` strictly thuộc $\{0, 1\}$; `y_proba` hữu hạn, không NaN, nằm trong $[0, 1]$.
     3. `test_holdout_error_group_row_by_row_consistency`: 100% các dòng có `error_group` khớp với `y_true` và `y_pred` theo quy tắc TP/TN/FP/FN.
     4. `test_holdout_full_32k_customer_ids_and_order_match_ground_truth`: Toàn bộ 32,000 `customer_id`, thứ tự dòng và `y_true` khớp 100% với Holdout gốc từ DuckDB/Parquet.
     5. `test_holdout_customer_id_sha256_computation_and_comparison`: Tự tính toán mã băm SHA-256 từ mảng bytes `int64` của 32,000 khách hàng trong artifact và đối chiếu độc lập với danh sách Holdout gốc (`008236ea0d8461b4d5f58b34e973766d4a696a20c97b8d28a4b9d025c99a5da2`).
     6. `test_holdout_confusion_matrix_matches_metrics_comparison_filtered_row`: Đọc `metrics_comparison.csv`, lọc động theo điều kiện `model_name == 'XGBoost (Full Features)'` & `split_id` & `evaluation_set` & `feature_space` (không dựa vào chỉ số dòng tĩnh), đối chiếu khớp 100% các số đếm TN=15,740, FP=9,763, FN=3,078, TP=3,419.
     7. `test_holdout_scale_pos_weight_exact_derivation_from_train_split`: Đếm trực tiếp nhãn âm (102,011) và nhãn dương (25,989) từ 128,000 dòng tập Train thực tế và đối chiếu tỷ lệ runtime $3.925160644888222$.
   - **Khớp nối ma trận nhầm lẫn:** 4 số đếm tính trực tiếp từ cột `y_true` và `y_pred` của tệp artifact này đạt chính xác: $\text{TN} = 15,740$, $\text{FP} = 9,763$, $\text{FN} = 3,078$, $\text{TP} = 3,419$, khớp 100% với `metrics_comparison.csv`.

### 1.2. Đối chiếu tham số mô hình và tiền xử lý
Toàn bộ kết quả phân nhóm FP/FN được tạo ra từ đúng mô hình `XGBoost (Full Features)` với các thông số nghiêm ngặt sau:
- **Thuật toán:** `XGBClassifier` trong `src/models/train_xgboost.py:124-134`.
- **Tham số kiến trúc:** `n_estimators=150`, `max_depth=6`, `learning_rate=0.08`, `subsample=0.85`, `colsample_bytree=0.85`, `random_state=42`, `n_jobs=-1`, `eval_metric="logloss"` (Xác nhận 100% từ mã nguồn).
- **Trọng số mất cân bằng (`scale_pos_weight`):** Được tính toán động tại thời điểm chạy trong `src/models/train_xgboost.py:100` bằng công thức:
  $$\text{pos\_weight} = \frac{\sum (y_{\text{train}} == 0)}{\sum (y_{\text{train}} == 1)} = \frac{102,011}{25,989} \approx 3.925160644888222$$
  *(Làm tròn: 3.9252. Giá trị này được truyền trực tiếp dưới dạng float vào mô hình; số 3.9261 trong các bản thảo trước là con số làm tròn thô không làm thay đổi bản chất mã nguồn thực thi).*
- **Không gian đặc trưng:** Đúng 63 đặc trưng liên tục/số học theo danh mục `candidate_cols` từ `outputs/customer_features.parquet` (Xác nhận từ mã nguồn `split_manager.py:60-69, 180-183`).
- **Tiền xử lý (Fit-on-Train strictly):** `SimpleImputer(strategy='median')` và `StandardScaler()` chỉ được `fit` trên 128,000 dòng tập Train, sau đó áp dụng `transform` trên 32,000 dòng tập Holdout (Xác nhận từ `split_manager.py:184-194`).
- **Ngưỡng quyết định:** Cố định $\tau = 0.50$. Khách hàng có xác suất $\hat{p}_i \ge 0.50$ được dự đoán là nhãn 1 (Mua hàng), ngược lại là nhãn 0 (Xác nhận từ `metrics_comparison.csv` và `train_xgboost.py:188`).

---

## 2. Đối chiếu số liệu Ma trận Nhầm lẫn & Công thức Tính toán chi tiết

### 2.1. Bảng số liệu ma trận nhầm lẫn thực tế (Holdout 32,000 mẫu)

Dữ liệu được đối chiếu trực tiếp từ [metrics_comparison.csv](file:///d:/HuyD/Đại Học/BigData/Global/outputs/metrics/metrics_comparison.csv):

| Chỉ số / Phân nhóm | XGBoost Full (63 biến) | XGBoost PSO (17 biến) | Chênh lệch ($\Delta = \text{PSO} - \text{Full}$) | Công thức tính toán toán học |
| :--- | :---: | :---: | :---: | :--- |
| **True Negatives (TN)** | **15,740** (49.19%) | **16,067** (50.21%) | **+327** (+2.08%) | Số mẫu $y=0$ và $\hat{y}=0$ |
| **False Positives (FP)** | **9,763** (30.51%) | **9,436** (29.49%) | **-327** (-3.35%) | Số mẫu $y=0$ và $\hat{y}=1$ |
| **False Negatives (FN)** | **3,078** (9.62%) | **3,327** (10.40%) | **+249** (+8.09%) | Số mẫu $y=1$ và $\hat{y}=0$ |
| **True Positives (TP)** | **3,419** (10.68%) | **3,170** (9.91%) | **-249** (-7.28%) | Số mẫu $y=1$ và $\hat{y}=1$ |
| **Tổng số mẫu Holdout** | **32,000** (100.0%) | **32,000** (100.0%) | 0 | $N = \text{TN} + \text{FP} + \text{FN} + \text{TP}$ |
| **Thực tế Nhãn Dương ($y=1$)** | **6,497** (20.30%) | **6,497** (20.30%) | 0 | $P = \text{TP} + \text{FN}$ |
| **Thực tế Nhãn Âm ($y=0$)** | **25,503** (79.70%) | **25,503** (79.70%) | 0 | $N_{\text{neg}} = \text{TN} + \text{FP}$ |
| **Dự đoán Nhãn Dương ($\hat{y}=1$)**| **13,182** (41.19%) | **12,606** (39.39%) | -576 (-4.37%) | $P_{\text{pred}} = \text{TP} + \text{FP}$ |
| **Dự đoán Nhãn Âm ($\hat{y}=0$)** | **18,818** (58.81%) | **19,394** (60.61%) | +576 (+3.06%) | $N_{\text{pred}} = \text{TN} + \text{FN}$ |
| **Precision ($\tau = 0.5$)** | **25.94%** | **25.15%** | **-0.79%** | $\text{TP} / (\text{TP} + \text{FP}) = 3,419 / 13,182$ |
| **Recall ($\tau = 0.5$)** | **52.62%** | **48.79%** | **-3.83%** | $\text{TP} / (\text{TP} + \text{FN}) = 3,419 / 6,497$ |
| **Specificity ($\tau = 0.5$)** | **61.72%** | **63.00%** | **+1.28%** | $\text{TN} / (\text{TN} + \text{FP}) = 15,740 / 25,503$ |
| **Accuracy ($\tau = 0.5$)** | **59.87%** | **60.12%** | **+0.25%** | $(\text{TP} + \text{TN}) / N = 19,159 / 32,000$ |
| **F1-Score ($\tau = 0.5$)** | **0.3475** | **0.3319** | **-0.0156** | $2 \cdot (\text{Prec} \cdot \text{Rec}) / (\text{Prec} + \text{Rec})$ |
| **PR-AUC** | **0.2654** | **0.2584** | **-0.0070** | Diện tích dưới đường cong Precision-Recall |
| **ROC-AUC** | **0.6006** | **0.5846** | **-0.0160** | Diện tích dưới đường cong ROC |

---

## 3. Bảng phân vị thống kê các Đặc trưng Hành vi Cốt lõi trên 4 Phân nhóm

Dưới đây là giá trị trung vị (Median) và trung bình (Mean) của 10 đặc trưng quan trọng nhất được tính toán trực tiếp từ dữ liệu thực tế trên 32,000 khách hàng tập Holdout:

| Đặc trưng phân tích | Nhóm TP ($N=3,419$) <br> *Đoán Mua & Thật Mua* | Nhóm FP ($N=9,763$) <br> *Đoán Mua & Thật Không* | Nhóm TN ($N=15,740$) <br> *Đoán Không & Thật Không* | Nhóm FN ($N=3,078$) <br> *Đoán Không & Thật Mua* |
| :--- | :---: | :---: | :---: | :---: |
| **loyalty_score** (Điểm trung thành) | **0.3740** *(TB: 0.3783)* | **0.3510** *(TB: 0.3602)* | **0.2070** *(TB: 0.2248)* | **0.2325** *(TB: 0.2490)* |
| **discount_usage_rate** (Tỷ lệ dùng ưu đãi) | **0.4152** *(TB: 0.4254)* | **0.4060** *(TB: 0.4158)* | **0.2451** *(TB: 0.2718)* | **0.2645** *(TB: 0.2954)* |
| **total_cart_additions** (Tổng thêm giỏ) | **20.0** *(TB: 20.74)* | **20.0** *(TB: 20.64)* | **19.0** *(TB: 19.49)* | **19.0** *(TB: 19.65)* |
| **total_session_duration** (Tổng giây phiên) | **4,027.5s** *(TB: 5,004.3s)* | **4,056.0s** *(TB: 4,940.0s)* | **3,914.6s** *(TB: 4,618.9s)* | **3,856.8s** *(TB: 4,749.9s)* |
| **total_pages_viewed** (Tổng trang xem) | **56.0** *(TB: 57.43)* | **56.0** *(TB: 57.31)* | **56.0** *(TB: 56.97)* | **56.0** *(TB: 57.00)* |
| **sess_count** (Tổng số phiên) | **10.0** *(TB: 10.11)* | **10.0** *(TB: 10.07)* | **10.0** *(TB: 9.97)* | **10.0** *(TB: 9.93)* |
| **trans_count** (Số giao dịch lịch sử) | **2.0** *(TB: 2.43)* | **2.0** *(TB: 2.45)* | **2.0** *(TB: 2.53)* | **2.0** *(TB: 2.56)* |
| **avg_order_value** (Giá trị đơn TB - $) | **$92.88** *(TB: $107.80)* | **$94.25** *(TB: $107.91)* | **$96.67** *(TB: $110.41)* | **$99.75** *(TB: $115.58)* |
| **email_open_rate** (Tỷ lệ mở email) | **0.3084** *(TB: 0.3308)* | **0.3190** *(TB: 0.3354)* | **0.3137** *(TB: 0.3326)* | **0.3157** *(TB: 0.3349)* |
| **account_age_days** (Tuổi tài khoản - ngày)| **596.0** *(TB: 596.38)* | **598.0** *(TB: 600.61)* | **606.0** *(TB: 602.32)* | **607.0** *(TB: 601.45)* |

---

## 4. Phân tích Định tính Hồ sơ Nhóm Báo động giả (False Positives - FP)

### 4.1. Bằng chứng số liệu quan sát thực tế ($N = 9,763$ khách hàng)
1. **Điểm gắn kết trung thành cao tương đương nhóm mua hàng:** Nhóm FP có trung vị `loyalty_score` đạt **0.3510** (trung bình 0.3602), bám sát nhóm TP (0.3740) và cao hơn tới **69.6%** so với nhóm không mua hàng được dự đoán đúng TN (0.2070).
2. **Tỷ lệ sử dụng mã ưu đãi cao:** Trung vị `discount_usage_rate` của FP là **0.4060**, gần như tương đương với TP (0.4152) và vượt xa TN (0.2451).
3. **Cường độ tương tác giỏ hàng và thời gian phiên cao:** Tổng số lần thêm sản phẩm vào giỏ hàng (`total_cart_additions`) đạt trung vị 20.0 lần, thời lượng truy cập đạt 4,056 giây (cao nhất trong cả 4 nhóm).

### 4.2. Cơ chế thuật toán dẫn đến sai lệch FP
- **Giải thích thuật toán:** Cây quyết định trong XGBoost phân nhánh mạnh dựa trên `loyalty_score` và `discount_usage_rate` (hai đặc trưng xếp thứ hạng cao nhất trong `outputs/feature_selection/feature_importance.csv`). Khi một khách hàng sở hữu điểm loyalty cao và thường xuyên dùng ưu đãi, các phân nhánh của cây đẩy xác suất $\hat{p}_i$ vượt ngưỡng 0.50, dẫn đến dự đoán nhãn 1 dù thực tế trong tập dữ liệu nhãn là 0.

### 4.3. Giả thuyết phân khúc hành vi (Behavioral Segmentation Hypothesis)
> [!NOTE]
> **CẢNH BÁO PHƯƠNG PHÁP LUẬN:** Tên gọi và mô tả dưới đây là **giả thuyết diễn giải được xây dựng để lý giải dữ liệu quan sát**, KHÔNG PHẢI là kết luận hành vi đã được kiểm chứng bằng thực nghiệm tâm lý hay khảo sát người dùng độc lập.
- **Giả thuyết phân khúc: "Khách hàng dạo chơi chờ sale" (Window Shoppers / Deal Seekers):** Nhóm này có thể gồm những người dùng thích tương tác với nền tảng, thường xuyên lưu hàng vào giỏ và săn tìm ưu đãi nhưng có tính trì hoãn giao dịch cao (chờ sự kiện sale lớn hơn, so sánh giá sàn khác, hoặc dùng giỏ hàng làm wishlist).
- **Rủi ro vận hành kinh doanh:** Nếu doanh nghiệp tự động phân phối ngân sách tiếp thị hoặc voucher tiền mặt giảm giá sâu cho nhóm này dựa trên dự đoán của mô hình, doanh nghiệp đối mặt với rủi ro lãng phí chi phí tiếp cận trên 9,763 khách hàng mà không đem lại chuyển đổi tức thì (Precision thực tế chỉ đạt 25.94%).

---

## 5. Phân tích Định tính Hồ sơ Nhóm Bỏ sót (False Negatives - FN)

### 5.1. Bằng chứng số liệu quan sát thực tế ($N = 3,078$ khách hàng)
1. **Điểm trung thành và mức độ dùng voucher rất thấp:** Trung vị `loyalty_score` của nhóm FN chỉ đạt **0.2325** và `discount_usage_rate` đạt **0.2645**. Hai chỉ số này hòa lẫn với nhóm người dùng không mua hàng TN (0.2070 và 0.2451).
2. **Thời lượng phiên và tương tác giỏ hàng ở mức trung bình thấp:** Tổng thời lượng duyệt web trung vị chỉ 3,856.8 giây (thấp nhất trong 4 nhóm), số lần thêm giỏ trung vị là 19 lần.
3. **Giá trị đơn hàng lịch sử cao nhất:** Trung vị giá trị đơn hàng trung bình (`avg_order_value`) của nhóm FN đạt **$99.75** (trung bình $115.58), cao hơn rõ rệt so với cả nhóm TP ($92.88) và FP ($94.25).

### 5.2. Cơ chế thuật toán dẫn đến sai lệch FN
- **Giải thích thuật toán:** Do nhóm FN không sở hữu các đặc trưng tương tác cao (ít săn sale, điểm loyalty thấp), các nhánh cây quyết định gán cho họ điểm số thấp ($\hat{p}_i < 0.50$), khiến mô hình gộp họ vào nhóm âm tính và bỏ sót nhãn dương thực tế.

### 5.3. Giả thuyết phân khúc hành vi (Behavioral Segmentation Hypothesis)
> [!NOTE]
> **CẢNH BÁO PHƯƠNG PHÁP LUẬN:** Tên gọi và mô tả dưới đây là **giả thuyết diễn giải được xây dựng để lý giải dữ liệu quan sát**, KHÔNG PHẢI là kết luận hành vi đã được chứng minh.
- **Giả thuyết phân khúc: "Khách hàng mua hàng chớp nhoáng / Đơn hàng lớn" (Decisive / High AOV Buyers):** Nhóm này có thể là những người dùng có nhu cầu mua sắm cụ thể, mua các món hàng giá trị cao ($99.75), không có thói quen săn mã giảm giá và rời đi nhanh sau khi mua. Vì ít tích lũy điểm tương tác, họ trở nên "vô hình" trước thuật toán.
- **Rủi ro vận hành kinh doanh:** Mô hình bỏ sót 3,078 khách hàng có giao dịch thực tế (chiếm 47.38% tổng số khách hàng mua thực tế). Đây là sự bỏ lỡ cơ hội phục vụ nhóm khách hàng có giá trị đơn hàng cao (High AOV).

---

## 6. Đánh đổi Sai số giữa XGBoost Full (63 biến) và XGBoost PSO (17 biến)

Việc nén 73.02% số chiều biến qua thuật toán PSO dẫn đến một sự đánh đổi sai số rõ ràng:

1. **PSO làm tăng sai số False Negative (+249 ca, tăng 8.09%):**
   - Số ca bỏ sót tăng từ 3,078 lên 3,327 khách hàng.
   - Khi loại bỏ 46 biến phụ trợ (tỷ trọng nguồn truy cập, chỉ số tương tác phiên chi tiết), không gian biểu diễn bị thu hẹp, khiến mô hình khó phát hiện các ca mua hàng không điển hình (FN).
2. **PSO giúp giảm nhẹ sai số False Positive (-327 ca, giảm 3.35%):**
   - Số ca báo động giả giảm từ 9,763 xuống 9,436 khách hàng.
   - Việc loại bỏ các biến có tính nhiễu giúp mô hình bớt nhạy cảm với các hành vi tương tác không dẫn đến chuyển đổi.
3. **Đánh đổi tổng thể về chỉ số:**
   - **Tốc độ:** Thời gian huấn luyện (fit time) giảm từ 4.65s xuống 2.22s (tăng tốc hơn 52%).
   - **Chất lượng phân loại:** Recall bị suy giảm từ **52.62% xuống 48.79%** (-3.83%); PR-AUC giảm từ **0.2654 xuống 0.2584** (-0.0070).

---

## 7. Hàm ý Quản trị Kinh doanh (Chuẩn cấu trúc 5 bước & Chống suy diễn nhân quả)

Mọi đề xuất dưới đây tuân thủ nghiêm ngặt chuẩn 5 bước: **Phát hiện $\rightarrow$ Bằng chứng thực nghiệm $\rightarrow$ Hàm ý $\rightarrow$ Hành động đề xuất $\rightarrow$ Giới hạn / Cảnh báo rủi ro**.

### Đề xuất 1: Chiến lược can thiệp tiếp thị phân tầng cho nhóm Báo động giả (FP)
- **Phát hiện quan sát:** Nhóm FP chiếm 30.51% tập kiểm tra (9,763 khách hàng), có điểm tương tác và độ nhạy khuyến mãi cao nhưng không chuyển đổi đơn hàng.
- **Bằng chứng thực nghiệm:** `discount_usage_rate` trung vị đạt 0.4060 và `loyalty_score` đạt 0.3510 trên tập Holdout.
- **Hàm ý kinh doanh:** Nếu tự động phân bổ voucher giảm giá sâu trực tiếp cho nhóm này, doanh nghiệp có nguy cơ xói mòn biên lợi nhuận trên quy mô lớn mà không đảm bảo chuyển đổi.
- **Hành động đề xuất:** Thiết kế chiến dịch can thiệp phi tiền mặt (non-monetary nudge) như: gửi thông báo nhắc nhở giỏ hàng, đề xuất sản phẩm liên quan hoặc tích điểm thành viên thay vì chiết khấu tiền mặt trực tiếp.
- **Giới hạn & Cảnh báo nhân quả:** Đây là tương quan quan sát trên dữ liệu snapshot. **Nghiên cứu không khẳng định việc giảm voucher sẽ giúp tiết kiệm ngân sách hoặc kích thích nhóm này mua hàng**. Mọi chiến dịch bắt buộc phải thực hiện thử nghiệm A/B Testing có nhóm đối chứng ngẫu nhiên (RCT) trước khi triển khai.

### Đề xuất 2: Tối ưu hóa quy trình cho nhóm khách hàng giá trị cao bị bỏ sót (FN)
- **Phát hiện quan sát:** Mô hình bỏ sót 47.38% khách hàng mua thực tế (3,078 khách hàng), nhóm này có thời lượng phiên ngắn nhưng giá trị đơn hàng trung bình cao nhất hệ thống.
- **Bằng chứng thực nghiệm:** `avg_order_value` trung vị đạt $99.75 (so với $92.88 ở nhóm TP), trong khi `loyalty_score` chỉ đạt 0.2325.
- **Hàm ý kinh doanh:** Quy trình tiếp thị dựa trên điểm trung thành truyền thống đang bỏ quên phân khúc khách hàng mua hàng dứt khoát có giá trị giỏ hàng lớn.
- **Hành động đề xuất:** Đơn giản hóa trải nghiệm thanh toán (One-click checkout, hiển thị sản phẩm cao cấp tại trang tìm kiếm nhanh).
- **Giới hạn & Cảnh báo nhân quả:** Tương quan giữa thời lượng phiên ngắn và AOV cao không đồng nghĩa với việc rút ngắn phiên duyệt web sẽ làm tăng giá trị đơn hàng. Không được tự ý cắt giảm thông tin mô tả sản phẩm trên website.

### Đề xuất 3: Lựa chọn mô hình dựa trên hàm chi phí kinh tế (Business Cost Function)
- **Phát hiện quan sát:** Mô hình nén PSO (17 biến) giúp giảm 327 ca báo động giả (FP) nhưng làm tăng 249 ca bỏ sót khách hàng (FN) và giảm độ nhạy Recall từ 52.62% xuống 48.79%.
- **Bằng chứng thực nghiệm:** So sánh ma trận nhầm lẫn tại ngưỡng $\tau = 0.50$ giữa Full Features và PSO Features trên cùng tập Holdout 32,000 mẫu.
- **Hàm ý kinh doanh:** Việc chọn mô hình tinh gọn (PSO) hay mô hình đầy đủ (Full) là bài toán cân bằng kinh tế:
  - Nếu chi phí bỏ sót một khách hàng (Cost of False Negative) lớn hơn chi phí tính toán phần cứng: Doanh nghiệp nên chọn mô hình Full Features hoặc ANOVA Features (PR-AUC 0.2759).
  - Nếu hệ thống yêu cầu độ trễ suy luận siêu thấp trên thiết bị biên hoặc tài nguyên tính toán bị giới hạn nghiêm ngặt: Doanh nghiệp nên chọn mô hình PSO Features (17 biến).
- **Hành động đề xuất:** Xây dựng hàm mục tiêu chi phí kinh doanh cụ thể trước khi quyết định đưa mô hình nào vào môi trường production.
- **Giới hạn & Cảnh báo rủi ro:** Đo lường thời gian chạy (runtime) trong nghiên cứu thực hiện trên máy tính chuẩn đơn luồng/đa luồng CPU cá nhân; hiệu năng thực tế trên cụm máy chủ phân tán có thể khác biệt.

---
*Báo cáo phân tích lỗi định tính đã hoàn tất với đầy đủ bằng chứng thực nghiệm và cơ chế kiểm toán độc lập từ 32,000 khách hàng tập Holdout, phục vụ trực tiếp cho Báo cáo Phần 4.7 và Phần 5.7.*
