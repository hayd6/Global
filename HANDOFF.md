# HANDOFF — Big Data E-commerce Purchase Prediction

> **Mục đích:** Cung cấp ngữ cảnh đầy đủ cho Codex để kiểm toán độc lập sản phẩm do AI Agent khác xây dựng trong thư mục `Global`. Codex phải kiểm tra mã nguồn, dữ liệu, thí nghiệm và đầu ra thực tế; không được mặc định rằng những gì Agent trước báo cáo đều đúng.

## 1. Vai trò của Codex

Bạn là **reviewer/QA độc lập**, không phải người viết lại dự án từ đầu.

Ưu tiên theo thứ tự:

1. Đọc file này cùng `PRD.md`, `AGENTS.md`, `README.md`, `DATA_DICTIONARY.md`, `ARCHITECTURE.md`, `EXPERIMENT_PLAN.md`, `DECISIONS.md`, `PROGRESS.md`, `REPRODUCIBILITY.md` nếu các file đó tồn tại.
2. Kiểm tra cấu trúc repository, mã nguồn, cấu hình, dữ liệu đầu vào, đầu ra đã sinh và lịch sử/ghi chú thí nghiệm.
3. Tái hiện các kiểm tra rẻ và an toàn trước; chỉ chạy lại pipeline hoặc thí nghiệm nặng khi có lý do rõ ràng.
4. Ghi nhận bằng chứng cụ thể: đường dẫn file, hàm/dòng mã nếu có, lệnh chạy, kết quả và mức độ nghiêm trọng.
5. Tạo `docs/EXPERIMENT_AUDIT.md` (hoặc cập nhật file này nếu đã có) với danh sách lỗi theo `Critical / High / Medium / Low`, đề xuất sửa chữa theo thứ tự ưu tiên và tiêu chí để xác nhận đã sửa.
6. Không âm thầm thay đổi kết quả, không bịa số liệu, không xóa đầu ra cũ trước khi lưu dấu vết. Nếu sửa mã, ghi rõ file nào đã sửa và vì sao.

Nếu không đủ bằng chứng để kết luận, ghi **Chưa xác minh** và nêu cách xác minh. Không coi `pytest` thành công là bằng chứng duy nhất cho tính hợp lệ của thí nghiệm.

## 2. Bối cảnh và mục tiêu dự án

**Tên đề tài tiếng Việt:**

“Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử.”

**Tên tiếng Anh:**

*Behavioral Feature Mining and PSO-Based Feature Selection for E-Commerce Purchase Prediction.*

Dự án thuộc học phần Big Data, hướng tới xây dựng pipeline dữ liệu và machine learning để dự đoán khả năng mua hàng của khách hàng thương mại điện tử, so sánh các mô hình baseline và khảo sát lựa chọn đặc trưng bằng Particle Swarm Optimization (PSO). Kết quả cần đủ tin cậy để giải thích trong báo cáo, thể hiện qua dashboard Power BI và có thể dùng trong website demo.

Mục tiêu không phải chứng minh PSO luôn tốt hơn. Nếu PSO giảm số đặc trưng nhưng làm giảm chất lượng dự đoán, cần báo cáo đúng trade-off đó.

## 3. Dataset và quy mô đã quan sát

Thư mục dữ liệu đầu vào: `Global/dataset/` (đường dẫn tương đối từ thư mục gốc dự án).

| File | Số dòng đã quan sát | Số cột đã quan sát | Vai trò dự kiến |
|---|---:|---:|---|
| `customers.csv` | 200,000 | 17 | Thông tin/đặc trưng khách hàng |
| `geo_data.csv` | 100 | 5 | Dữ liệu địa lý |
| `marketing_campaigns.csv` | 200,000 | 6 | Dữ liệu chiến dịch marketing |
| `sessions.csv` | 2,000,000 | 11 | Hành vi phiên truy cập |
| `transactions.csv` | 500,000 | 11 | Giao dịch |
| `train.csv` | 160,000 | 2 | Tập huấn luyện có nhãn |
| `test.csv` | 40,000 | 1 | Tập test không có nhãn |
| `sample_submission.csv` | 40,000 | 2 | Mẫu định dạng submission |

Các số liệu trên là thông tin đã quan sát trong lần chạy Agent trước; hãy xác nhận lại trên dữ liệu đang có. Không tự suy đoán schema chỉ từ tên file.

Các phát hiện sơ bộ đã ghi nhận:
- Tỷ lệ lớp dương trong `train.csv` khoảng **20.30375%**.
- ID trong train và test được báo cáo là không giao nhau; các ID này đều có trong bảng customers. Hãy kiểm chứng lại.
- Ngày trong dữ liệu đã quan sát nằm trong khoảng **2022-01-01 đến 2024-09-26**. Đây là phạm vi ngày dữ liệu, không phải ngày diễn ra cuộc thi Kaggle.
- Mô tả dataset được hiểu là dự đoán khách hàng mua hàng trong 30 ngày tiếp theo, nhưng **thời điểm chốt dữ liệu (prediction cutoff), quy tắc tạo nhãn và cách các bảng được snapshot chưa được xác minh chắc chắn**. Đây là rủi ro trọng yếu cần kiểm tra trước khi chấp nhận mô hình.

### 3.1. Kiểm tra chất lượng dữ liệu bắt buộc

- Kiểm tra số dòng/cột, kiểu dữ liệu, giá trị thiếu, bản ghi trùng, giá trị bất thường và các giá trị phân loại.
- Xác minh khóa chính/khóa ngoại, độ phủ ID và quan hệ giữa các bảng.
- Kiểm tra dữ liệu tiền tệ như `order_value`, `campaign_budget`: parse số an toàn, xử lý ký hiệu tiền tệ và giá trị lỗi; không chuyển lỗi parse thành số hợp lệ một cách âm thầm.
- Kiểm tra định dạng timestamp, múi giờ nếu có, phạm vi thời gian và thứ tự thời gian.
- Phân biệt rõ dữ liệu thô, dữ liệu đã làm sạch, dữ liệu tích hợp và feature table; không ghi đè dữ liệu gốc.
- Lưu báo cáo chất lượng dữ liệu và các phép biến đổi có thể tái lập.

## 4. Kiến trúc và công nghệ dự kiến

Các công nghệ được chọn hoặc đã xuất hiện trong mã/ghi chú dự án:

- Python làm ngôn ngữ chính.
- DuckDB cho truy vấn/tích hợp dữ liệu lớn; Pandas hoặc Polars cho xử lý phù hợp.
- Parquet cho các bảng trung gian/feature table nếu pipeline hiện thực hóa.
- scikit-learn cho tiền xử lý, mô hình baseline và đánh giá.
- XGBoost cho mô hình tăng cường.
- PSO cho lựa chọn đặc trưng.
- Matplotlib cho biểu đồ.
- Pytest cho kiểm thử.
- Power BI nhận các bảng/CSV đã xuất từ pipeline.
- Website demo có thể được xây dựng riêng; chỉ đánh giá backend/frontend nếu thực sự tồn tại trong repository. Không mặc định rằng website đã hoàn thành.

Không thêm MongoDB vào kiến trúc này nếu không có quyết định mới được ghi nhận trong repository. Tránh thêm dịch vụ trả phí hoặc API bên ngoài không cần thiết.

## 5. Phạm vi pipeline cần được kiểm toán

Kiểm tra xem các bước sau có thực sự được triển khai, chạy đúng thứ tự và sử dụng cùng một cấu hình hay không:

1. **Data audit:** đọc schema, số dòng, chất lượng dữ liệu, phân phối target và tính toàn vẹn tham chiếu.
2. **Cleaning/integration:** chuẩn hóa kiểu dữ liệu, xử lý missing/duplicates, nối các bảng đúng khóa, ghi log và xuất dữ liệu sạch.
3. **Feature engineering:** tổng hợp hành vi khách hàng từ sessions/transactions/campaigns và ghép với thông tin customer/geo khi phù hợp.
4. **EDA:** phân phối target, đặc trưng khách hàng, hành vi truy cập/giao dịch, tương quan và biểu đồ có thể tái tạo.
5. **Train/validation split:** xác định rõ chiến lược chia tập, random seed, stratification hoặc time-based split nếu phù hợp với mục tiêu dự đoán.
6. **Baseline:** huấn luyện và đánh giá các mô hình trên cùng một tập validation, cùng định nghĩa feature và cùng quy trình tiền xử lý khi muốn so sánh công bằng.
7. **Feature selection:** xây dựng phương pháp thống kê và PSO; ghi lại objective/fitness, tham số, random seed, số lần đánh giá, thời gian tìm kiếm và tập đặc trưng được chọn.
8. **XGBoost:** so sánh mô hình dùng toàn bộ đặc trưng với mô hình dùng đặc trưng chọn lọc, trên cùng split và metric.
9. **Evaluation:** xuất metric, confusion matrix/threshold metrics nếu thích hợp, PR curve hoặc các biểu đồ liên quan; xác định cách chọn threshold.
10. **Export:** xuất bảng và biểu đồ cho Power BI, kết quả feature selection, metadata cấu hình và kết quả thí nghiệm.
11. **Testing/reproducibility:** kiểm thử, hướng dẫn cài đặt/chạy lại, seed, phiên bản thư viện và mô tả đầu ra.

## 6. Các lỗi/rủi ro cần ưu tiên kiểm tra

### 6.1. Critical/High — Leakage và tính hợp lệ thời gian

Đây là hạng mục ưu tiên cao nhất.

- Nếu mục tiêu là dự đoán mua hàng trong 30 ngày tương lai, mỗi feature chỉ được dùng thông tin sẵn có tại thời điểm dự đoán.
- Kiểm tra `transactions.csv` và `sessions.csv`: các bản ghi có thể xảy ra sau thời điểm chốt dự đoán hoặc trong khoảng 30 ngày dùng để tạo nhãn hay không.
- Những feature như `total_spend`, `trans_count`, `last_trans_date`, `high_value_flag`, số lần thêm giỏ hoặc tổng session có thể gây leakage nếu tính từ toàn bộ lịch sử chứa cả tương lai.
- Kiểm tra các feature gắn trực tiếp với kết quả mua hàng, trạng thái giao dịch, dữ liệu phát sinh sau mua hoặc biến được tạo từ target.
- Xác minh target được tạo như thế nào và prediction cutoff có thể suy ra từ tài liệu/dữ liệu hay không. Không tự khẳng định rằng dataset không leakage khi chưa có bằng chứng.
- Nếu không thể xác định cutoff, ghi rõ giới hạn: không thể chứng minh feature temporal là hợp lệ cho bài toán dự đoán tương lai; đề xuất cách xử lý hoặc cách giới hạn kết luận.

### 6.2. So sánh thí nghiệm không đồng nhất

Agent trước có báo cáo hai bảng baseline với số đặc trưng khác nhau:
- Một bảng baseline ghi khoảng **180 features**.
- Một bảng so sánh khác ghi **63 full features** và **17 selected features**.

Cần xác định tại sao số lượng khác nhau: phiên bản pipeline khác nhau, cột bị loại, thay đổi cấu hình, chỉ dùng numeric features, hoặc kết quả thử nghiệm trung gian. Không gộp các kết quả như thể cùng một thí nghiệm nếu không chứng minh được tính tương thích.

Kiểm tra:
- Tất cả mô hình trong một bảng so sánh có cùng train/validation indices không?
- Có cùng target, preprocessing, feature availability, threshold selection và metric implementation không?
- Có dùng validation để chọn feature/siêu tham số rồi lại báo cáo chính validation đó như kết quả cuối cùng không?
- Có cần một test set nội bộ riêng hoặc nested/cross-validation để giảm selection bias không? Đề xuất giải pháp phù hợp với quy mô và thời gian dự án.

### 6.3. PSO — Fitness, chi phí và diễn giải

- Đọc trực tiếp công thức fitness; xác định metric tối ưu, penalty theo số feature và cách xử lý trường hợp chọn quá ít/quá nhiều feature.
- Xác minh fitness được tính chỉ trên train/validation hợp lệ và không truy cập test labels.
- Kiểm tra encoding nhị phân, cập nhật vị trí/vận tốc, giới hạn số chiều, stopping criteria, random seed, số particle/iterations và cách lưu global-best.
- Phân biệt **thời gian fit mô hình sau khi chọn feature** với **tổng thời gian tìm kiếm PSO**. Không tuyên bố PSO tiết kiệm thời gian toàn bộ nếu chỉ đo thời gian fit.
- Đánh giá số feature giảm và hiệu năng bị mất bằng số tuyệt đối lẫn phần trăm tương đối; không diễn giải accuracy tăng là đủ nếu PR-AUC/ROC-AUC giảm.
- Xác minh feature selection không chạy trên toàn bộ dữ liệu trước khi split và không dùng target/test theo cách gây leakage.

### 6.4. Metric và mất cân bằng lớp

Tỷ lệ lớp dương được báo cáo khoảng 20.3%, do đó:
- Không dùng accuracy làm thước đo duy nhất.
- Ưu tiên PR-AUC/Average Precision, ROC-AUC, precision, recall, F1; thêm confusion matrix và threshold rõ ràng khi cần.
- Kiểm tra `pos_label`, cách tính average, cách lấy xác suất/decision score và cách chọn threshold.
- Đánh giá threshold có được chọn trên validation hay bị chọn theo test/target cuối cùng.
- Kiểm tra baseline dummy để biết mô hình có thực sự tốt hơn chiến lược đơn giản hay không.
- Ghi nhận độ biến thiên/khoảng tin cậy nếu chi phí cho phép; không tuyên bố ý nghĩa thống kê khi chưa kiểm định.

### 6.5. Khả năng tái lập và chất lượng code

- Chạy `pytest -v`; xem nội dung và phạm vi test, không chỉ nhìn số test pass.
- Kiểm tra import, đường dẫn tương đối, cấu hình, seed, xử lý exception và khả năng chạy từ thư mục gốc.
- Kiểm tra pipeline có phụ thuộc file đầu ra cũ hoặc thứ tự chạy thủ công không.
- Kiểm tra các file đầu ra có được sinh từ lần chạy cuối cùng hay còn sót từ thí nghiệm cũ.
- Kiểm tra `.gitignore`, không để token, mật khẩu, thông tin cá nhân hoặc dữ liệu nhạy cảm trong repository.
- Xác minh README phản ánh đúng lệnh, file đầu vào/đầu ra và thời gian chạy thực tế.

## 7. Kết quả sơ bộ Agent trước báo cáo — chỉ dùng làm điểm đối chiếu

**Không xem các số dưới đây là kết quả đã được xác nhận.** Hãy đối chiếu với CSV đầu ra, mã nguồn và cách chạy thực tế. Nếu không thể tái tạo, ghi là không xác minh được.

### 7.1. Baseline — bảng được báo cáo là dùng khoảng 180 features

| Mô hình (tên Agent báo cáo) | PR-AUC | ROC-AUC | F1 | Precision | Recall | Fit time (s) |
|---|---:|---:|---:|---:|---:|---:|
| Gradient Boosting | 0.2785 | 0.6150 | 0.3660 | 0.2442 | 0.7303 | 19.17 |
| Random Forest | 0.2753 | 0.6101 | 0.3635 | 0.2425 | 0.7258 | 12.95 |
| Logistic Regression | 0.2704 | 0.6033 | 0.3602 | 0.2396 | 0.7299 | 1.10 |
| “SVM (SGD)” | 0.2578 | 0.5858 | 0.3526 | 0.2337 | 0.7214 | 4.30 |
| Decision Tree | 0.2575 | 0.5927 | 0.3569 | 0.2372 | 0.7247 | 7.14 |
| Naive Bayes | 0.2170 | 0.5235 | 0.3377 | 0.2073 | 0.9080 | 0.42 |
| KNN | 0.2108 | 0.5187 | 0.3375 | 0.2071 | 0.9103 | 8.04 |

Xác minh tên mô hình “SVM (SGD)” từ class thực tế. Nếu là `SGDClassifier`, phải ghi tên chính xác và cấu hình loss; không mặc định đây là SVC kernel SVM.

### 7.2. So sánh — bảng được báo cáo là dùng 63 full features và 17 selected features

| Phương án | Số feature | PR-AUC | ROC-AUC | F1 | Precision | Recall | Accuracy | Fit time (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline full | 63 | 0.2787 | 0.6098 | 0.3689 | 0.2452 | 0.7428 | 0.4851 | 14.60 |
| Baseline statistical | 17 | 0.2778 | 0.6098 | 0.3682 | 0.2435 | 0.7554 | 0.4729 | 6.21 |
| Baseline PSO | 17 | 0.2643 | 0.5917 | 0.3572 | 0.2381 | 0.7140 | 0.4768 | 4.00 |
| XGBoost full | 63 | 0.2723 | 0.6018 | 0.3651 | 0.2413 | 0.7511 | 0.4682 | 3.18 |
| XGBoost PSO | 17 | 0.2586 | 0.5857 | 0.3556 | 0.2425 | 0.6698 | 0.5084 | 1.51 |

Nhận xét cần kiểm chứng:
- Giảm 63 xuống 17 feature tương đương giảm khoảng **73.0%** số đặc trưng.
- Với XGBoost, PR-AUC giảm từ 0.2723 xuống 0.2586 (giảm tuyệt đối 0.0137, khoảng 5.0% tương đối); ROC-AUC giảm 0.0161. Vì vậy chưa có cơ sở nói PSO “giữ nguyên hiệu năng trong 2.6%” nếu không xác định rõ metric và cách tính.
- Accuracy XGBoost PSO cao hơn trong bảng này nhưng PR-AUC/ROC-AUC/recall thấp hơn; không thể dựa vào accuracy riêng để kết luận mô hình tốt hơn.
- Fit time giảm không chứng minh tổng thời gian giảm nếu chưa tính chi phí tìm kiếm PSO.
- Các bảng có thể đến từ cấu hình hoặc lần chạy khác nhau; cần giải quyết khác biệt trước khi dùng trong báo cáo.

## 8. Cấu trúc code/đầu ra Agent trước báo cáo

Agent trước nói đã tạo các file tài liệu:
- `.gitignore`, `requirements.txt`
- `PRD.md`, `AGENTS.md`, `README.md`
- `DATA_DICTIONARY.md`, `ARCHITECTURE.md`, `EXPERIMENT_PLAN.md`, `DECISIONS.md`, `PROGRESS.md`, `REPRODUCIBILITY.md`

Các module được báo cáo:
- `config.py`
- `src/data/inspect_data.py`
- `src/data/clean_data.py`
- `src/data/integrate_data.py`
- `src/features/build_features.py`
- `src/analysis/eda.py`
- `src/models/baselines.py`
- `src/models/pso_optimizer.py`
- `src/models/feature_selection.py`
- `src/models/train_xgboost.py`
- `src/evaluation/evaluate.py`
- `src/export/export_outputs.py`
- `src/pipeline.py`
- thư mục tests

Agent trước báo cáo:
- Pipeline hoàn thành trong khoảng 148.4 giây.
- `pytest -v`: 11/11 tests passed.
- 67 engineered features và 9 biểu đồ EDA.
- `customer_features.parquet` khoảng 200,000 khách hàng.
- Có đầu ra dưới `outputs/`, `outputs/metrics/`, `outputs/plots/`, `outputs/feature_selection/`, `outputs/powerbi/`.

Đây là danh sách cần xác minh, không phải khẳng định các file vẫn tồn tại hoặc các số liệu là mới nhất. Kiểm tra repository thực tế và ghi nhận sai khác.

## 9. Phân công nhóm

Nhóm có 4 thành viên:

- **Thành viên 1 — người dùng:** phụ trách code và pipeline: DuckDB, cleaning/integration, feature engineering, EDA, baseline models, PSO, XGBoost, evaluation, exports, tests và tài liệu kỹ thuật.
- **Thành viên 2:** phần mở đầu, câu hỏi nghiên cứu/phương pháp, tài liệu liên quan và diễn giải EDA.
- **Thành viên 3:** diễn giải kết quả ML, PSO convergence, feature được chọn, phân tích lỗi và runtime.
- **Thành viên 4:** Power BI, website demo, slide, video/demo và tích hợp báo cáo cuối.

Codex tập trung vào kiểm toán kỹ thuật và độ tin cậy của bằng chứng. Không tự viết lại toàn bộ báo cáo học thuật nếu chưa được yêu cầu.

## 10. Tiêu chí nghiệm thu

Chỉ đánh dấu đạt khi có bằng chứng kiểm tra tương ứng.

### Dữ liệu
- [ ] Tám file CSV được nhận diện và số dòng/cột xác minh được.
- [ ] Schema, missing values, duplicates, ID coverage và referential integrity được báo cáo.
- [ ] Có data dictionary và mô tả nguồn gốc/biến đổi.
- [ ] Dữ liệu gốc không bị ghi đè.
- [ ] Quy tắc tạo target và thời điểm dự đoán được xác minh hoặc giới hạn chưa biết được ghi rõ.

### Chống leakage và thiết kế thí nghiệm
- [ ] Mọi feature đều có lý do hợp lệ để tồn tại tại thời điểm dự đoán.
- [ ] Không dùng test labels trong preprocessing, feature selection, tuning hoặc threshold selection.
- [ ] Train/validation split được tạo một lần hoặc được quản lý rõ ràng và dùng công bằng cho các mô hình so sánh.
- [ ] Các bảng so sánh dùng cùng định nghĩa target, split, preprocessing và metric, hoặc khác biệt được giải thích rõ.
- [ ] Có baseline đơn giản và metric phù hợp với dữ liệu mất cân bằng.
- [ ] PSO fitness, tham số, stopping criteria, seed và chi phí tìm kiếm được ghi lại.

### Mô hình và kết quả
- [ ] Kết quả có thể tái tạo từ mã/config và dữ liệu hiện có.
- [ ] Có PR-AUC, ROC-AUC, precision, recall, F1 và metric bổ sung phù hợp.
- [ ] Số feature trước/sau selection khớp với artifact.
- [ ] Thời gian fit được phân biệt với thời gian search/pipeline.
- [ ] Các kết luận phản ánh đúng trade-off; không tuyên bố PSO tốt hơn nếu kết quả không hỗ trợ.
- [ ] Bảng metric, biểu đồ và tài liệu dùng cùng một phiên bản kết quả.

### Code, đầu ra và tài liệu
- [ ] `pytest -v` chạy thành công và test kiểm tra logic quan trọng, không chỉ kiểm tra file tồn tại.
- [ ] Lệnh chạy được ghi rõ và hoạt động từ thư mục gốc.
- [ ] Các file Power BI export tồn tại, có schema ổn định và không chứa dữ liệu/metric giả.
- [ ] README và tài liệu khớp với repository hiện tại.
- [ ] Không có secrets trong mã hoặc file được commit.
- [ ] `docs/EXPERIMENT_AUDIT.md` nêu lỗi, bằng chứng, mức độ nghiêm trọng, phương án sửa và kết quả tái kiểm tra.

## 11. Cách làm việc và báo cáo đầu ra

Hãy thực hiện theo các giai đoạn, không chạy lại tất cả một cách máy móc:

**Giai đoạn A — Inventory:** liệt kê cấu trúc file, xác định entry point, config, dữ liệu, artifacts, test và tài liệu hiện có.

**Giai đoạn B — Static audit:** đọc mã để tìm leakage, split không nhất quán, metric sai, feature mismatch, lỗi đường dẫn và vấn đề tái lập.

**Giai đoạn C — Artifact audit:** đọc CSV/JSON/Parquet/biểu đồ đã sinh để so khớp với code; kiểm tra bảng metric, số feature, thời gian và ngày sửa file.

**Giai đoạn D — Targeted verification:** chạy các lệnh kiểm tra nhẹ, pytest và một phần thí nghiệm tối thiểu khi cần. Chỉ chạy full pipeline khi biết rõ chi phí, đầu ra sẽ bị ghi đè và việc chạy lại thực sự cần thiết.

**Giai đoạn E — Audit report:** tạo/cập nhật `docs/EXPERIMENT_AUDIT.md` theo cấu trúc:
1. Tóm tắt trạng thái: `PASS / PASS WITH ISSUES / FAIL / INSUFFICIENT EVIDENCE`.
2. Phạm vi đã kiểm tra và chưa kiểm tra.
3. Findings theo mức độ `Critical / High / Medium / Low`, mỗi finding gồm bằng chứng, tác động, cách sửa và cách xác minh.
4. Bảng đối chiếu các số liệu đã báo cáo với số liệu từ artifacts.
5. Kết quả test/lệnh đã chạy.
6. Kế hoạch sửa lỗi theo thứ tự ưu tiên.
7. Các giới hạn còn lại.

Trước khi thay đổi mã hoặc xóa/tạo lại artifacts, hãy nêu ngắn gọn kế hoạch và giữ lại bằng chứng cần thiết. Nếu được yêu cầu sửa lỗi, sửa theo từng nhóm, chạy test liên quan và ghi lại kết quả. Không tối ưu hóa chỉ để làm đẹp metric và không điều chỉnh kết luận nhằm khiến PSO có vẻ thành công.

## 12. Lệnh kiểm tra ban đầu gợi ý

Chạy từ thư mục gốc `Global` (điều chỉnh theo môi trường nếu cần):

```powershell
Get-Location
git status --short
Get-ChildItem
Get-ChildItem outputs -Recurse -File | Select-Object FullName, Length, LastWriteTime
pytest -v
```

Không chạy `python src/pipeline.py` ngay lập tức nếu chưa xác định được nó có ghi đè đầu ra hiện có hay không.

## 13. Chỉ dẫn cuối

Hãy bắt đầu bằng việc đọc repository và đưa ra **inventory + kế hoạch audit ngắn gọn**, sau đó tiếp tục kiểm tra. Đừng yêu cầu người dùng nhắc lại thông tin đã có trong file này. Không tuyên bố đã kiểm tra một file/lệnh nếu chưa thực sự truy cập hoặc chạy nó. Kết quả cuối cùng phải giúp người dùng quyết định rõ: dự án đã đủ tin cậy để chuyển sang Power BI/báo cáo hay phải sửa những lỗi nào trước.
