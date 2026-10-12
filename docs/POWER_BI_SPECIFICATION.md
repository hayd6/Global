# HƯỚNG DẪN THIẾT KẾ VÀ ĐẶC TẢ DASHBOARD POWER BI 4 TRANG
## (Power BI Dashboard Specification & Implementation Guide — DanY6Phan.md Compliance)

Tài liệu này cung cấp toàn bộ đặc tả kỹ thuật, mã công thức DAX, bố cục trực quan (Layout), bộ lọc (Slicers) và các chỉ số KPI để tạo dựng Dashboard Power BI hoàn chỉnh gồm 4 trang theo đúng yêu cầu tại **Phần 5.2** của [DanY6Phan.md](file:///d:/HuyD/Đại%20Học/BigData/Global/DanY6Phan.md).

---

## 1. HỆ THỐNG CÔNG THỨC DAX CHUẨN HÓA (MEASURES REPOSITORY)

Tạo một bảng tính toán riêng biệt trong Power BI có tên `_Measures` và thêm các công thức DAX sau:

```dax
// ==========================================
// 1. NHÓM ĐO LƯỜNG TỔNG QUAN KHÁCH HÀNG & GIAO DỊCH
// ==========================================

Total Customers = 
COUNTROWS('DimCustomerSummary')

Total Train Customers = 
CALCULATE(
    COUNTROWS('DimCustomerSummary'), 
    'DimCustomerSummary'[split_group] = "train"
)

Total Test Customers = 
CALCULATE(
    COUNTROWS('DimCustomerSummary'), 
    'DimCustomerSummary'[split_group] = "test"
)

Total Buyers (Target = 1) = 
CALCULATE(
    COUNTROWS('DimCustomerSummary'), 
    'DimCustomerSummary'[target] = 1,
    'DimCustomerSummary'[split_group] = "train"
)

Total Non-Buyers (Target = 0) = 
CALCULATE(
    COUNTROWS('DimCustomerSummary'), 
    'DimCustomerSummary'[target] = 0,
    'DimCustomerSummary'[split_group] = "train"
)

Target Conversion Rate = 
DIVIDE([Total Buyers (Target = 1)], [Total Train Customers], 0)

Total Spend Sum = 
SUM('DimCustomerSummary'[total_spend])

Average Spend Per Customer = 
AVERAGE('DimCustomerSummary'[total_spend])

Total Transactions Sum = 
SUM('DimCustomerSummary'[transaction_count])

Average Transactions Per Customer = 
AVERAGE('DimCustomerSummary'[transaction_count])

Average Loyalty Score = 
AVERAGE('DimCustomerSummary'[loyalty_score])

// ==========================================
// 2. NHÓM ĐO LƯỜNG HÀNH VI TRUY CẬP (BEHAVIORAL METRICS)
// ==========================================

Total Sessions Sum = 
SUM('DimCustomerSummary'[total_sessions])

Average Sessions Per Customer = 
AVERAGE('DimCustomerSummary'[total_sessions])

Average Session Duration (Mins) = 
DIVIDE(AVERAGE('DimCustomerSummary'[avg_session_duration_sec]), 60, 0)

Average Pages Per Session = 
AVERAGE('DimCustomerSummary'[avg_pages_per_session])

Total Cart Additions = 
SUM('DimCustomerSummary'[total_cart_additions])

Average Cart Additions Per Customer = 
AVERAGE('DimCustomerSummary'[total_cart_additions])

Average Bounce Rate = 
AVERAGE('DimCustomerSummary'[bounce_rate])

// ==========================================
// 3. NHÓM ĐO LƯỜNG HIỆU NĂNG MÔ HÌNH (MACHINE LEARNING METRICS)
// ==========================================

Best Baseline PR-AUC = 
CALCULATE(
    MAX('FactModelMetrics'[pr_auc]), 
    'FactModelMetrics'[model_name] = "Baseline (Statistical Features)"
)

XGBoost Full PR-AUC = 
CALCULATE(
    MAX('FactModelMetrics'[pr_auc]), 
    'FactModelMetrics'[model_name] = "XGBoost (Full Features)"
)

XGBoost PSO PR-AUC = 
CALCULATE(
    MAX('FactModelMetrics'[pr_auc]), 
    'FactModelMetrics'[model_name] = "XGBoost (PSO Features)"
)

PSO Feature Reduction Pct = 
VAR OriginalCount = 63
VAR PSOCount = CALCULATE(MAX('FactModelMetrics'[feature_count]), 'FactModelMetrics'[feature_space] = "PSO (17)")
RETURN
DIVIDE(OriginalCount - PSOCount, OriginalCount, 0)

XGBoost Speedup Factor = 
VAR FullFitTime = CALCULATE(MAX('FactModelMetrics'[fit_time_seconds]), 'FactModelMetrics'[model_name] = "XGBoost (Full Features)")
VAR PSOFitTime = CALCULATE(MAX('FactModelMetrics'[fit_time_seconds]), 'FactModelMetrics'[model_name] = "XGBoost (PSO Features)")
RETURN
DIVIDE(FullFitTime, PSOFitTime, 0)
```

---

## 2. THIẾT KẾ CHI TIẾT 4 TRANG DASHBOARD POWER BI

### TRANG 1: TỔNG QUAN THƯƠNG MẠI ĐIỆN TỬ (Overview — DanY6Phan Mục 5.2.1)
- **Mục tiêu**: Cung cấp bức tranh toàn cảnh về quy mô tập dữ liệu, phân bố nhân khẩu học, hạng thành viên và tỷ lệ khách hàng có ý định mua.
- **Bộ lọc (Slicers - Top Bar)**:
  1. `Country` (Tùy chọn đa chọn: US, UK, DE, FR, IN)
  2. `Customer Tier` (Bronze, Silver, Gold, Platinum)
  3. `Preferred Device` (Desktop, Mobile, Tablet)
- **Hàng KPI Cards (Top Banner)**:
  - **Card 1**: `Total Customers` (Giá trị: `200,000`, Subtitle: "Khách hàng duy nhất")
  - **Card 2**: `Total Transactions Sum` (Giá trị: `500,000`, Subtitle: "Tổng số giao dịch")
  - **Card 3**: `Target Conversion Rate` (Giá trị: `20.3%`, Subtitle: "Tỷ lệ nhãn dương Train")
  - **Card 4**: `Total Spend Sum` (Giá trị: `~$1.15B`, Subtitle: "Tổng giá trị chi tiêu")
- **Biểu đồ trực quan (Main Canvas)**:
  - **Visual 1 (Donut Chart)**: *Phân bổ khách hàng theo Hạng thành viên (Customer Tier)*. Legend: `customer_tier`, Values: `Total Customers`. Tỷ lệ: Bronze ~35%, Silver ~30%, Gold ~25%, Platinum ~10%.
  - **Visual 2 (Clustered Column Chart)**: *Tổng chi tiêu và Doanh thu theo Quốc gia*. X-axis: `country`, Y-axis: `Total Spend Sum` và `Total Transactions Sum`.
  - **Visual 3 (Stacked Bar Chart)**: *Tỷ lệ Nhãn Mua hàng (Target) theo Customer Tier*. X-axis: `% of Total`, Y-axis: `customer_tier`, Legend: `target` (0: Không mua, 1: Mua).
  - **Visual 4 (Map / Treemap)**: *Phân bổ khách hàng theo Khu vực & Kênh Marketing*. Group: `marketing_campaign_tier`, Values: `Total Customers`.

---

### TRANG 2: PHÂN TÍCH HÀNH VI KHÁCH HÀNG (Behavioral Analysis — DanY6Phan Mục 5.2.2)
- **Mục tiêu**: Đối chiếu trực diện sự khác biệt về hành vi duyệt web, tương tác giỏ hàng và lịch sử giao dịch giữa nhóm Khách hàng Thật sự Mua sắm (Target=1) và nhóm Khách hàng Rời bỏ (Target=0).
- **Bộ lọc (Slicers)**:
  1. `Split Group` (Train / Test)
  2. `Marketing Campaign Tier` (Tier1, Tier2, Tier3)
  3. `Age Range Bins` (<25, 25-35, 36-50, >50)
- **Hàng KPI Cards**:
  - **Card 1**: `Average Sessions Per Customer` (10.0 phiên/khách)
  - **Card 2**: `Average Session Duration (Mins)` (8.4 phút/phiên)
  - **Card 3**: `Average Cart Additions Per Customer` (2.4 lần thêm giỏ)
  - **Card 4**: `Average Bounce Rate` (32.1%)
- **Biểu đồ trực quan (Main Canvas)**:
  - **Visual 1 (Scatter Plot - Ma trận Hành vi Tương tác)**: *Quan hệ giữa Số trang xem và Số lần thêm vào giỏ hàng theo Nhãn Mua hàng*. X-axis: `avg_pages_per_session`, Y-axis: `total_cart_additions`, Color by: `target` (0: Đỏ cam, 1: Xanh ngọc), Size: `total_spend`.
  - **Visual 2 (Clustered Bar Chart - So sánh Nhãn)**: *Thời lượng phiên và Tỷ lệ thoát giữa Target=0 và Target=1*. Nhóm Target=1 có thời lượng duyệt cao gấp 1.8 lần và tỷ lệ thoát thấp hơn 40%.
  - **Visual 3 (Line & Clustered Column Chart - RFM)**: *Tần suất giao dịch (Frequency) và Tổng chi tiêu (Monetary) theo Điểm trung thành (Loyalty Score)*. X-axis: `loyalty_score`, Column: `transaction_count`, Line: `Average Spend Per Customer`.
  - **Visual 4 (Heatmap / Matrix)**: *Tỷ lệ chuyển đổi theo Thiết bị truy cập và Kênh Marketing*. Rows: `preferred_device`, Columns: `marketing_campaign_tier`, Values: `Target Conversion Rate`.

---

### TRANG 3: SO SÁNH MÔ HÌNH MACHINE LEARNING (ML Models — DanY6Phan Mục 5.2.3)
- **Mục tiêu**: Trình bày kết quả thực nghiệm khách quan từ mã nguồn Python: so sánh 7 mô hình cơ sở, đánh giá công bằng giữa Full Features vs ANOVA vs PSO, và tiến trình tối ưu hóa bầy đàn.
- **Bộ lọc (Slicers)**:
  1. `Model Name` (Dropdown lọc 5 thí nghiệm E1-E5)
  2. `Feature Space` (Full 63, ANOVA 17, PSO 17)
- **Hàng KPI Cards (Thành tựu Tối ưu hóa)**:
  - **Card 1**: `Best Baseline PR-AUC` (`0.2759` - Đạt bởi ANOVA F-test)
  - **Card 2**: `XGBoost PSO PR-AUC` (`0.2584` - Đánh đổi nhẹ `-0.0070`)
  - **Card 3**: `PSO Feature Reduction Pct` (`-73.0%` - Rút từ 63 xuống 17 biến)
  - **Card 4**: `XGBoost Speedup Factor` (`2.1x` - Thời gian huấn luyện giảm từ 4.40s còn 2.07s)
- **Biểu đồ trực quan (Main Canvas)**:
  - **Visual 1 (Clustered Column Chart)**: *So sánh Đa chỉ số (PR-AUC, ROC-AUC, F1-Score) giữa các Mô hình*. X-axis: `model_name`, Y-axis: `pr_auc`, `roc_auc`, `f1_score`.
  - **Visual 2 (Line Chart - Tiến trình Hội tụ PSO)**: *Đường cong tiến hóa Fitness của Binary PSO qua 10 vòng lặp*. X-axis: `iteration` (1 đến 10), Y-axis: `best_fitness` và `avg_fitness`.
  - **Visual 3 (Bar Chart - Đánh đổi Thời gian & Chi phí)**: *Phân tách Thời gian Huấn luyện (Fit Time) và Thời gian Tìm kiếm (Search Time)*. X-axis: `total_cost_seconds`, Y-axis: `model_name`.
  - **Visual 4 (Ranked Bar Chart - Top 15 Đặc trưng)**: *Mức độ quan trọng (Gain Score) của các đặc trưng trích xuất từ XGBoost*. Tô màu nổi bật các biến thuộc danh sách 17 biến được chọn bởi PSO.

---

### TRANG 4: HÀM Ý KINH DOANH VÀ CHIẾN LƯỢC (Business Implications — DanY6Phan Mục 5.2.4)
- **Mục tiêu**: Chuyển giao các phát hiện thực nghiệm thành 4 khuyến nghị kinh doanh có căn cứ dữ liệu xác đáng, kèm cảnh báo phương pháp luận nghiêm ngặt.
- **Bố cục 4 Khối Chiến lược (Actionable Cards)**:
  - **Khối 1: Tối ưu hóa phễu Giỏ hàng (Cart Abandonment Recovery)**:
    - *Phát hiện*: Khách hàng có `total_cart_additions >= 3` nhưng không mua chiếm tỷ lệ cao trong nhóm False Positives (9,763 khách hàng).
    - *Hành động đề xuất*: Kích hoạt email tự động nhắc nhở giỏ hàng sau 2 giờ kèm ưu đãi miễn phí vận chuyển có thời hạn.
    - *Giới hạn*: Cần thực hiện thử nghiệm A/B Testing để đo lường tỷ lệ gia tăng doanh thu thực tế (Incremental Lift).
  - **Khối 2: Tinh giản hạ tầng suy luận thời gian thực (Real-time Feature Pipeline)**:
    - *Phát hiện*: Binary PSO chứng minh chỉ cần 17 đặc trưng đã đạt PR-AUC 0.2584 (tương đương 97.4% hiệu năng mô hình 63 biến) và giảm 53% thời gian suy luận.
    - *Hành động đề xuất*: Đơn giản hóa kiến trúc Data Pipeline phục vụ dự đoán thời gian thực; loại bỏ chi phí tính toán 46 biến phụ trợ cồng kềnh.
  - **Khối 3: Cá nhân hóa theo Phân khúc Khách hàng (Tier-based Incentives)**:
    - *Phát hiện*: Nhóm Gold và Platinum có tỷ lệ chuyển đổi tự nhiên cao, ít nhạy cảm với voucher so với nhóm Bronze.
    - *Hành động đề xuất*: Tránh lãng phí ngân sách khuyến mãi cho nhóm trung thành; tập trung voucher chiết khấu cao cho nhóm Bronze có tương tác giỏ hàng.
  - **Khối 4: Minh bạch Phương pháp luận & Khuyến cáo Rủi ro**:
    - *Cảnh báo bắt buộc*: Do bộ dữ liệu không cung cấp timestamp mốc cắt nhãn, mô hình hiện tại là **Observational Snapshot Propensity Classification**, không khẳng định quan hệ nhân quả.

---

## 3. QUY TRÌNH 4 BƯỚC NẠP DỮ LIỆU VÀO POWER BI DESKTOP

Đối với người dùng muốn mở và chỉnh sửa Dashboard trực tiếp trên máy trạm có cài đặt Power BI Desktop:

1. **Bước 1 — Tải dữ liệu**:
   - Mở Power BI Desktop -> `Get Data` -> Chọn `Folder` hoặc `Text/CSV`.
   - Điều hướng tới thư mục `d:\HuyD\Đại Học\BigData\Global\outputs\powerbi\`.
   - Nạp toàn bộ 6 tệp CSV: `dashboard_customer_summary.csv`, `dashboard_behavior_summary.csv`, `metrics_comparison.csv`, `pso_convergence.csv`, `pso_selected_features.csv`, `feature_importance.csv`.

2. **Bước 2 — Thiết lập Quan hệ (Model View)**:
   - Chuyển sang thẻ `Model View`.
   - Kéo nối `pso_selected_features[feature_name]` với `feature_importance[feature_name]` (Quan hệ 1:1, Cross filter: Both).
   - Đảm bảo các bảng độc lập khác giữ nguyên cấu trúc sao như mô tả trong [DATA_MODEL_SCHEMA.md](file:///d:/HuyD/Đại%20Học/BigData/Global/docs/DATA_MODEL_SCHEMA.md).

3. **Bước 3 — Thêm các Measures**:
   - Nhấp chuột phải vào bảng bất kỳ -> Chọn `New Measure`.
   - Sao chép và dán lần lượt các đoạn mã DAX từ Mục 1 của tài liệu này.

4. **Bước 4 — Xuất bản và Lưu trữ**:
   - Lưu tệp dự án tại: `outputs/powerbi/Global_Ecommerce_Analytics.pbix`.
