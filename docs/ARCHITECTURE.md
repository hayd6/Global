# ARCHITECTURE & PIPELINE DESIGN

Tài liệu này mô tả kiến trúc hệ thống và luồng xử lý toàn diện của dự án **Global E-Commerce Customer Purchase Prediction**.

---

## 1. Sơ đồ kiến trúc tổng thể (Mermaid Architecture Diagram)

```mermaid
flowchart TD
    subgraph DataSources["1. Nguồn Dữ Liệu (dataset/ - READ ONLY)"]
        Customers["customers.csv (200k)"]
        Sessions["sessions.csv (2M)"]
        Transactions["transactions.csv (500k)"]
        Geo["geo_data.csv (100)"]
        Campaigns["marketing_campaigns.csv (200)"]
        Train["train.csv (160k)"]
        Test["test.csv (40k)"]
    end

    subgraph Phase1_2["2. Data Audit & DuckDB Cleaning / Integration"]
        Audit["Kiểm toán dữ liệu (inspect_data.py)<br/>Schema, Missing, Types, Duplicates"]
        CleanDuckDB["DuckDB SQL Processing (clean_data.py)<br/>- Chuẩn hóa boolean & currency<br/>- Clean 'unknown' age & 'N/A' pages"]
        AggSessions["Tổng hợp Sessions theo customer_id"]
        AggTrans["Tổng hợp Transactions theo customer_id"]
        Integrate["Tích hợp cấp khách hàng (integrate_data.py)<br/>Khách hàng + Sessions + Trans + Geo + Campaign"]
    end

    subgraph Phase3_4["3. Leakage Control, Feature Engineering & EDA"]
        LeakageAudit["Kiểm toán Target & Leakage (Giai đoạn 3)<br/>Loại ID, biến tương lai, biến nhiễu rõ ràng"]
        FeatureEngine["Trích xuất đặc trưng (build_features.py)<br/>RFM, Tương tác, Tỷ lệ thoát, Giỏ hàng, Địa lý"]
        EDA["EDA & Visualizations (eda.py)<br/>8+ biểu đồ phân tích chuyên sâu"]
    end

    subgraph Phase5_8["4. Machine Learning & Optimization Pipeline"]
        Split["Stratified Train/Val Split (80/20 trên 160k train)<br/>Độc lập Test (40k)"]
        Baselines["7 Mô hình cơ sở (baselines.py)<br/>LR, NB, DT, RF, GB, KNN, SVM"]
        StatSelect["Lựa chọn thống kê (ANOVA/Chi2/MutualInfo)"]
        PSO["Binary PSO Optimizer (pso_optimizer.py)<br/>Tối ưu hóa đa mục tiêu: PR-AUC & Độ tinh giản"]
        XGB["Huấn luyện XGBoost (train_xgboost.py)<br/>Toàn bộ đặc trưng vs Thống kê vs PSO"]
    end

    subgraph Phase9_10["5. Đánh giá & Xuất bản (outputs/)"]
        Eval["Đánh giá đa chỉ số: PR-AUC, ROC-AUC, F1, Confusion Matrix"]
        ExportPowerBI["Xuất dữ liệu Power BI / Web (export_outputs.py)"]
        Tests["Kiểm thử tự động pytest (tests/)"]
    end

    DataSources --> Phase1_2
    CleanDuckDB --> AggSessions
    CleanDuckDB --> AggTrans
    Customers --> Integrate
    AggSessions --> Integrate
    AggTrans --> Integrate
    Geo --> Integrate
    Campaigns --> Integrate

    Integrate --> Phase3_4
    FeatureEngine --> Phase5_8
    Train --> Split
    Split --> Baselines
    Split --> StatSelect
    Split --> PSO
    PSO --> XGB
    StatSelect --> XGB
    Split --> XGB

    Phase5_8 --> Phase9_10
```

---

## 2. Các thành phần hệ thống

### 2.1. Module Xử lý Dữ liệu lớn bằng DuckDB (`src/data/`)
- **Vấn đề**: `sessions.csv` có 2 triệu dòng, `transactions.csv` có 500,000 dòng. Nếu JOIN trực tiếp 2 bảng này trước khi tổng hợp, ma trận kết hợp trung gian có thể phình to lên hàng chục triệu dòng, gây tràn RAM và làm méo mó các chỉ số thống kê.
- **Giải pháp**:
  - Dùng **DuckDB** để nhóm và tổng hợp song song `sessions` theo `customer_id` (tính: tổng phiên, tổng thời lượng, tổng giỏ hàng, tỷ lệ thoát trung bình, số phiên theo nguồn truy cập...).
  - Tổng hợp `transactions` theo `customer_id` (tính: tổng số đơn, tổng giá trị, đơn hàng trung bình, phân bổ phương thức thanh toán, tỷ lệ dùng voucher...).
  - Sau đó mới kết hợp các bảng đã tổng hợp với `customers.csv` và ánh xạ `geo_data.csv` cùng `marketing_campaigns.csv`. Đảm bảo kết quả đầu ra luôn có cấu trúc **1 dòng duy nhất cho mỗi khách hàng**.

### 2.2. Kiểm soát rò rỉ dữ liệu (Anti-Leakage Design)
- **Tách biệt ID**: `customer_id`, `session_id`, `transaction_id`, `campaign_id` bị loại khỏi ma trận đặc trưng mô hình.
- **Tiền xử lý trong Pipeline**: Các bước Imputation (điền thiếu) và Scaling (chuẩn hóa) được đóng gói trong Scikit-Learn Pipeline, chỉ `fit` trên tập con huấn luyện (Train split) để ngăn ngừa hiện tượng Data Snooping / Data Leakage sang tập Validation và Test.
- **Phân tách Stratified**: Do tỷ lệ target dương là 20.3%, chiến lược chia tập đảm bảo giữ nguyên tỷ lệ nhãn dương giữa tập huấn luyện và tập kiểm định nội bộ.

### 2.3. Bộ tối ưu hóa bầy đàn nhị phân (Binary PSO)
- **Biểu diễn hạt (Particle Representation)**: Mỗi hạt là một vector nhị phân $\mathbf{x}_i \in \{0, 1\}^D$, trong đó $D$ là tổng số lượng đặc trưng ứng viên. Giá trị $1$ biểu thị đặc trưng được chọn, $0$ biểu thị đặc trưng bị loại.
- **Quy tắc cập nhật**:
  - Tốc độ: $\mathbf{v}_i^{(t+1)} = w \mathbf{v}_i^{(t)} + c_1 r_1 (\mathbf{p}_i - \mathbf{x}_i^{(t)}) + c_2 r_2 (\mathbf{g} - \mathbf{x}_i^{(t)})$
  - Chuyển đổi xác suất bằng hàm Sigmoid: $S(v_{id}) = \frac{1}{1 + e^{-v_{id}}}$
  - Vị trí nhị phân: $x_{id}^{(t+1)} = 1$ nếu $rand() < S(v_{id})$, ngược lại $0$.
- **Hàm mục tiêu (Fitness Function)**:
  $$\text{Fitness} = \alpha \cdot \text{PR-AUC} + (1 - \alpha) \cdot \left(1 - \frac{\sum x_{id}}{D}\right)$$
  với $\alpha = 0.85$ để ưu tiên tối đa chất lượng dự đoán (PR-AUC vì dữ liệu mất cân bằng) đồng thời phạt các bộ đặc trưng cồng kềnh, khuyến khích tính tinh gọn (sparsity).

### 2.4. Khung đánh giá đa chiều (Evaluation Framework)
- Không chỉ dựa vào Accuracy (dễ ngộ nhận khi nhãn mất cân bằng 80:20).
- Tập trung vào:
  1. **PR-AUC (Precision-Recall Area Under Curve)**: Thước đo quan trọng nhất cho lớp thiểu số.
  2. **ROC-AUC**: Khả năng phân loại tổng thể giữa hai lớp.
  3. **F1-Score, Precision, Recall**: Đo lường tại ngưỡng xác suất tối ưu.
  4. **Số lượng đặc trưng (Feature Sparsity)**: Đánh giá độ gọn nhẹ của mô hình.
  5. **Thời gian chạy (Training & Inference Time)**: Đánh giá tính khả thi trong sản xuất.
