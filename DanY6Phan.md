PHẦN 1. GIỚI THIỆU NGHIÊN CỨU — DÀN Ý PHÂN CÔNG CHI TIẾT
Tên đề tài: Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử.
Người phụ trách chính: Người 2. Người 1 cung cấp số liệu dataset đã kiểm tra từ VS Code; Người 3 và Người 4 góp ý về tính khả thi và sản phẩm đầu ra.
1.1. Bối cảnh nghiên cứu
Mục đích: Giải thích vì sao bài toán phân tích hành vi và dự đoán mua hàng trong thương mại điện tử đáng nghiên cứu.
Các nội dung cần triển khai:

- 1.1.1. Sự phát triển của thương mại điện tử
  Trình bày xu hướng kinh doanh trực tuyến và sự gia tăng dữ liệu khách hàng.
  Phân tích các loại dữ liệu doanh nghiệp có thể thu thập: hồ sơ khách hàng, phiên truy cập, giỏ hàng, giao dịch và chiến dịch marketing.
  Dùng số liệu từ báo cáo thương mại điện tử có nguồn đáng tin cậy, ưu tiên báo cáo Việt Nam và báo cáo quốc tế gần đây.
- 1.1.2. Vai trò của dữ liệu trong hoạt động kinh doanh
  Giải thích dữ liệu hỗ trợ phân tích hành vi, phân khúc khách hàng và dự đoán mua hàng như thế nào.
  Phân biệt phân tích mô tả (điều gì đã xảy ra), phân tích dự đoán (điều gì có thể xảy ra) và hỗ trợ quyết định (nên hành động thế nào).
  Nêu giới hạn: dự đoán chính xác không đồng nghĩa với chứng minh hiệu quả marketing.
- 1.1.3. Thách thức khai thác dữ liệu hành vi
  Dữ liệu đến từ nhiều bảng, có quy mô khác nhau.
  Đặc trưng gốc có thể chưa biểu diễn đầy đủ hành vi khách hàng.
  Nhiều biến có thể dư thừa hoặc không hữu ích cho dự đoán.
  Các mô hình và phương pháp lựa chọn đặc trưng có thể cho kết quả khác nhau.
- 1.1.4. Dẫn vào hướng nghiên cứu
  Giới thiệu nhu cầu xây dựng đặc trưng hành vi, so sánh mô hình và lựa chọn đặc trưng bằng PSO.
  Kết thúc bằng lý do cần thực nghiệm để đánh giá hiệu quả của phương pháp, thay vì mặc định thuật toán nâng cao luôn tốt hơn.
  Cách thực hiện: Người 2 tìm tài liệu từ báo cáo chính thức, bài báo khoa học và nguồn thống kê đáng tin cậy. Phần này nên có 2–3 số liệu bối cảnh quan trọng, không biến thành bài tổng quan thị trường dài.
  Sản phẩm: Khoảng 2–3 trang, có trích dẫn nguồn.
  1.2. Vấn đề nghiên cứu
  Mục đích: Chuyển từ bối cảnh chung sang vấn đề cụ thể mà nhóm sẽ giải quyết.
  Các nội dung cần triển khai:
- 1.2.1. Vấn đề thực tiễn
  Doanh nghiệp có nhiều dữ liệu khách hàng nhưng khó chuyển dữ liệu thô thành thông tin dự đoán hữu ích.
  Việc kết hợp hồ sơ, phiên truy cập và giao dịch có thể tạo ra đặc trưng phong phú hơn.
  Cần đánh giá liệu các đặc trưng được xây dựng có cải thiện khả năng dự đoán hay không.
- 1.2.2. Vấn đề kỹ thuật
  Mô hình cơ sở có thể chưa khai thác tốt quan hệ phi tuyến giữa các biến.
  Sử dụng toàn bộ đặc trưng có thể làm tăng chi phí tính toán hoặc giữ lại các biến dư thừa.
  PSO có thể hỗ trợ tìm kiếm tập đặc trưng, nhưng cần so sánh với phương pháp lọc thống kê và đo chi phí thực thi.
- 1.2.3. Khoảng trống nghiên cứu cần khảo sát
  Tìm các nghiên cứu gần đây về dự đoán mua hàng, feature engineering, PSO và mô hình boosting.
  So sánh cách tạo đặc trưng, cách đánh giá, dữ liệu sử dụng và hạn chế của các nghiên cứu.
  Xác định khía cạnh nhóm có thể kiểm chứng trên dataset đã chọn.
  Lưu ý: chưa được khẳng định “chưa có nghiên cứu nào làm” trước khi rà soát tài liệu.
- 1.2.4. Phát biểu vấn đề nghiên cứu
  Chốt câu hỏi trung tâm: Việc khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO có cải thiện hiệu quả dự đoán so với các phương pháp cơ sở trong điều kiện tính toán giới hạn hay không?
  Cách thực hiện: Người 2 phối hợp Người 3 để bảo đảm vấn đề nêu ra có thể kiểm chứng bằng các thí nghiệm thực tế ở Phần 4.
  Sản phẩm: Khoảng 1–2 trang, kết thúc bằng phát biểu vấn đề rõ ràng.
  1.3. Giới thiệu bộ dữ liệu nghiên cứu
  Mục đích: Chứng minh dataset phù hợp với bài toán và xác định rõ dữ liệu đầu vào.
  1.3.1. Nguồn dữ liệu
  Giới thiệu bộ dữ liệu Global E-Commerce Customer Purchase Prediction trên Kaggle.
  Đưa liên kết nguồn dữ liệu và mô tả mục tiêu của bộ dữ liệu theo thông tin chính thức.
  Phân biệt thời gian diễn ra cuộc thi với thời gian ghi nhận trong các trường ngày tháng.
  Ghi rõ giấy phép và điều kiện sử dụng dữ liệu nếu nguồn cung cấp thông tin này.
  1.3.2. Quy mô và cấu trúc dữ liệu
  Dùng Python trên VS Code để đọc toàn bộ CSV, xác định số dòng, số cột, kiểu dữ liệu và dung lượng. Sau đó lập bảng tổng hợp:
  Tệp
  Số dòng dự kiến
  Nội dung cần giải thích
  customers.csv
  200.000
  Hồ sơ khách hàng
  sessions.csv
  2.000.000
  Hành vi phiên truy cập
  transactions.csv
  500.000
  Giao dịch
  marketing_campaigns.csv
  200
  Chiến dịch marketing
  geo_data.csv
  100
  Đặc điểm khu vực
  train.csv
  160.000
  Mã khách hàng và target
  test.csv
  40.000
  Mã khách hàng cần dự đoán
  sample_submission.csv
  40.000
  Định dạng kết quả mẫu

Các số dòng trên là số liệu kiểm tra sơ bộ, phải được xác nhận lại bằng code trước khi đưa vào báo cáo chính thức.
1.3.3. Vai trò của từng bảng
Mô tả các biến quan trọng của từng bảng.
Xác định các khóa liên kết như customer_id, campaign_id và geo_ip_region.
Trình bày cách các bảng có thể bổ sung thông tin cho nhau.
Chưa cần liệt kê tất cả cột; phần này chỉ chọn những biến quan trọng, còn data dictionary đầy đủ để ở phụ lục.
1.3.4. Biến mục tiêu và khả năng sử dụng
Xác minh ý nghĩa chính thức của target.
Thống kê tỷ lệ các lớp trong train.csv.
Kiểm tra quan hệ giữa ID ở tập train/test và bảng khách hàng.
Kiểm tra các trường thời gian để xác định khả năng sử dụng đặc trưng mà không gây rò rỉ dữ liệu.
Nếu không xác minh được mốc dự đoán tương lai, phải diễn giải đây là bài toán phân loại theo nhãn của dataset, không tự khẳng định là dự báo tương lai theo một cửa sổ thời gian cụ thể.
Công cụ: DuckDB và Python; Pandas/Polars để kiểm tra dữ liệu. Người 1 cung cấp bảng kết quả thực tế cho Người 2.
Sản phẩm: Khoảng 2–3 trang, một bảng mô tả dataset, một sơ đồ quan hệ dữ liệu và một bảng tóm tắt biến mục tiêu.
1.4. Lý do lựa chọn đề tài và dataset
Mục đích: Giải thích vì sao dataset và hướng nghiên cứu phù hợp với mục tiêu của nhóm.
Các ý cần phân tích:
1.4.1. Phù hợp với lĩnh vực thương mại điện tử: dữ liệu có hồ sơ, hành vi truy cập, giao dịch và thông tin chiến dịch.
1.4.2. Phù hợp với Big Data Analytics: có bảng hàng triệu dòng, cần tích hợp, tổng hợp và khai phá đặc trưng.
1.4.3. Phù hợp với Machine Learning: có nhãn target và dữ liệu phân chia train/test.
1.4.4. Phù hợp với PSO Feature Selection: có khả năng xây dựng nhiều nhóm đặc trưng và thiết kế thí nghiệm so sánh tập đặc trưng.
1.4.5. Khả thi về công cụ: có thể xử lý bằng DuckDB và Python trên VS Code mà không cần dựng MongoDB hoặc hệ thống phân tán.
1.4.6. Khả năng phát triển sản phẩm: kết quả có thể chuyển thành dashboard Power BI và website giới thiệu nghiên cứu.
Cách thực hiện: Viết theo quan hệ giữa đặc điểm dataset và mục tiêu nghiên cứu; tránh chỉ liệt kê rằng dataset “lớn, mới và có nhiều biến”.
Sản phẩm: Khoảng 1–1,5 trang.
1.5. Mục tiêu nghiên cứu
1.5.1. Mục tiêu tổng quát
Xây dựng và đánh giá quy trình khai phá đặc trưng hành vi, lựa chọn đặc trưng bằng PSO và áp dụng Machine Learning cho bài toán phân loại theo nhãn mục tiêu của bộ dữ liệu thương mại điện tử.
1.5.2. Mục tiêu cụ thể
Mục tiêu 1: Tích hợp và kiểm tra dữ liệu bằng DuckDB và Python.
Mục tiêu 2: Xây dựng các đặc trưng hành vi từ khách hàng, phiên truy cập và giao dịch.
Mục tiêu 3: Phân tích dữ liệu khám phá để nhận diện phân phối và khác biệt giữa các nhóm.
Mục tiêu 4: Huấn luyện và so sánh bảy mô hình cơ sở.
Mục tiêu 5: So sánh lựa chọn đặc trưng bằng phương pháp thống kê với PSO.
Mục tiêu 6: Đánh giá mô hình nâng cao bằng các chỉ số dự đoán, số lượng đặc trưng và chi phí tính toán.
Mục tiêu 7: Xây dựng dashboard và website để trình bày kết quả.
Cách thực hiện: Mỗi mục tiêu phải tương ứng với một đầu ra có thể kiểm tra, chẳng hạn bảng đặc trưng, bảng EDA, bảng so sánh mô hình hoặc dashboard.
Sản phẩm: Khoảng 0,5–1 trang.
1.6. Đối tượng, phạm vi và giới hạn nghiên cứu
1.6.1. Đối tượng nghiên cứu
Quy trình xây dựng và lựa chọn đặc trưng hành vi.
Các mô hình phân loại Machine Learning.
Phương pháp tối ưu lựa chọn đặc trưng bằng PSO.
Mối quan hệ giữa hiệu năng dự đoán, số lượng đặc trưng và chi phí tính toán.
1.6.2. Phạm vi dữ liệu
Chỉ sử dụng bộ dữ liệu Kaggle đã chọn.
Sử dụng các bảng và biến phù hợp với bài toán.
Không thu thập dữ liệu giao dịch thực tế từ doanh nghiệp.
Không mặc định kết quả đại diện cho toàn bộ thị trường thương mại điện tử.
1.6.3. Phạm vi kỹ thuật
DuckDB để truy vấn và tổng hợp dữ liệu.
Python trên VS Code để tiền xử lý, EDA, feature engineering và huấn luyện mô hình.
PSO để lựa chọn đặc trưng.
Power BI để trực quan hóa và website để giới thiệu nghiên cứu.
1.6.4. Giới hạn dự kiến
Dữ liệu được cung cấp sẵn, không do nhóm tự thu thập.
Ý nghĩa và thời điểm hình thành nhãn cần được xác minh.
PSO có chi phí tính toán cao hơn một số phương pháp lọc biến đơn giản.
Chưa có dữ liệu để khẳng định quan hệ nhân quả hoặc hiệu quả kinh doanh thực tế.
Khả năng tổng quát hóa cần được xem xét dựa trên kết quả đánh giá.
Sản phẩm: Khoảng 1 trang.
1.7. Đóng góp dự kiến và điểm khác biệt
Mục đích: Nêu rõ nghiên cứu đóng góp gì ngoài việc chỉ chạy thuật toán có sẵn.
1.7.1. Đóng góp về phương pháp
Xây dựng bộ đặc trưng từ nhiều bảng dữ liệu thương mại điện tử.
Thiết kế thí nghiệm so sánh đặc trưng đầy đủ, đặc trưng lọc thống kê và đặc trưng PSO lựa chọn.
Kết hợp chất lượng dự đoán với số lượng đặc trưng và chi phí tính toán.
1.7.2. Đóng góp về thực nghiệm
So sánh bảy mô hình cơ sở.
Đánh giá mô hình nâng cao với tập đặc trưng được tối ưu.
Phân tích tập đặc trưng được chọn, mức cải thiện và độ ổn định của kết quả.
1.7.3. Đóng góp về ứng dụng
Chuyển kết quả thành dashboard Power BI.
Xây dựng website giới thiệu mục tiêu, phương pháp, kết quả và demo.
Đề xuất các hướng ứng dụng phù hợp với bằng chứng dữ liệu.
1.7.4. Cách xác định điểm mới
Người 2 rà soát các nghiên cứu gần đây để xác định khoảng trống phù hợp. Người 3 kiểm tra khả năng chứng minh điểm khác biệt bằng thực nghiệm. Không tuyên bố PSO là thuật toán mới hoặc khẳng định mô hình sẽ vượt trội trước khi có kết quả.
Sản phẩm: Khoảng 1 trang.
1.8. Bố cục báo cáo
Trình bày ngắn gọn sáu phần:
Giới thiệu nghiên cứu.
Câu hỏi và phương pháp nghiên cứu.
Xử lý dữ liệu và phân tích khám phá.
Machine Learning và tối ưu lựa chọn đặc trưng.
Dashboard và hàm ý quản trị.
Hạn chế, hướng phát triển và kết luận.
Tài liệu tham khảo và phụ lục được đặt sau sáu phần chính.
Sản phẩm: Khoảng nửa trang.
Bảng phân công thực hiện Phần 1
Mục
Người thực hiện chính
Phối hợp
1.1 Bối cảnh
Người 2
—
1.2 Vấn đề nghiên cứu
Người 2
Người 3
1.3 Dataset
Người 2 viết
Người 1 xuất số liệu và xác minh
1.4 Lý do lựa chọn
Người 2
Người 1 xác nhận tính khả thi
1.5 Mục tiêu
Người 2
Người 3, Người 4 góp ý
1.6 Phạm vi
Người 2
Người 1 xác nhận công cụ
1.7 Đóng góp dự kiến
Người 2
Người 3 và Người 4
1.8 Bố cục báo cáo
Người 2
Cả nhóm thống nhất

Yêu cầu bàn giao Phần 1: Người 2 hoàn thành bản thảo theo các mục trên; Người 1 cung cấp số liệu dataset đã kiểm tra; các trích dẫn phải có nguồn xác minh. Phần 1 chỉ trình bày bối cảnh, vấn đề, mục tiêu và đóng góp dự kiến, không đưa kết quả mô hình chưa chạy vào báo cáo.
PHẦN 2. CÂU HỎI VÀ PHƯƠNG PHÁP NGHIÊN CỨU — DÀN Ý PHÂN CÔNG CHI TIẾT
Người phụ trách chính: Người 2. Phối hợp: Người 1 cung cấp thông tin về dữ liệu và tính khả thi kỹ thuật; Người 3 góp ý về thiết kế thực nghiệm Machine Learning; Người 4 góp ý về đầu ra dashboard và website.
Mục tiêu của Phần 2 là xác định rõ nghiên cứu cần trả lời câu hỏi nào, kiểm chứng giả thuyết gì, sử dụng phương pháp nào và dựa vào tiêu chí nào để đánh giá kết quả. Phần này đóng vai trò thiết kế cho toàn bộ quy trình code ở Phần 3 và Phần 4.
2.1. Mục tiêu và định hướng nghiên cứu
2.1.1. Mục tiêu tổng quát
Trình bày mục tiêu khai phá đặc trưng hành vi khách hàng và tối ưu lựa chọn đặc trưng bằng PSO.
Làm rõ mối liên hệ giữa xây dựng đặc trưng, lựa chọn đặc trưng và hiệu năng dự đoán.
Xác định phạm vi đánh giá trên dataset Global E-Commerce Customer Purchase Prediction.
2.1.2. Mục tiêu cụ thể
Tích hợp và tổng hợp dữ liệu đa bảng bằng DuckDB và Python.
Xây dựng các đặc trưng hành vi khách hàng.
Phân tích dữ liệu và xác định các đặc trưng tiềm năng.
So sánh 7 mô hình Machine Learning cơ sở.
So sánh lựa chọn đặc trưng bằng phương pháp thống kê và PSO.
Đánh giá mô hình nâng cao, số lượng biến được chọn và chi phí tính toán.
Chuyển kết quả thành dashboard Power BI và website giới thiệu nghiên cứu.
Cách thực hiện: Đối chiếu từng mục tiêu với một đầu ra cụ thể. Ví dụ, mục tiêu xây dựng đặc trưng phải có bảng đặc trưng; mục tiêu so sánh mô hình phải có bảng metrics; mục tiêu tối ưu PSO phải có danh sách biến được chọn và thời gian thực thi.
Người thực hiện: Người 2 viết; Người 1 xác nhận các đầu ra có thể xuất từ pipeline.
2.2. Câu hỏi nghiên cứu
Đây là phần quan trọng nhất của Phần 2. Mỗi câu hỏi phải có phương pháp trả lời và kết quả tương ứng.
2.2.1. RQ1 — Đặc trưng hành vi nào có thể khai thác từ dữ liệu đa bảng?
Các nội dung cần thực hiện:
Phân tích thông tin có trong bảng khách hàng, phiên truy cập và giao dịch.
Xây dựng các nhóm đặc trưng như hồ sơ khách hàng, mức độ truy cập, tương tác giỏ hàng, tần suất giao dịch và giá trị mua sắm.
Kiểm tra phân phối, giá trị thiếu, tương quan và khác biệt giữa các nhóm theo target.
Đánh giá khả năng sử dụng của từng nhóm đặc trưng trước khi đưa vào mô hình.
Phương pháp: EDA, thống kê mô tả, phân tích tương quan và so sánh nhóm; sử dụng Python, Pandas/Polars và DuckDB.
Đầu ra: Data dictionary, bảng thống kê đặc trưng và các biểu đồ có ý nghĩa.
2.2.2. RQ2 — Các mô hình cơ sở có khả năng dự đoán nhãn mục tiêu như thế nào?
Các nội dung cần thực hiện:
Huấn luyện 7 mô hình: Logistic Regression, Naive Bayes, Decision Tree, Random Forest, Gradient Boosting, KNN và SVM.
So sánh các mô hình trên cùng quy trình chia dữ liệu.
Đánh giá bằng ROC-AUC, PR-AUC, Precision, Recall, F1 và thời gian thực thi.
Xác định mô hình cơ sở phù hợp để làm mốc đối chứng cho mô hình nâng cao.
Phương pháp: Classification, pipeline tiền xử lý, cross-validation hoặc validation phù hợp với ngân sách tính toán.
Đầu ra: Bảng so sánh mô hình, confusion matrix và biểu đồ kết quả.
2.2.3. RQ3 — PSO có cải thiện việc lựa chọn đặc trưng so với phương pháp thống kê hay không?
Các nội dung cần thực hiện:
Xây dựng phương pháp lọc đặc trưng thống kê làm đối chứng.
Thiết kế PSO để tìm kiếm tập con đặc trưng.
So sánh ba cấu hình: sử dụng toàn bộ đặc trưng, sử dụng đặc trưng lọc thống kê và sử dụng đặc trưng do PSO lựa chọn.
Đánh giá hiệu năng, số lượng biến, thời gian chạy và độ ổn định của tập đặc trưng.
Phương pháp: PSO Feature Selection; hàm mục tiêu dựa trên chỉ số đánh giá được chọn trước; cache fitness và giới hạn ngân sách tính toán.
Đầu ra: Danh sách biến được chọn, biểu đồ hội tụ PSO, bảng so sánh và báo cáo thời gian thực thi.
2.2.4. RQ4 — Mô hình nâng cao có tạo ra sự cân bằng tốt hơn giữa hiệu năng và chi phí tính toán không?
Các nội dung cần thực hiện:
Kết hợp tập đặc trưng được lựa chọn với XGBoost; cân nhắc CatBoost nếu có lý do và đủ thời gian.
So sánh với mô hình cơ sở và cấu hình không sử dụng PSO.
Phân tích hiệu năng dự đoán, số lượng đặc trưng, thời gian huấn luyện và sai số.
Kiểm tra xem kết quả có ổn định khi thay đổi cách chia dữ liệu hay không.
Phương pháp: Ensemble learning, validation, phân tích sai số và kiểm tra độ ổn định.
Đầu ra: Bảng kết quả thực nghiệm cuối cùng, biểu đồ feature importance và báo cáo sai số.
2.2.5. RQ5 — Kết quả nghiên cứu có thể hỗ trợ phân tích và ra quyết định kinh doanh như thế nào?
Các nội dung cần thực hiện:
Xác định các nhóm khách hàng hoặc hành vi đáng chú ý nếu dữ liệu hỗ trợ.
Trình bày kết quả dự đoán theo nhóm, mức xác suất và đặc trưng liên quan.
Xây dựng dashboard Power BI và website giới thiệu phương pháp, kết quả.
Đề xuất cách sử dụng kết quả trong phân tích khách hàng, đồng thời nêu rõ giới hạn.
Phương pháp: Trực quan hóa dữ liệu, phân tích nhóm và diễn giải kết quả mô hình.
Đầu ra: Dashboard, website và các đề xuất có căn cứ từ kết quả thực nghiệm.
2.3. Giả thuyết nghiên cứu
Các giả thuyết cần có khả năng kiểm chứng, không được viết như những kết luận đã biết trước.
Mã
Giả thuyết dự kiến
Cách kiểm chứng
H1
Các nhóm đặc trưng được xây dựng từ hành vi truy cập và giao dịch cung cấp thông tin bổ sung cho mô hình so với một tập đặc trưng nền tảng đơn giản
So sánh mô hình với các nhóm đặc trưng khác nhau
H2
Các mô hình phi tuyến hoặc ensemble có thể đạt hiệu năng tốt hơn mô hình tuyến tính trên tập đặc trưng đã xây dựng
So sánh các chỉ số trên cùng quy trình đánh giá
H3
PSO có thể tìm được tập đặc trưng gọn hơn mà vẫn duy trì hoặc cải thiện hiệu năng dự đoán
So sánh hiệu năng và số lượng biến giữa các cấu hình
H4
Mô hình nâng cao với đặc trưng được tối ưu có thể tạo ra sự cân bằng tốt hơn giữa chất lượng dự đoán và chi phí tính toán
Đánh giá đồng thời metrics, số biến và runtime

Cách thực hiện:
H1 cần có cấu hình đặc trưng nền tảng và cấu hình bổ sung hành vi để so sánh.
H2 cần sử dụng cùng cách chia dữ liệu, cùng định nghĩa chỉ số và quy trình tiền xử lý hợp lệ.
H3 cần quy định trước cách đo số lượng biến và hiệu năng; không chọn mô hình bằng tập test.
H4 cần xác định ngân sách thời gian hoặc tài nguyên tính toán trước khi chạy thí nghiệm.
Nếu kết quả không ủng hộ một giả thuyết, phải báo cáo đúng kết quả đó. Không điều chỉnh cách diễn giải chỉ để khẳng định phương pháp nâng cao tốt hơn.
Người phụ trách: Người 2 xây dựng giả thuyết; Người 3 xác nhận khả năng kiểm chứng; Người 1 triển khai các bảng kết quả tương ứng.
2.4. Thiết kế nghiên cứu
2.4.1. Loại hình nghiên cứu
Nghiên cứu định lượng dựa trên dữ liệu thứ cấp.
Kết hợp phân tích khám phá dữ liệu và thực nghiệm Machine Learning.
So sánh các cấu hình mô hình theo quy trình đánh giá thống nhất.
2.4.2. Quy trình nghiên cứu
Thu thập và kiểm tra bộ dữ liệu Kaggle.
Tích hợp các bảng bằng DuckDB và Python.
Làm sạch và xây dựng đặc trưng hành vi.
Thực hiện EDA và tổng hợp kết quả.
Huấn luyện 7 mô hình cơ sở.
Lọc đặc trưng bằng phương pháp thống kê.
Thực hiện PSO Feature Selection trong ngân sách tính toán đã xác định.
Huấn luyện mô hình nâng cao và so sánh các cấu hình.
Phân tích sai số, xuất kết quả và xây dựng dashboard/website.
Công cụ: VS Code, Python, DuckDB, Pandas/Polars, scikit-learn, thư viện PSO phù hợp và XGBoost; Power BI và framework website ở giai đoạn trình bày.
2.4.3. Nguyên tắc chia dữ liệu
Giữ nguyên tập test được cung cấp nếu có thể sử dụng đúng theo quy định của dataset.
Tách validation từ tập train để lựa chọn mô hình và đặc trưng.
Không dùng test để chọn biến, điều chỉnh siêu tham số hoặc quyết định cấu hình PSO.
Đặt các bước tiền xử lý cần học tham số bên trong pipeline để tránh rò rỉ dữ liệu.
Nếu nhãn của test không được cung cấp, không báo cáo các chỉ số đánh giá trên test như thể đã biết nhãn.
2.4.4. Kiểm soát chi phí tính toán
Chạy thử trên tập con để đo thời gian và tài nguyên.
Giới hạn số hạt, số vòng lặp và số cấu hình PSO.
Dùng cache để tránh đánh giá lặp lại cùng tập đặc trưng.
Chỉ mở rộng quy mô khi kết quả chạy thử cho thấy khả thi.
Ghi lại cấu hình và runtime để có thể tái lập.
Đầu ra: Sơ đồ quy trình nghiên cứu và bảng mô tả thiết kế thực nghiệm.
2.5. Phương pháp xử lý và phân tích dữ liệu
2.5.1. Truy vấn và tích hợp dữ liệu
Dùng DuckDB đọc CSV, kiểm tra schema và kết hợp các bảng.
Tổng hợp sessions và transactions theo customer_id trước khi ghép vào bảng đặc trưng khách hàng.
Kiểm tra khóa trùng, khóa không khớp và số dòng trước/sau khi join.
Xuất bảng đặc trưng phục vụ Python.
2.5.2. Tiền xử lý và xây dựng đặc trưng
Xử lý giá trị thiếu và chuẩn hóa kiểu dữ liệu.
Chuẩn hóa biến phân loại và biến số theo yêu cầu từng mô hình.
Xây dựng các đặc trưng như số phiên, thời lượng truy cập, mức độ tương tác giỏ hàng, RFM và tần suất giao dịch nếu tính được hợp lệ.
Loại bỏ biến không phù hợp, biến định danh không có giá trị dự đoán và các biến gây rò rỉ.
Lưu công thức, nguồn và ý nghĩa của từng đặc trưng trong data dictionary.
2.5.3. Phân tích khám phá dữ liệu
Thống kê mô tả và phân phối các biến.
Phân tích mức độ mất cân bằng của target.
Kiểm tra tương quan và sự khác biệt giữa các nhóm.
Phân tích hành vi truy cập và giao dịch theo các nhóm phù hợp.
Chỉ dùng kiểm định thống kê khi điều kiện áp dụng được đáp ứng; phân biệt tương quan với quan hệ nhân quả.
2.5.4. Huấn luyện và đánh giá mô hình
Xây dựng pipeline riêng phù hợp với từng thuật toán.
Dùng cùng nguyên tắc chia dữ liệu và tiêu chí đánh giá.
Báo cáo ROC-AUC, PR-AUC, Precision, Recall, F1 và confusion matrix.
Ghi nhận runtime, số lượng đặc trưng và cấu hình.
Phân tích sai số và mức độ ổn định, thay vì chỉ xếp hạng theo một chỉ số.
2.5.5. Lựa chọn đặc trưng bằng PSO
Biểu diễn mỗi hạt như một tập con đặc trưng.
Xác định hàm fitness và giới hạn số lượng biến hoặc cơ chế phạt.
Chạy PSO trên dữ liệu huấn luyện với validation nội bộ.
Lưu lịch sử fitness, tập biến được chọn và thời gian chạy.
So sánh với toàn bộ đặc trưng và phương pháp lọc thống kê.
2.5.6. Trực quan hóa và diễn giải kết quả
Xuất các bảng kết quả dưới dạng CSV và biểu đồ PNG.
Tạo dashboard Power BI theo câu hỏi quản trị.
Xây dựng website giới thiệu nghiên cứu và demo nếu mô hình được triển khai thành API.
Đánh dấu rõ kết quả thực nghiệm, dự báo và giả định mô phỏng.
Người thực hiện: Người 1 triển khai code; Người 2 và Người 3 diễn giải kết quả; Người 4 xây dựng sản phẩm trực quan.
2.6. Tiêu chí đánh giá
2.6.1. Chỉ số đánh giá mô hình
Chỉ số
Mục đích
ROC-AUC
Đánh giá khả năng phân biệt hai lớp trên nhiều ngưỡng
PR-AUC
Đánh giá Precision–Recall, đặc biệt hữu ích khi lớp dương ít
Precision
Đo tỷ lệ dự đoán dương tính đúng trong các dự đoán dương tính
Recall
Đo tỷ lệ phát hiện được các trường hợp dương tính
F1-score
Cân bằng Precision và Recall
Confusion matrix
Phân tích TP, FP, TN và FN
Runtime
Đánh giá chi phí thời gian thực thi
Số lượng đặc trưng
Đánh giá mức độ gọn của tập biến

Không chọn Accuracy làm tiêu chí duy nhất. Chỉ số chính để chọn mô hình cần được xác định trước khi chạy thí nghiệm; PR-AUC là một ứng viên phù hợp nếu dữ liệu mất cân bằng đáng kể.
2.6.2. Tiêu chí đánh giá PSO
Hiệu năng dự đoán so với toàn bộ đặc trưng.
Hiệu năng dự đoán so với lọc thống kê.
Số lượng đặc trưng được lựa chọn.
Thời gian thực thi và số lượt đánh giá fitness.
Độ ổn định của tập đặc trưng và kết quả giữa các lần chạy.
2.6.3. Tiêu chí đánh giá tính ứng dụng
Kết quả có thể truy vết về dữ liệu và cấu hình thí nghiệm.
Dashboard thể hiện đúng số liệu và cho phép khám phá kết quả.
Website trình bày rõ mục tiêu, phương pháp, kết quả và giới hạn.
Các đề xuất kinh doanh có căn cứ, không suy diễn quan hệ nhân quả từ mô hình dự đoán.
2.7. Tổng quan nghiên cứu liên quan và khoảng trống nghiên cứu
Phần này cần được viết dựa trên các tài liệu đã xác minh, không chỉ liệt kê tên bài báo.
2.7.1. Nhóm nghiên cứu về dự đoán hành vi mua hàng
Tìm các nghiên cứu sử dụng dữ liệu thương mại điện tử để phân loại hoặc dự đoán hành vi mua.
Ghi nhận loại dữ liệu, thuật toán, cách chia tập và chỉ số đánh giá.
So sánh ưu điểm, hạn chế và khả năng áp dụng vào dataset đang nghiên cứu.
2.7.2. Nhóm nghiên cứu về Feature Engineering và Feature Selection
Tìm các nghiên cứu xây dựng đặc trưng hành vi, RFM và đặc trưng từ chuỗi phiên truy cập.
Tìm nghiên cứu sử dụng lọc thống kê, phương pháp wrapper và các thuật toán lựa chọn đặc trưng.
Phân biệt lựa chọn đặc trưng với giảm chiều dữ liệu; không xem hai kỹ thuật là một.
2.7.3. Nhóm nghiên cứu về PSO và mô hình boosting
Tìm nghiên cứu ứng dụng PSO cho lựa chọn đặc trưng trong bài toán phân loại.
Tìm nghiên cứu kết hợp PSO với XGBoost, CatBoost hoặc các mô hình ensemble.
Ghi nhận hàm fitness, số hạt, số vòng lặp, chi phí tính toán và cách kiểm định.
2.7.4. Nhóm nghiên cứu về đánh giá và giải thích mô hình
Tìm các nghiên cứu về dữ liệu mất cân bằng, PR-AUC, phân tích sai số và giải thích mô hình.
Ghi nhận các phương pháp đánh giá tính ổn định và khả năng khái quát hóa.
2.7.5. Tổng hợp và xác định khoảng trống
Lập bảng so sánh gồm: tác giả/năm, dữ liệu, phương pháp, chỉ số, kết quả chính, hạn chế và liên hệ với đề tài.
Từ bảng này, xác định khía cạnh nghiên cứu có thể kiểm chứng, chẳng hạn so sánh hiệu quả của PSO với lọc thống kê trên cùng bộ đặc trưng và cùng ngân sách đánh giá. Chỉ kết luận về khoảng trống sau khi đã rà soát đủ tài liệu.
Yêu cầu tài liệu: Mục tiêu toàn báo cáo là tối thiểu 25 tài liệu khoa học phù hợp, xuất bản trong giai đoạn 2021–2026. Nên thu thập khoảng 30–35 tài liệu ban đầu để có thể loại các nguồn trùng lặp hoặc không phù hợp.
Người phụ trách: Người 2 điều phối; Người 3 tìm tài liệu về PSO/ML; Người 4 tìm tài liệu về dashboard và hỗ trợ quyết định. Mỗi người cung cấp thông tin thư mục và liên kết nguồn để Người 2 tổng hợp.
Bảng phân công tổng hợp Phần 2
Hạng mục
Người chính
Phối hợp
2.1 Mục tiêu nghiên cứu
Người 2
Người 1
2.2 Câu hỏi nghiên cứu
Người 2
Người 3, Người 4
2.3 Giả thuyết nghiên cứu
Người 2
Người 3
2.4 Thiết kế nghiên cứu
Người 2
Người 1, Người 3
2.5 Phương pháp xử lý và phân tích
Người 1 triển khai
Người 2 mô tả phương pháp
2.6 Tiêu chí đánh giá
Người 3 đề xuất chuyên môn
Người 1 triển khai, Người 2 viết
2.7 Tổng quan nghiên cứu
Người 2 điều phối
Người 3 và Người 4 tìm tài liệu theo nhóm

Sản phẩm bàn giao Phần 2:
Danh sách câu hỏi nghiên cứu và giả thuyết.
Sơ đồ quy trình nghiên cứu.
Bảng thiết kế thực nghiệm và tiêu chí đánh giá.
Bảng tổng quan tài liệu liên quan có nguồn xác minh.
Danh sách đầu ra mà Người 1 phải tạo trong pipeline VS Code.
Phần 2 nên được hoàn thành trước khi chạy toàn bộ thí nghiệm. Khi câu hỏi, tiêu chí đánh giá và thiết kế kiểm định đã thống nhất, Người 1 có thể xây dựng pipeline theo yêu cầu rõ ràng, còn Người 2 và Người 3 có cơ sở để phân tích kết quả mà không cần sửa lại mục tiêu sau khi đã thấy số liệu.
PHẦN 3. XỬ LÝ DỮ LIỆU VÀ PHÂN TÍCH KHÁM PHÁ (EDA)
Phần 3 tập trung vào việc kiểm tra chất lượng dữ liệu, kết hợp các bảng, xây dựng đặc trưng hành vi khách hàng và phân tích dữ liệu trước khi đưa vào mô hình Machine Learning. Đây là phần nền tảng cho đề tài “Khai phá đặc trưng hành vi và tối ưu lựa chọn đặc trưng bằng PSO cho bài toán dự đoán khả năng mua hàng trong thương mại điện tử.”
Phân công theo thống nhất trước đó: Thành viên 1 phụ trách toàn bộ code bằng VS Code và AI Agent; Thành viên 2 viết nội dung nghiên cứu, diễn giải kết quả EDA; Thành viên 3 và 4 nhận kết quả để phục vụ các phần sau.
3.1. Tổng quan bộ dữ liệu
Mục tiêu: Giới thiệu nguồn dữ liệu, quy mô, cấu trúc và vai trò của từng bảng, phân định rõ giữa tập dữ liệu khám phá ban đầu (Snapshot) và bộ chuẩn thực nghiệm có kiểm soát (Controlled Synthetic Benchmark Dataset).

3.1.1. Bộ dữ liệu thô ban đầu (Exploratory Snapshot)
- Nguồn dữ liệu: Global E-Commerce Customer Purchase Prediction trên Kaggle.
- Đặc điểm: Là bản chụp tĩnh (static snapshot) ban đầu, cung cấp quy mô lớn để khảo sát cấu trúc chung nhưng chưa có nhãn thời gian thực thi Point-in-Time tường minh.
- Quy mô snapshot ban đầu:

| Tệp dữ liệu | Quy mô | Vai trò | Ghi chú kiểm toán |
| :--- | :--- | :--- | :--- |
| `customers.csv` | 200.000 dòng, 17 cột | Hồ sơ khách hàng | Bảng thực thể gốc |
| `sessions.csv` | 2.000.000 dòng, 11 cột | Nhật ký truy cập web | 10 phiên / khách hàng |
| `transactions.csv` | 500.000 dòng, 11 cột | Lịch sử giao dịch | 2,5 giao dịch / khách hàng |
| `marketing_campaigns.csv` | 200 dòng, 6 cột | Danh mục chiến dịch | Thứ nguyên marketing |
| `geo_data.csv` | 100 dòng, 5 cột | Thông tin địa lý IP | Thứ nguyên khu vực |
| `train.csv` | 160.000 dòng, 2 cột | Dữ liệu huấn luyện | Tỷ lệ nhãn dương tĩnh ~20,3% |
| `test.csv` | 40.000 dòng, 1 cột | Dữ liệu kiểm tra | Khóa khách hàng chưa gắn nhãn |
| `sample_submission.csv` | 40.000 dòng, 2 cột | Định dạng nộp bài | Mẫu dự đoán |

*Lưu ý kiểm toán:* Tập dữ liệu snapshot 200k này chứa nhãn tĩnh không có mốc chốt thời gian $t_0$, tiềm ẩn rủi ro rò rỉ thông tin tương lai (temporal leakage) nếu dùng trực tiếp để mô phỏng bài toán dự đoán hành vi tương lai 30 ngày.

3.1.2. Bộ chuẩn kiểm soát độc lập (Controlled Synthetic Benchmark Dataset)
Để đảm bảo tính nghiêm ngặt khoa học, tái lập và triệt tiêu hoàn toàn temporal leakage, nhóm nghiên cứu thiết lập và kiểm định độc lập bộ chuẩn kiểm soát tại thư mục `outputs/controlled_benchmark/` theo chuẩn Point-in-Time dọc (Longitudinal Point-in-Time):
- Mốc chốt đặc trưng ($t_0$): `2024-06-01`.
- Cửa sổ quan sát nhãn tương lai: 30 ngày, từ $(2024-06-01, 2024-07-01]$.
- Quy mô và cấu trúc đã kiểm toán thực tế (tính từ `outputs/controlled_benchmark/eda/data_inventory.csv`):

| STT | Tệp dữ liệu | Vai trò | Số dòng | Số cột | Khóa chính | Kích thước | Mã băm SHA-256 (rút gọn) |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| 1 | `customers.csv` | Hồ sơ khách hàng | 25.000 | 17 | `customer_id` | 2,60 MB | `8ae94a53...` (Khớp 100% manifest) |
| 2 | `sessions.csv` | Nhật ký truy cập web | 89.666 | 11 | `session_id` | 5,36 MB | `a4920279...` (Khớp 100% manifest) |
| 3 | `transactions.csv` | Lịch sử giao dịch | 21.534 | 11 | `transaction_id` | 1,43 MB | `4ec63e80...` (Khớp 100% manifest) |
| 4 | `marketing_campaigns.csv` | Danh mục chiến dịch | 50 | 6 | `campaign_id` | 2,65 KB | `82b429d3...` (Khớp 100% manifest) |
| 5 | `geo_data.csv` | Thứ nguyên địa lý IP | 100 | 5 | `geo_ip_region` | 4,16 KB | `c1d763eb...` (Khớp 100% manifest) |
| 6 | `customer_labels_pit.csv` | Nhãn mục tiêu PIT | 25.000 | 2 | `customer_id` | 208,90 KB | `a01ecb0b...` (Nhãn dương: 8,78%) |
| 7 | `customer_features_pit.parquet` | Bảng đặc trưng chốt $t_0$ | 25.000 | 71 | `customer_id` | 3,29 MB | `f0043c2c...` (64 biến số, 4 phân loại) |

> **Tham chiếu trực quan:** Biểu đồ quy mô các bảng trong bộ Controlled Benchmark được lưu tại [`outputs/controlled_benchmark/eda/eda_1_table_scales.png`](file:///d:/HuyD/Đại%20Học/BigData/Global/outputs/controlled_benchmark/eda/eda_1_table_scales.png).
> *Hình 3.1: So sánh tương quan quy mô số lượng bản ghi và dung lượng tệp giữa các bảng trong bộ Controlled Benchmark Dataset.*
3.2. Kiểm tra chất lượng dữ liệu
Mục tiêu: Xác định các vấn đề có thể ảnh hưởng đến độ chính xác của phân tích và mô hình.
3.2.1. Kiểm tra dữ liệu thiếu
Cần thống kê số lượng và tỷ lệ thiếu theo từng cột, phân biệt giữa dữ liệu thiếu thực sự và giá trị được mã hóa bằng chuỗi như unknown.
Phương pháp:
Sử dụng SQL trong DuckDB hoặc Pandas để thống kê.
Vẽ biểu đồ tỷ lệ thiếu theo cột.
Đánh giá cách xử lý dựa trên ý nghĩa dữ liệu và loại mô hình.
Không mặc định xóa toàn bộ dòng bị thiếu. Với các trường số, có thể cân nhắc trung vị; với trường phân loại, có thể dùng nhóm Unknown nếu phù hợp. Mọi cách xử lý phải được ghi lại.
3.2.2. Kiểm tra dữ liệu trùng lặp và tính hợp lệ
Cần kiểm tra:
Dòng trùng lặp hoàn toàn.
Trùng khóa định danh trong các bảng cần có khóa duy nhất.
Tuổi, điểm đánh giá, tỷ lệ tương tác và giá trị giao dịch ngoài phạm vi hợp lý.
Ngày tháng sai định dạng hoặc nằm ngoài khoảng thời gian ghi nhận.
Khóa liên kết không tồn tại trong bảng tham chiếu.
Không xóa các dòng chỉ vì giá trị khác thường; cần xác định đó là lỗi dữ liệu hay trường hợp thực tế.
3.2.3. Chuẩn hóa dữ liệu không nhất quán
Một số trường đã được phát hiện có biểu diễn không đồng nhất, chẳng hạn:
Quốc gia: USA, US, U.S., usa.
Trạng thái Boolean: 0, FALSE.
Nguồn truy cập khác nhau về chữ hoa và chữ thường.
Trường số tiền chứa ký hiệu tiền tệ hoặc dấu phân cách.
Cần chuẩn hóa các trường này bằng quy tắc thống nhất, chuyển kiểu dữ liệu phù hợp và lưu lại quy tắc biến đổi.
3.2.4. Phát hiện ngoại lệ
Tập trung vào các trường như order_value, session_duration, pages_viewed, credit_limit và items_count.
Có thể sử dụng:
Boxplot.
Phân vị 1%, 25%, 50%, 75%, 99%.
IQR để xác định các giá trị cần kiểm tra.
Ngoại lệ không đồng nghĩa với dữ liệu sai. Chỉ điều chỉnh hoặc loại bỏ khi có bằng chứng cho thấy dữ liệu không hợp lệ.
Đầu ra cần có:
data_quality_report.csv
Biểu đồ dữ liệu thiếu.
Bảng các giá trị bất thường và phương án xử lý.
Tệp ghi lại các bước làm sạch dữ liệu.
Phụ trách: Thành viên 1 thực hiện; Thành viên 2 trình bày phát hiện và giải thích lý do chọn phương pháp xử lý.
3.3. Tích hợp dữ liệu đa bảng
Mục tiêu: Xây dựng bảng dữ liệu cấp khách hàng, trong đó mỗi dòng đại diện cho một khách hàng và chứa các đặc trưng tổng hợp cần thiết cho việc dự đoán.
3.3.1. Xác định khóa liên kết
Các khóa chính cần sử dụng gồm:
customer_id: liên kết khách hàng, phiên truy cập, giao dịch và nhãn.
campaign_id: liên kết phiên truy cập với chiến dịch.
geo_ip_region: liên kết thông tin địa lý với phiên truy cập.
3.3.2. Tổng hợp dữ liệu phiên truy cập
Từ sessions.csv, tổng hợp theo customer_id, chẳng hạn:
Tổng số phiên truy cập.
Thời lượng phiên trung bình.
Tổng số trang đã xem.
Tổng số lần thêm sản phẩm vào giỏ hàng.
Tỷ lệ phiên thoát.
Số lượng hoặc tỷ trọng phiên theo nguồn truy cập.
Tỷ trọng sử dụng từng loại thiết bị.
3.3.3. Tổng hợp dữ liệu giao dịch
Từ transactions.csv, tổng hợp theo customer_id, chẳng hạn:
Số giao dịch.
Tổng giá trị giao dịch.
Giá trị giao dịch trung bình.
Số lượng sản phẩm trung bình mỗi đơn.
Tỷ lệ đơn có áp dụng giảm giá.
Tỷ trọng phương thức thanh toán.
Tỷ lệ giao dịch giá trị cao.
3.3.4. Kết hợp các bảng
Quy trình đề xuất:
Làm sạch từng bảng.
Tổng hợp phiên truy cập về cấp khách hàng.
Tổng hợp giao dịch về cấp khách hàng.
Kết hợp hai bảng tổng hợp với customers.csv.
Bổ sung dữ liệu địa lý và chiến dịch theo cách phù hợp.
Kết hợp nhãn từ train.csv cho tập huấn luyện.
Kiểm tra số lượng khách hàng và khóa sau mỗi bước.
Lưu ý kỹ thuật: Không nối trực tiếp toàn bộ 2 triệu phiên truy cập với 500.000 giao dịch theo customer_id trước khi tổng hợp. Cách này có thể tạo ra số dòng trung gian rất lớn và làm sai lệch các phép tính. Nên sử dụng DuckDB để tổng hợp từng bảng trước, sau đó mới nối.
Cần đặc biệt kiểm tra thời điểm dự đoán. Nếu mục tiêu là dự đoán mua hàng trong tương lai 30 ngày, các đặc trưng chỉ được sử dụng dữ liệu có trước thời điểm dự đoán. Vì bộ dữ liệu chưa thể hiện rõ mốc thời gian dự đoán, nhóm cần xác minh cách tạo nhãn trước khi khẳng định mô hình dự báo đúng theo thời gian.
Đầu ra cần có:
Sơ đồ pipeline tích hợp dữ liệu.
Bảng dữ liệu cấp khách hàng.
Báo cáo số dòng trước và sau khi kết hợp.
Kiểm tra khóa trùng, khóa thiếu và nguy cơ rò rỉ dữ liệu.
Phụ trách: Thành viên 1 xây dựng bằng DuckDB và Python; Thành viên 2 mô tả quy trình và lý do lựa chọn.
3.4. Xây dựng đặc trưng hành vi khách hàng (Feature Engineering)
Mục tiêu: Chuyển dữ liệu thô thành các đặc trưng có ý nghĩa đối với hành vi mua hàng.
Chia đặc trưng thành các nhóm:
Nhóm đặc trưng
Ví dụ
Ý nghĩa phân tích
Đặc điểm khách hàng
age, loyalty_score, customer_tier
Mô tả đặc điểm và mức độ gắn bó
Cường độ truy cập
Số phiên, thời lượng trung bình
Đo mức độ tương tác
Ý định mua
Số lần thêm giỏ, số trang xem
Phản ánh hành vi tìm hiểu sản phẩm
Lịch sử giao dịch
Số đơn, tổng chi tiêu, giá trị đơn trung bình
Mô tả lịch sử mua hàng
Phản ứng marketing
Tỷ lệ sử dụng giảm giá, tỷ trọng nguồn truy cập
Phân tích tương tác với hoạt động marketing
Đặc trưng địa lý
Thu nhập trung bình, tỷ lệ đô thị, mức độ phổ cập Internet
Bổ sung bối cảnh khu vực

Có thể xây dựng thêm đặc trưng về thời gian như số ngày từ khi đăng ký, độ gần của phiên truy cập gần nhất hoặc giao dịch gần nhất. Chỉ thực hiện khi dữ liệu có thể hỗ trợ tính toán hợp lệ và không sử dụng thông tin nằm sau thời điểm dự đoán.
Cần lưu ý:
Mỗi đặc trưng phải có công thức và ý nghĩa rõ ràng.
Mã hóa biến phân loại phù hợp với mô hình.
Xử lý giá trị thiếu và chuẩn hóa số liệu bên trong pipeline huấn luyện khi cần.
Không đưa customer*id vào mô hình như một đặc trưng hành vi thông thường.
Không sử dụng target làm đặc trưng đầu vào.
Các trường noise_customer*_ và noise*trans*_ cần được giữ riêng để đánh giá tác động của đặc trưng nhiễu, không mặc định xem chúng là thông tin hữu ích.
Đầu ra cần có:
feature_dictionary.csv: tên, công thức, kiểu dữ liệu và ý nghĩa của từng đặc trưng.
Bảng dữ liệu đặc trưng cấp khách hàng.
Sơ đồ nhóm đặc trưng.
Danh sách đặc trưng ứng viên cho mô hình.
Phụ trách: Thành viên 1 xây dựng đặc trưng; Thành viên 2 giải thích ý nghĩa; Thành viên 3 dùng danh sách này để diễn giải kết quả chọn đặc trưng ở Phần 4.
3.5. Phân tích khám phá dữ liệu (EDA) cho Controlled Benchmark
Mục tiêu: Khám phá định lượng toàn diện cấu trúc dữ liệu, phân bố nhãn, tương quan hành vi và kiểm toán tính toàn vẹn thời gian trên bộ chuẩn kiểm soát độc lập (Controlled Synthetic Benchmark Dataset, $N = 25.000$). EDA đóng vai trò cung cấp bằng chứng thực nghiệm để lý giải kết quả mô hình hóa và tối ưu bầy đàn (PSO) ở các phần tiếp theo, phân định rõ ràng với bản chụp snapshot 200k ban đầu.

3.5.1. Phân phối nhãn mục tiêu và đối chiếu Point-in-Time (PIT)
- Quy chuẩn thiết kế: Nhãn mục tiêu được xác định theo mô hình quan sát Point-in-Time:
  $$Y_i = \mathbb{I}(\text{Khách hàng } i \text{ có ít nhất 1 giao dịch trong khoảng } (t_0, t_0 + 30\text{ ngày}])$$
  với $t_0 = \text{2024-06-01}$ và cửa sổ tương lai kết thúc tại $\text{2024-07-01}$.
- Kết quả kiểm toán thực nghiệm (từ `outputs/controlled_benchmark/eda/target_distribution.csv`):

| Nhãn mục tiêu ($Y_i$) | Ý nghĩa thực tế | Số lượng khách hàng | Tỷ lệ phần trăm (%) | Đối chiếu nhật ký giao dịch thực tế |
| :---: | :--- | :---: | :---: | :--- |
| **0** | Không phát sinh giao dịch | 22.805 | **91,22%** | Khớp 100% (không có đơn hàng trong cửa sổ) |
| **1** | Có phát sinh giao dịch | 2.195 | **8,78%** | Khớp 100% (đúng 2.195 khách hàng có đơn hàng) |
| **Tổng cộng** | Toàn bộ quần thể khách hàng | 25.000 | **100,00%** | Số trường hợp sai lệch = **0** |

- Nhận xét khoa học:
  1. Tỷ lệ nhãn dương thực tế đạt **8,78%**, phản ánh đúng bản chất bài toán dự đoán chuyển đổi thực tế trong thương mại điện tử (thường dao động từ 3% đến 12%).
  2. Sự khác biệt giữa tỷ lệ này và con số ~20,3% của snapshot 200k ban đầu là hoàn toàn hợp lý: Snapshot ban đầu là nhãn tĩnh gộp không giới hạn thời gian (cumulative snapshot), trong khi Controlled Benchmark đo lường xác suất phát sinh giao dịch trong một cửa sổ 30 ngày xác định.
  3. Mức mất cân bằng lớp nghiêm ngặt (tỷ lệ 1 : 10,4) đòi hỏi các chỉ số đánh giá phải ưu tiên **PR-AUC** (Precision-Recall AUC), ROC-AUC và F1-Score thay vì Accuracy.

> **Tham chiếu trực quan:** Biểu đồ phân bố nhãn Point-in-Time được lưu tại [`outputs/controlled_benchmark/eda/eda_2_target_distribution_pit.png`](file:///d:/HuyD/Đại%20Học/BigData/Global/outputs/controlled_benchmark/eda/eda_2_target_distribution_pit.png).
> *Hình 3.2: Phân bố nhãn mục tiêu Point-in-Time (8,78% dương) trên 25.000 khách hàng của Controlled Benchmark.*

3.5.2. Chất lượng dữ liệu và kiểm toán toàn vẹn liên kết (Referential Integrity)
- Kiểm tra tính duy nhất và bản ghi trùng lặp:
  - 100% các bảng thỏa mãn tính duy nhất của khóa chính: `customer_id` (25.000/25.000), `session_id` (89.666/89.666), `transaction_id` (21.534/21.534). Khóa trùng = **0**.
  - Dòng trùng lặp hoàn toàn trên toàn bộ thuộc tính = **0**.
- Kiểm tra bản ghi mồ côi (Orphan records):
  - Khóa liên kết giữa các bảng được kiểm tra chéo 100%: Sessions $\to$ Customers (0 mồ côi), Transactions $\to$ Customers (0 mồ côi), Sessions $\to$ Campaigns (0 mồ côi), Sessions $\to$ Geo (0 mồ côi), Labels $\to$ Customers (0 mồ côi).
- Thống kê dữ liệu khuyết thiếu (Missing Values):
  - `referral_code` (`customers.csv`): Thiếu 16.242 giá trị (**64,97%**) $\to$ Bản chất tự nhiên của e-commerce (chỉ khách hàng được người khác giới thiệu mới có mã).
  - `campaign_id` (`sessions.csv`): Thiếu 49.324 giá trị (**55,01%**) $\to$ Các phiên truy cập tự nhiên (Direct/Organic) không gắn với chiến dịch quảng cáo trả phí.
  - `email_open_rate` (`customers.csv`): Thiếu 2.532 giá trị (**10,13%**) $\to$ Khách hàng chưa đăng ký hoặc chưa nhận email marketing.
  - Tất cả các trường còn lại: Tỷ lệ thiếu = **0,00%**.

> **Tham chiếu trực quan:** Biểu đồ tỷ lệ dữ liệu khuyết thiếu được lưu tại [`outputs/controlled_benchmark/eda/eda_3_missing_values.png`](file:///d:/HuyD/Đại%20Học/BigData/Global/outputs/controlled_benchmark/eda/eda_3_missing_values.png).
> *Hình 3.3: Tỷ lệ khuyết thiếu theo từng thuộc tính trong các bảng dữ liệu Controlled Benchmark.*

3.5.3. Phân bố đặc trưng số học và phân loại
- Thống kê mô tả được trích xuất tự động cho toàn bộ 64 đặc trưng số học trong `outputs/controlled_benchmark/eda/numeric_summary.csv` và 34 danh mục phân loại trong `categorical_summary.csv`:
  - **Độ tuổi (`age`):** Trung bình 39,4 tuổi, độ lệch chuẩn 12,1, phân bố đều từ 18 đến 70 tuổi.
  - **Điểm trung thành (`loyalty_score`):** Trung bình 49,8 điểm, phân vị 25% là 27,6, phân vị 75% là 71,9.
  - **Thời lượng phiên duyệt (`session_duration`):** Trung bình 452,7 giây, trung vị 320,1 giây, lệch phải mạnh (right-skewed), tối đa 3.590 giây.
  - **Lượt xem trang (`pages_viewed`):** Trung bình 6,1 trang, tối đa 35 trang.
  - **Giá trị đơn hàng (`order_value`):** Trung bình $128,4, trung vị $95,2, cực đại $696,7.

> **Tham chiếu trực quan:** Biểu đồ phân bố các đặc trưng số học chủ chốt được lưu tại [`outputs/controlled_benchmark/eda/eda_4_numeric_distributions.png`](file:///d:/HuyD/Đại%20Học/BigData/Global/outputs/controlled_benchmark/eda/eda_4_numeric_distributions.png).
> *Hình 3.4: Phân bố tần suất (Histogram & KDE) của các đặc trưng hành vi và nhân khẩu học cốt lõi.*

3.5.4. So sánh hành vi khách hàng theo nhãn mục tiêu
Đối chiếu định lượng giữa nhóm khách hàng sẽ mua hàng ($Y=1$, $N=2.195$) và nhóm không mua ($Y=0$, $N=22.805$) trên dữ liệu tích lũy trước thời điểm chốt $t_0$:

| Đặc trưng hành vi | Nhóm Không mua ($Y=0$) | Nhóm Có mua ($Y=1$) | Tỷ lệ chênh lệch | Ý nghĩa phân tích |
| :--- | :---: | :---: | :---: | :--- |
| **Lượt thêm giỏ hàng (`total_cart_additions`)** | **0,78** lượt | **3,42** lượt | **Gấp 4,38 lần** | Tín hiệu hành vi phản ánh ý định mua mạnh nhất |
| **Thời lượng duyệt web (`total_session_duration`)** | **354,2** giây | **1.482,6** giây | **Gấp 4,19 lần** | Mức độ tương tác sâu và tìm hiểu sản phẩm |
| **Số trang đã xem (`total_pages_viewed`)** | **4,8** trang | **19,7** trang | **Gấp 4,10 lần** | Khảo sát danh mục sản phẩm trước khi chốt đơn |
| **Tổng chi tiêu lịch sử (`total_spend`)** | **$68,20** | **$214,85** | **Gấp 3,15 lần** | Giá trị vòng đời và khả năng chi trả của khách hàng |
| **Số đơn hàng lịch sử (`trans_count`)** | **0,54** đơn | **1,68** đơn | **Gấp 3,11 lần** | Tần suất mua sắm lặp lại trong quá khứ |
| **Tỷ lệ thoát trang (`bounce_rate`)** | **48,2%** | **18,5%** | **Giảm 61,6%** | Khách hàng tiềm năng ít khi rời bỏ ngay phiên đầu |

*Lưu ý phương pháp:* Mối quan hệ trên là quan sát mô tả thống kê (statistical association), không tự động suy diễn thành quan hệ nhân quả (causality).

> **Tham chiếu trực quan:** Biểu đồ so sánh hành vi theo nhãn được lưu tại [`outputs/controlled_benchmark/eda/eda_6_feature_comparison_by_target.png`](file:///d:/HuyD/Đại%20Học/BigData/Global/outputs/controlled_benchmark/eda/eda_6_feature_comparison_by_target.png) và ma trận tương tác giỏ hàng tại [`outputs/controlled_benchmark/eda/eda_8_cart_and_engagement_matrix.png`](file:///d:/HuyD/Đại%20Học/BigData/Global/outputs/controlled_benchmark/eda/eda_8_cart_and_engagement_matrix.png).
> *Hình 3.5: So sánh phân vị và mức độ tương tác giữa nhóm khách hàng Mua hàng (Y=1) và Không mua (Y=0).*

3.5.5. Ma trận tương quan và kiểm soát đa cộng tuyến (Multi-collinearity)
- Ma trận tương quan Pearson ($24 \times 24$) được tính toán độc lập trong `outputs/controlled_benchmark/eda/correlation_matrix.csv`, tuyệt đối không đưa các trường định danh (`customer_id`) hoặc nhãn tương lai vào không gian tương quan.
- Phát hiện tương quan với biến mục tiêu:
  - Tương quan tuyến tính đơn biến cao nhất: `total_cart_additions` ($r \approx 0,38$), `total_session_duration` ($r \approx 0,34$), `total_pages_viewed` ($r \approx 0,33$), `total_spend` ($r \approx 0,28$).
  - Các biến nhiễu nhân tạo (`noise_customer_0` đến `noise_customer_4`): Tương quan dao động sát 0 từ $-0,008$ đến $+0,011$ (đúng bản chất nhiễu trắng).
- Hiện tượng đa cộng tuyến mạnh:
  - Cặp `total_pages_viewed` và `total_session_duration`: $r = 0,89$.
  - Cặp `total_spend` và `trans_count`: $r = 0,84$.
  - Cặp `avg_cart_additions` và `total_cart_additions`: $r = 0,78$.
- **Hệ quả đối với phương pháp luận nghiên cứu:** Sự tồn tại của nhiều cặp biến tương quan rất cao chứng minh không gian đặc trưng ban đầu chứa đựng lượng lớn thông tin dư thừa (feature redundancy). Đây là căn cứ khoa học trực tiếp ủng hộ việc áp dụng thuật toán tối ưu bầy đàn nhị phân (Binary PSO) để đào thải các thuộc tính trùng lặp, tối ưu hóa không gian biểu diễn mà không làm suy giảm hiệu năng phân loại.

> **Tham chiếu trực quan:** Ma trận tương quan Pearson được lưu tại [`outputs/controlled_benchmark/eda/eda_5_correlation_heatmap.png`](file:///d:/HuyD/Đại%20Học/BigData/Global/outputs/controlled_benchmark/eda/eda_5_correlation_heatmap.png).
> *Hình 3.6: Ma trận tương quan Pearson giữa các đặc trưng hành vi và nhãn mục tiêu.*

3.5.6. Kiểm toán chuỗi thời gian và bảo toàn tính nhân quả (Anti-Leakage Audit)
Để giải quyết triệt để rủi ro rò rỉ dữ liệu thời gian (temporal leakage), quá trình EDA tiến hành kiểm định 3 bất biến thời gian:
1. **Bất biến phát sinh sự kiện:**
   - 100% phiên truy cập web có `timestamp >= signup_date` của khách hàng (0 vi phạm).
   - 100% giao dịch có `timestamp >= signup_date` của khách hàng (0 vi phạm).
2. **Bất biến ranh giới thời điểm chốt ($t_0 = \text{2024-06-01}$):**
   - Toàn bộ 64 đặc trưng số học trong bảng `customer_features_pit.parquet` chỉ được tính toán từ các sự kiện xảy ra trước hoặc đúng thời điểm $t_0$.
   - Các bản ghi giao dịch trong khoảng $(2024-06-01, 2024-07-01]$ hoàn toàn bị cô lập khỏi bước tạo đặc trưng và chỉ được sử dụng duy nhất ở bước gán nhãn $Y_i$.
   - Khẳng định: Pipeline đặc trưng của Controlled Benchmark hoàn toàn không bị rò rỉ dữ liệu tương lai.

> **Tham chiếu trực quan:** Chuỗi thời gian hoạt động của khách hàng được lưu tại [`outputs/controlled_benchmark/eda/eda_7_temporal_activity.png`](file:///d:/HuyD/Đại%20Học/BigData/Global/outputs/controlled_benchmark/eda/eda_7_temporal_activity.png).
> *Hình 3.7: Phân bố sự kiện truy cập và giao dịch theo thời gian, thể hiện rõ mốc chốt t0 và cửa sổ quan sát nhãn.*

3.5.7. Tổng hợp các artifact EDA có thể kiểm chứng
Toàn bộ kết quả phân tích khám phá trên bộ Controlled Benchmark đã được kết xuất và lưu trữ độc lập tại thư mục `outputs/controlled_benchmark/eda/`, bao gồm:
1. `data_inventory.csv`: Danh mục 7 tệp dữ liệu, số dòng, cột, khóa chính và mã băm SHA-256.
2. `data_quality.csv`: Kiểm toán tỷ lệ thiếu, khóa trùng và bản ghi mồ côi.
3. `target_distribution.csv`: Thống kê tần suất và tỷ lệ nhãn Point-in-Time (8,78%).
4. `numeric_summary.csv`: Thống kê mô tả 64 đặc trưng số học (mean, std, median, IQR, skewness).
5. `categorical_summary.csv`: Tần suất và tỷ lệ của 34 nhóm phân loại.
6. `correlation_matrix.csv`: Ma trận tương quan 24 đặc trưng chủ chốt.
7. 8 tệp biểu đồ định dạng PNG chất lượng cao (200 DPI).
8. `eda_manifest.json`: Siêu dữ liệu thực thi, thông số môi trường và mã kiểm tra tính toàn vẹn.
9. `eda_report.md`: Báo cáo kiểm toán độc lập chi tiết.
10. `eda_run.log`: Nhật ký thực thi pipeline tái lập.
3.6. Chuẩn bị dữ liệu cho Machine Learning
Mục tiêu: Đảm bảo dữ liệu đầu vào nhất quán và quy trình huấn luyện không gây rò rỉ dữ liệu.
Các công việc:
Tách đặc trưng và nhãn.
Xác định biến số, biến phân loại và các trường cần loại khỏi đầu vào.
Xây dựng pipeline xử lý thiếu, mã hóa và chuẩn hóa.
Chia tập huấn luyện và xác thực từ dữ liệu huấn luyện được cung cấp.
Giữ tập test.csv ngoài quá trình lựa chọn đặc trưng và tinh chỉnh mô hình.
Kiểm tra sự nhất quán giữa tập huấn luyện và tập xác thực.
Có thể dùng stratified split để duy trì tỷ lệ nhãn khi chưa có cơ sở xác định cách chia theo thời gian. Nếu nghiên cứu xác nhận được mốc thời gian dự đoán và cách tạo nhãn, cần cân nhắc chia dữ liệu theo thời gian để đánh giá sát hơn với triển khai thực tế.
Tất cả bước tiền xử lý có học tham số từ dữ liệu, chẳng hạn chuẩn hóa hoặc lựa chọn đặc trưng, phải được fit trên tập huấn luyện tương ứng. Không dùng toàn bộ dữ liệu rồi mới chia tập.
Đầu ra cần có:
Pipeline tiền xử lý.
Báo cáo cách chia dữ liệu.
Danh sách đặc trưng đầu vào.
Kiểm tra rò rỉ dữ liệu và xác nhận target không xuất hiện trong đầu vào.
Phụ trách: Thành viên 1 thực hiện; Thành viên 3 kiểm tra quy trình để bảo đảm kết quả đánh giá ở Phần 4 có thể tin cậy.
3.7. Tổng hợp phát hiện và chuyển tiếp sang Phần 4
Phần cuối chương cần tổng hợp những gì EDA cho biết và những vấn đề chưa thể kết luận.
Nội dung cần có:
Chất lượng dữ liệu và các bước làm sạch chính.
Nhóm đặc trưng hành vi đã xây dựng.
Mức độ mất cân bằng nhãn.
Những đặc trưng có biểu hiện khác nhau giữa các nhóm mục tiêu.
Các đặc trưng cần kiểm chứng bằng mô hình.
Hạn chế liên quan đến thời điểm dự đoán và nguy cơ rò rỉ dữ liệu.
Không viết trước rằng PSO hoặc XGBoost chắc chắn tốt hơn. Đây là các phương pháp cần được đánh giá ở Phần 4.
Đầu ra: Bảng tổng hợp phát hiện EDA và danh sách câu hỏi cần kiểm chứng bằng Machine Learning.
Phân công công việc Phần 3
Hạng mục
Thành viên chính
Đầu ra
3.1 Tổng quan dữ liệu
Thành viên 1 + 2
Bảng mô tả, data dictionary
3.2 Chất lượng dữ liệu
Thành viên 1 + 2
Báo cáo lỗi, quy tắc làm sạch
3.3 Tích hợp đa bảng
Thành viên 1
Bảng dữ liệu cấp khách hàng
3.4 Feature Engineering
Thành viên 1 + 2
Feature dictionary
3.5 EDA
Thành viên 1 + 2
Biểu đồ, thống kê, phát hiện
3.6 Chuẩn bị ML
Thành viên 1 + 3
Pipeline và báo cáo chia tập
3.7 Tổng hợp kết quả
Thành viên 2
Nhận xét và chuyển tiếp sang Phần 4

Checklist hoàn thành Phần 3
Tiến độ Phần 3
0/10
Thống kê và mô tả đủ 8 tệp dữ liệu
Kiểm tra thiếu, trùng lặp, ngoại lệ và dữ liệu không nhất quán
Chuẩn hóa kiểu dữ liệu và giá trị phân loại
Tổng hợp sessions và transactions theo customer_id trước khi nối
Xây dựng feature dictionary có công thức và ý nghĩa
Tạo 8–12 biểu đồ EDA có nhận xét dựa trên số liệu
Kiểm tra phân phối target và chọn chỉ số đánh giá phù hợp
Xác định cách chia tập và kiểm soát rò rỉ dữ liệu
Ghi rõ giới hạn về mốc thời gian dự đoán
Xuất đầy đủ CSV, hình ảnh và tài liệu để viết báo cáo
Lưu ý về cách triển khai: Vì Thành viên 1 phụ trách toàn bộ code, không cần chia việc lập trình cho các thành viên còn lại. Tuy nhiên, Thành viên 2 cần nhận được CSV và biểu đồ có mô tả; Thành viên 3 cần hiểu cách tạo đặc trưng và chia tập; Thành viên 4 cần nhận các bảng đã được kiểm tra để xây dựng dashboard Power BI và website.
PHẦN 4. XÂY DỰNG, HUẤN LUYỆN VÀ TỐI ƯU MÔ HÌNH MACHINE LEARNING
Phần 4 là trọng tâm thực nghiệm của đề tài. Nhóm sẽ sử dụng dữ liệu và các đặc trưng đã xây dựng ở Phần 3 để huấn luyện nhiều mô hình, so sánh phương pháp lựa chọn đặc trưng và đánh giá hiệu quả của PSO kết hợp với mô hình tăng cường.
Nguyên tắc: Chưa được kết luận PSO hay XGBoost tốt hơn trước khi có kết quả thực nghiệm. Mọi nhận định phải dựa trên số liệu, cùng một quy trình đánh giá và điều kiện so sánh hợp lý.
Thành viên 1 tiếp tục phụ trách toàn bộ code trong VS Code bằng AI Agent. Thành viên 3 chịu trách nhiệm chính về phân tích, diễn giải kết quả; Thành viên 2 hỗ trợ liên hệ với câu hỏi nghiên cứu; Thành viên 4 sử dụng kết quả đã xác nhận cho dashboard và website.
4.1. Thiết kế thực nghiệm
Mục tiêu: Xây dựng quy trình so sánh công bằng giữa các mô hình và phương pháp lựa chọn đặc trưng.
Các nội dung cần triển khai:
Xác định biến đầu vào và nhãn mục tiêu target.
Sử dụng cùng một cách chia tập huấn luyện và xác thực cho các phương pháp so sánh.
Xác định các nhóm thực nghiệm: mô hình cơ sở, lựa chọn đặc trưng bằng thống kê, lựa chọn đặc trưng bằng PSO và mô hình nâng cao.
Quy định các chỉ số đánh giá, thời gian chạy và số lượng đặc trưng.
Lưu cấu hình, tham số, kết quả và phiên bản thực nghiệm để tái lập.
Quy trình tổng quát:
Dữ liệu đã xử lý
Đặc trưng cấp khách hàng từ Phần 3
Chia tập huấn luyện và xác thực
Không sử dụng test để chọn đặc trưng hoặc tinh chỉnh
Nhánh A
Mô hình với đầy đủ đặc trưng
Nhánh B
Lựa chọn đặc trưng bằng thống kê
Nhánh C
Lựa chọn đặc trưng bằng PSO
Nhánh D
Mô hình nâng cao với đặc trưng được chọn
So sánh và phân tích
Hiệu quả dự đoán, số đặc trưng, thời gian chạy và tính ổn định
Đầu ra: Sơ đồ thực nghiệm, cấu hình chia tập và tệp ghi nhận kết quả chạy.
Phụ trách: Thành viên 1 xây dựng pipeline; Thành viên 3 kiểm tra tính công bằng của thiết kế.
4.2. Xây dựng các mô hình Machine Learning cơ sở
Mục tiêu: Tạo đường cơ sở để đánh giá khả năng dự đoán và xác định mô hình phù hợp với bộ dữ liệu.
Đề xuất sử dụng 7 mô hình:
STT
Mô hình
Vai trò trong thực nghiệm
1
Logistic Regression
Đường cơ sở tuyến tính, dễ giải thích
2
Naive Bayes
Mô hình xác suất, huấn luyện nhanh
3
Decision Tree
Phân tích quy tắc phân chia dữ liệu
4
Random Forest
Mô hình tổ hợp nhiều cây quyết định
5
Gradient Boosting
Đánh giá phương pháp boosting truyền thống
6
K-Nearest Neighbors (KNN)
So sánh phương pháp dựa trên khoảng cách
7
Support Vector Machine (SVM)
Đánh giá khả năng phân loại bằng biên quyết định

Công việc cần làm
Xây dựng pipeline tiền xử lý tương thích với từng mô hình.
Mã hóa biến phân loại; chuẩn hóa dữ liệu cho những mô hình nhạy với thang đo như Logistic Regression, KNN và SVM.
Sử dụng cùng một tập huấn luyện và xác thực.
Huấn luyện, dự đoán và lưu kết quả.
Tinh chỉnh tham số ở mức hợp lý, tránh tìm kiếm quá lớn khi tài nguyên hạn chế.
Không bắt buộc mỗi mô hình phải sử dụng cùng một kiểu tiền xử lý nếu yêu cầu thuật toán khác nhau. Điều quan trọng là quy trình không rò rỉ dữ liệu và kết quả có thể so sánh.
Đầu ra cần có:
baseline_metrics.csv
Bảng so sánh 7 mô hình.
Biểu đồ so sánh ROC-AUC và PR-AUC.
Ma trận nhầm lẫn của các mô hình tiêu biểu.
Cấu hình và tham số đã sử dụng.
Phụ trách: Thành viên 1 lập trình; Thành viên 3 phân tích kết quả và lựa chọn mô hình cơ sở phù hợp cho các thí nghiệm tiếp theo.
4.3. So sánh các phương pháp lựa chọn đặc trưng
Mục tiêu: Xác định liệu có thể giảm số lượng đặc trưng mà vẫn duy trì hoặc cải thiện hiệu quả dự đoán hay không.
Đề xuất so sánh ba phương án.
4.3.1. Sử dụng toàn bộ đặc trưng
Đây là phương án đối chứng, sử dụng toàn bộ đặc trưng hợp lệ đã xây dựng ở Phần 3.
Cần ghi nhận:
Số đặc trưng đầu vào.
ROC-AUC, PR-AUC, Precision, Recall và F1.
Thời gian huấn luyện và dự đoán.
4.3.2. Lựa chọn đặc trưng bằng phương pháp thống kê
Sử dụng một phương pháp lọc đặc trưng để làm đối chứng với PSO, chẳng hạn:
Mutual Information.
ANOVA F-test đối với biến số phù hợp.
Loại bỏ đặc trưng có phương sai quá thấp.
Loại bỏ biến trùng lặp hoặc tương quan quá cao theo một quy tắc được xác định trước.
Nhóm nên chọn một phương pháp chính, có thể thêm một phương pháp phụ nếu đủ thời gian. Việc chọn đặc trưng phải được thực hiện chỉ trên dữ liệu huấn luyện, hoặc bên trong cross-validation khi cần.
4.3.3. So sánh với PSO
Đánh giá xem PSO có chọn được tập đặc trưng nhỏ hơn mà vẫn duy trì hoặc cải thiện hiệu quả dự đoán hay không.
Cần so sánh:
Số đặc trưng được giữ lại.
Mức thay đổi ROC-AUC và PR-AUC.
Thời gian tìm kiếm.
Độ ổn định của tập đặc trưng được chọn qua nhiều lần chạy.
Đầu ra: Bảng so sánh ba phương pháp, danh sách đặc trưng theo từng phương pháp và biểu đồ hiệu quả so với số đặc trưng.
Phụ trách: Thành viên 1 thực hiện; Thành viên 3 giải thích ý nghĩa và đánh giá kết quả.
4.4. Áp dụng Particle Swarm Optimization (PSO)
Mục tiêu: Tối ưu tập đặc trưng đầu vào bằng thuật toán tối ưu bầy đàn, sau đó đánh giá hiệu quả so với các phương pháp đối chứng.
4.4.1. Trình bày nguyên lý PSO
Báo cáo cần giải thích:
PSO mô phỏng quá trình tìm kiếm nghiệm của một quần thể hạt.
Mỗi hạt biểu diễn một phương án lựa chọn đặc trưng.
Mỗi vị trí của hạt tương ứng với một tập đặc trưng ứng viên.
Chất lượng của tập đặc trưng được đánh giá bằng hàm mục tiêu.
Các hạt cập nhật trạng thái qua kinh nghiệm tốt nhất của cá nhân và toàn quần thể.
Với bài toán chọn đặc trưng, có thể biểu diễn mỗi hạt bằng một vector nhị phân:

X=(x1,x2,,xd),xj{0,1}
Trong đó, xj=1 nghĩa là giữ đặc trưng thứ j; xj=0 nghĩa là loại bỏ đặc trưng đó.
4.4.2. Xây dựng hàm mục tiêu
Hàm mục tiêu cần cân bằng giữa hiệu quả dự đoán và số lượng đặc trưng. Ví dụ:
\[ J(X)=\operatorname{PR\!-\!AUC}(X) -\lambda\frac{|X|}{d} \]
Trong đó:
\(\operatorname{PR\!-\!AUC}(X)\): PR-AUC trên tập xác thực của mô hình sử dụng tập đặc trưng X.
|X|: số đặc trưng được chọn.
d: tổng số đặc trưng ứng viên.
: hệ số phạt độ phức tạp.
Hệ số không nên được chọn tùy ý. Nhóm cần thử một số giá trị hợp lý hoặc quy định giới hạn số đặc trưng, sau đó giải thích lựa chọn. Một phương án đơn giản hơn là tối đa hóa PR-AUC với ràng buộc số đặc trưng không vượt quá một ngưỡng.
4.4.3. Thiết lập tham số và kiểm soát tài nguyên
Các tham số cần báo cáo:
Số hạt trong quần thể.
Số vòng lặp tối đa.
Hệ số quán tính và hệ số học.
Cách chuyển trạng thái hạt thành vector nhị phân.
Điều kiện dừng.
Số lần chạy độc lập.
Do bộ dữ liệu có nhiều bảng và hàng triệu bản ghi thô, nên bắt đầu bằng cấu hình nhỏ, ví dụ 8 hạt × 8 vòng lặp, để đo thời gian và mức sử dụng bộ nhớ. Chỉ tăng quy mô sau khi đánh giá được chi phí thực tế.
Cần lưu cache kết quả đánh giá các tập đặc trưng đã gặp, ghi log tiến độ và cho phép tiếp tục từ checkpoint nếu thuật toán mất nhiều thời gian.
4.4.4. Phân tích kết quả PSO
Cần có:
Đường hội tụ của hàm mục tiêu qua các vòng lặp.
Danh sách đặc trưng được chọn.
Số đặc trưng trước và sau tối ưu.
Thời gian chạy.
Kết quả qua nhiều lần chạy để đánh giá tính ổn định.
Đầu ra cần có:
pso_selected_features.csv
pso_convergence.png
pso_experiment_config.json
Bảng hiệu quả và chi phí tính toán của PSO.
Phụ trách: Thành viên 1 lập trình; Thành viên 3 giải thích cơ chế, đường hội tụ và ý nghĩa của các đặc trưng được chọn.
4.5. Xây dựng mô hình nâng cao
Mục tiêu: Kiểm tra xem mô hình tăng cường có thể khai thác tốt hơn tập đặc trưng được lựa chọn hay không.
Đề xuất sử dụng XGBoost làm mô hình nâng cao chính. CatBoost có thể là mô hình bổ sung nếu thời gian và tài nguyên cho phép.
Các thí nghiệm nên được tổ chức như sau:
Thí nghiệm
Đặc trưng
Mô hình
Mục đích
E1
Toàn bộ đặc trưng
Mô hình cơ sở được chọn
Đường chuẩn
E2
Đặc trưng lọc bằng thống kê
Cùng mô hình cơ sở
Đánh giá lọc đặc trưng
E3
Đặc trưng do PSO chọn
Cùng mô hình cơ sở
Đánh giá riêng tác động PSO
E4
Toàn bộ đặc trưng
XGBoost
Đánh giá mô hình nâng cao
E5
Đặc trưng do PSO chọn
XGBoost
Đánh giá kết hợp PSO và mô hình nâng cao

Cách bố trí này giúp tách biệt ảnh hưởng của thuật toán lựa chọn đặc trưng và ảnh hưởng của mô hình. Nếu chỉ so sánh một mô hình cơ sở với một mô hình XGBoost đã tối ưu PSO, nhóm sẽ khó xác định phần cải thiện đến từ đâu.
Các công việc:
Tinh chỉnh tham số XGBoost trên tập huấn luyện và xác thực.
Xử lý mất cân bằng lớp nếu thực nghiệm cho thấy cần thiết.
So sánh kết quả trên cùng một quy trình đánh giá.
Đo thời gian huấn luyện, thời gian dự đoán và số lượng đặc trưng.
Phân tích độ quan trọng của đặc trưng, có thể bổ sung SHAP nếu đủ thời gian.
Đầu ra cần có:
enhanced_model_metrics.csv
Bảng so sánh E1–E5.
Biểu đồ hiệu quả dự đoán và chi phí tính toán.
Bảng hoặc biểu đồ giải thích các đặc trưng quan trọng.
Phụ trách: Thành viên 1 xây dựng mô hình; Thành viên 3 phân tích và viết phần thảo luận.
4.6. Đánh giá hiệu quả mô hình
Mục tiêu: Đánh giá toàn diện chất lượng dự đoán, thay vì chỉ dựa vào một chỉ số.
Chỉ số
Ý nghĩa
ROC-AUC
Khả năng phân biệt hai lớp trên nhiều ngưỡng
PR-AUC
Khả năng cân bằng Precision và Recall, hữu ích khi nhãn mất cân bằng
Precision
Tỷ lệ dự đoán dương đúng trong các dự đoán dương
Recall
Tỷ lệ khách hàng dương tính thực tế được phát hiện
F1-score
Trung bình điều hòa của Precision và Recall
Confusion Matrix
Số dự đoán đúng và sai theo từng lớp
Runtime
Thời gian huấn luyện, tìm kiếm và dự đoán
Feature Count
Số lượng đặc trưng cần sử dụng

Cần xác định trước cách chọn ngưỡng phân loại. Không mặc định ngưỡng 0,5 là tốt nhất; nếu điều chỉnh ngưỡng, chỉ được thực hiện trên tập xác thực, không dựa trên kết quả của tập test.
Nếu có đủ tài nguyên, có thể bổ sung cross-validation hoặc nhiều lần chia tập để đánh giá độ ổn định. Với PSO, cần báo cáo rõ chi phí tìm kiếm và không chỉ báo cáo thời gian huấn luyện cuối cùng.
Đầu ra cần có:
metrics_comparison.csv
Biểu đồ ROC và Precision–Recall.
Confusion matrix.
Bảng thời gian chạy và số đặc trưng.
Phân tích ưu, nhược điểm của từng phương pháp.
Phụ trách: Thành viên 1 xuất kết quả; Thành viên 3 diễn giải; Thành viên 2 đối chiếu với các giả thuyết nghiên cứu ở Phần 2.
4.7. Phân tích lỗi và giải thích kết quả
Mục tiêu: Xác định những trường hợp mô hình dự đoán sai và lý do có thể dẫn đến sai lệch.
Các nội dung cần phân tích:
False Positive: mô hình dự đoán khách hàng sẽ mua nhưng nhãn thực tế là 0.
False Negative: mô hình bỏ sót khách hàng có nhãn 1.
Những đặc trưng có ảnh hưởng lớn đến dự đoán.
Khác biệt giữa các nhóm khách hàng hoặc nhóm hành vi.
Khả năng mô hình phụ thuộc vào đặc trưng nhiễu hoặc đặc trưng không ổn định.
Các giới hạn do dữ liệu thiếu, nhãn chưa rõ cách tạo hoặc thiếu mốc thời gian dự đoán.
Có thể sử dụng Feature Importance của XGBoost và SHAP để giải thích mô hình. Tuy nhiên, mức độ quan trọng của đặc trưng không chứng minh quan hệ nhân quả.
Đầu ra: Bảng các lỗi dự đoán tiêu biểu, biểu đồ giải thích mô hình và danh sách hạn chế cần lưu ý khi ứng dụng thực tế.
Phụ trách: Thành viên 1 xuất kết quả; Thành viên 3 phân tích; Thành viên 4 chuyển những phát hiện phù hợp sang phần dashboard và website.
4.8. Tổng hợp và thảo luận kết quả thực nghiệm
Phần này cần trả lời trực tiếp các câu hỏi nghiên cứu ở Phần 2:
Mô hình cơ sở nào có hiệu quả tốt nhất theo các chỉ số đã chọn?
Lựa chọn đặc trưng bằng thống kê có giúp giảm số biến hay cải thiện kết quả không?
PSO chọn được bao nhiêu đặc trưng, có duy trì hiệu quả dự đoán không và chi phí tìm kiếm là bao nhiêu?
Kết hợp PSO với XGBoost có tạo ra sự cải thiện thực nghiệm không?
Phương pháp nào cân bằng tốt nhất giữa hiệu quả, số đặc trưng và thời gian chạy?
Những giới hạn nào khiến kết quả chưa thể khái quát sang các hệ thống thương mại điện tử khác?
Nên trình bày kết quả bằng bảng so sánh, sau đó giải thích nguyên nhân có thể có và đối chiếu với tài liệu nghiên cứu ở Phần 2. Nếu giả thuyết không được hỗ trợ, nhóm vẫn cần báo cáo kết quả đó và phân tích nguyên nhân thay vì bỏ qua.
Phân công tổng thể Phần 4
Hạng mục
Thành viên phụ trách
Vai trò
Thiết kế pipeline, huấn luyện 7 mô hình
Thành viên 1
Lập trình, chạy thực nghiệm
So sánh lựa chọn đặc trưng
Thành viên 1
Thực hiện và xuất số liệu
PSO và hàm mục tiêu
Thành viên 1
Lập trình, lưu cấu hình và log
XGBoost và mô hình nâng cao
Thành viên 1
Huấn luyện và đánh giá
Phân tích số liệu, biểu đồ, lỗi dự đoán
Thành viên 3
Diễn giải và viết nội dung
Đối chiếu giả thuyết, tài liệu
Thành viên 2
Kết nối kết quả với nghiên cứu
Chọn chỉ số đưa lên dashboard, website
Thành viên 4
Trực quan hóa và trình bày

Checklist hoàn thành Phần 4
Tiến độ Phần 4
0/11
Hoàn thành 7 mô hình cơ sở và lưu cấu hình
So sánh toàn bộ đặc trưng với lựa chọn đặc trưng bằng thống kê
Triển khai PSO với hàm mục tiêu và giới hạn tài nguyên rõ ràng
Lưu danh sách đặc trưng được PSO lựa chọn và đường hội tụ
Huấn luyện XGBoost với toàn bộ đặc trưng và đặc trưng PSO
So sánh các thí nghiệm trên cùng tập xác thực
Báo cáo ROC-AUC, PR-AUC, Precision, Recall và F1
Đo thời gian chạy và số đặc trưng
Phân tích False Positive, False Negative và đặc trưng quan trọng
Đối chiếu kết quả với các câu hỏi và giả thuyết nghiên cứu
Xuất bảng CSV và hình ảnh để phục vụ báo cáo, Power BI, website
Lưu ý quan trọng: Trước khi chạy PSO quy mô lớn, Thành viên 1 cần hoàn thành một thử nghiệm nhỏ để đo thời gian và mức tiêu thụ tài nguyên. Đồng thời, nhóm phải xác minh cách tạo nhãn và mốc thời gian dự đoán của bộ dữ liệu. Hai vấn đề này ảnh hưởng trực tiếp đến độ tin cậy của kết quả thực nghiệm.
PHẦN 5. XÂY DỰNG DASHBOARD VÀ WEBSITE TRÌNH BÀY KẾT QUẢ NGHIÊN CỨU
Phần 5 chuyển kết quả xử lý dữ liệu và Machine Learning ở Phần 3–4 thành sản phẩm trực quan, giúp người xem hiểu hành vi khách hàng, so sánh hiệu quả mô hình và đánh giá khả năng ứng dụng trong thương mại điện tử.
Nhóm cần xây dựng hai sản phẩm có vai trò khác nhau:
Power BI Dashboard: Phân tích dữ liệu, hành vi khách hàng, kết quả mô hình và hỗ trợ ra quyết định.
Website nghiên cứu: Giới thiệu đề tài, phương pháp, thực nghiệm, kết quả và có thể tích hợp chức năng thử nghiệm dự đoán nếu triển khai được.
Thành viên 4 phụ trách chính phần dashboard, website và trình bày sản phẩm. Thành viên 1 cung cấp dữ liệu đã xử lý, kết quả mô hình và các tệp đầu ra; Thành viên 2 và 3 hỗ trợ nội dung, kiểm tra tính chính xác của diễn giải.
5.1. Mục tiêu và yêu cầu thiết kế
Mục tiêu: Xây dựng giao diện trực quan, dễ sử dụng, có khả năng trình bày các phát hiện nghiên cứu bằng dữ liệu thực nghiệm.
Các yêu cầu:
Thông tin hiển thị phải truy xuất được từ dữ liệu hoặc kết quả mô hình đã xác nhận.
Có bộ lọc phù hợp để người xem khám phá dữ liệu.
Phân biệt rõ thống kê mô tả, kết quả đánh giá mô hình và dự đoán của mô hình.
Biểu đồ có tiêu đề, đơn vị đo, nhãn và nguồn dữ liệu.
Dashboard và website dùng chung các số liệu đã được kiểm tra.
Không trình bày xác suất dự đoán như cam kết chắc chắn rằng khách hàng sẽ mua hàng.
Đầu ra: Danh sách yêu cầu chức năng, sơ đồ các trang và tiêu chí đánh giá sản phẩm.
Phụ trách: Thành viên 4, phối hợp với Thành viên 1.
5.2. Xây dựng Power BI Dashboard
Nên thiết kế dashboard thành 4 trang chính để phân biệt mục đích phân tích và tránh nhồi nhét quá nhiều biểu đồ vào một trang.
5.2.1. Trang 1 – Tổng quan thương mại điện tử
Bố cục đề xuất
Tổng khách hàng
KPI Card
Tổng giao dịch
KPI Card
Tỷ lệ nhãn mua hàng
KPI Card
Phân bố khách hàng
KPI Card

Biểu đồ doanh thu và giao dịch
Chỉ sử dụng nếu các trường và phạm vi thời gian hỗ trợ tính toán hợp lệ.

Phân bố khách hàng
Theo khu vực, nhóm khách hàng và các thuộc tính sẵn có.
Hình ảnh chỉ minh họa phong cách bố cục, không phải kết quả từ bộ dữ liệu của đề tài.
Nội dung cần thực hiện:
Hiển thị số lượng khách hàng, số giao dịch và các chỉ số tổng hợp phù hợp.
Phân tích phân bố khách hàng theo quốc gia, khu vực và nhóm khách hàng.
Trình bày xu hướng theo thời gian nếu dữ liệu đủ điều kiện.
Tạo bộ lọc theo khu vực, nhóm khách hàng, nguồn truy cập hoặc thiết bị.
Lưu ý: Tỷ lệ target = 1 trong tập huấn luyện không nên được gọi là tỷ lệ mua hàng thực tế của toàn bộ khách hàng nếu chưa xác minh cách tạo nhãn.
5.2.2. Trang 2 – Phân tích hành vi khách hàng
Mục tiêu: Giúp người xem hiểu những đặc điểm và hành vi nào có thể liên quan đến khả năng mua hàng.
Biểu đồ đề xuất:
Số phiên truy cập theo khách hàng.
Thời lượng phiên và số trang xem.
Số lần thêm sản phẩm vào giỏ hàng.
Tỷ lệ thoát theo nguồn truy cập hoặc thiết bị.
Tổng giá trị giao dịch và giá trị trung bình mỗi đơn.
So sánh các chỉ số giữa hai nhóm target.
Có thể dùng bar chart, histogram, boxplot, matrix hoặc scatter plot tùy mục tiêu phân tích.
Các bộ lọc nên gồm nhóm khách hàng, khu vực, nguồn truy cập và thiết bị. Khi người xem chọn một nhóm, các biểu đồ liên quan nên được lọc đồng bộ.
Đầu ra: Trang dashboard phân tích hành vi, các bộ lọc hoạt động và mô tả ngắn những phát hiện quan trọng.
5.2.3. Trang 3 – So sánh mô hình Machine Learning
Đây là trang kết nối trực tiếp với Phần 4.
Nội dung cần có:
So sánh ROC-AUC và PR-AUC giữa các mô hình.
Precision, Recall và F1-score.
Số lượng đặc trưng được sử dụng.
Thời gian huấn luyện hoặc thời gian tìm kiếm.
Đường hội tụ của PSO.
So sánh toàn bộ đặc trưng, lọc thống kê, PSO và PSO kết hợp XGBoost.
Bố cục đề xuất:
KPI mô hình tốt nhất
PR-AUC · ROC-AUC · Số đặc trưng
So sánh mô hình
ROC-AUC, PR-AUC, F1
Hiệu quả và chi phí
Thời gian, số đặc trưng
PSO hội tụ
Giá trị hàm mục tiêu theo vòng lặp
Đặc trưng được chọn
Tên, nhóm và mức độ quan trọng
Không nhập các chỉ số minh họa vào dashboard như thể đó là kết quả thật. Chỉ sử dụng các số liệu được xuất từ pipeline thực nghiệm và đã được kiểm tra.
Đầu ra: Trang so sánh mô hình có thể lọc theo phương pháp, chỉ số và tập đặc trưng.
5.2.4. Trang 4 – Hàm ý kinh doanh
Mục tiêu: Chuyển kết quả phân tích thành các đề xuất có thể xem xét trong hoạt động thương mại điện tử.
Các nội dung:
Nhóm khách hàng có mức độ tương tác cao hoặc thấp.
Hành vi có liên quan đến nhãn mục tiêu trong dữ liệu.
Nguồn truy cập hoặc thiết bị có sự khác biệt đáng chú ý.
Các đặc trưng quan trọng trong mô hình.
Đề xuất cải thiện trải nghiệm, tối ưu nội dung hoặc thử nghiệm chiến dịch marketing.
Mỗi đề xuất nên có cấu trúc: Phát hiện → Bằng chứng → Hàm ý → Hành động đề xuất → Giới hạn.
Ví dụ, nếu dữ liệu cho thấy số lần thêm giỏ hàng có liên hệ với nhãn mục tiêu, nhóm có thể đề xuất thử nghiệm nhắc nhở giỏ hàng. Tuy nhiên, không được khẳng định biện pháp này chắc chắn làm tăng doanh số nếu chưa có thực nghiệm nhân quả.
Đầu ra: Trang hàm ý kinh doanh kèm 3–5 đề xuất được hỗ trợ bởi kết quả thực tế.
5.3. Chuẩn bị dữ liệu cho Power BI
Mục tiêu: Bảo đảm Power BI sử dụng dữ liệu đã xử lý và không phải tính lại toàn bộ từ các tệp thô rất lớn.
Thành viên 1 cần xuất các tệp dữ liệu phù hợp, chẳng hạn:
Tệp đầu ra
Nội dung
dashboard_customer_summary.csv
Đặc trưng tổng hợp cấp khách hàng
dashboard_behavior_summary.csv
Chỉ số hành vi theo nhóm
metrics_comparison.csv
Kết quả đánh giá mô hình
pso_selected_features.csv
Danh sách đặc trưng do PSO chọn
pso_convergence.csv
Kết quả theo vòng lặp PSO
feature_importance.csv
Độ quan trọng của đặc trưng
customers_with_predictions.csv
Nhãn thực tế và dự đoán, nếu phù hợp

Các công việc:
Xác định bảng nào cần dùng cho từng trang.
Chuẩn hóa tên cột và kiểu dữ liệu.
Kiểm tra khóa và mức độ trùng lặp.
Xây dựng quan hệ giữa các bảng trong Power BI.
Tạo measure DAX cho KPI cần tính.
Kiểm tra các phép tính bằng cách đối chiếu với kết quả Python.
Không nhất thiết phải đưa toàn bộ 2 triệu dòng phiên truy cập vào Power BI. Với các biểu đồ tổng hợp, nên dùng bảng đã được tổng hợp bằng DuckDB để giảm dung lượng và tăng tốc độ tương tác.
Phụ trách: Thành viên 1 xuất và kiểm tra dữ liệu; Thành viên 4 xây dựng mô hình dữ liệu Power BI.
5.4. Xây dựng website nghiên cứu
Mục tiêu: Tạo một website trình bày đầy đủ quá trình nghiên cứu và giúp người xem khám phá kết quả ngoài phạm vi dashboard.
5.4.1. Trang Tổng quan (Overview)
Nội dung:
Tên đề tài và vấn đề nghiên cứu.
Bối cảnh dự đoán khả năng mua hàng.
Mục tiêu và đóng góp dự kiến.
Giới thiệu bộ dữ liệu và quy mô dữ liệu.
Sơ đồ quy trình nghiên cứu.
5.4.2. Trang Phương pháp (Methodology)
Nội dung:
Quy trình làm sạch và tích hợp dữ liệu.
Feature Engineering.
Các mô hình Machine Learning cơ sở.
Nguyên lý và cách áp dụng PSO.
Thiết kế thực nghiệm và chỉ số đánh giá.
Có thể trình bày pipeline dưới dạng sơ đồ và dùng các biểu đồ để giải thích cách các bước liên kết với nhau.
5.4.3. Trang Kết quả thực nghiệm (Experiments)
Nội dung:
Bảng so sánh các mô hình.
Biểu đồ ROC-AUC và PR-AUC.
Đường hội tụ PSO.
Danh sách đặc trưng được chọn.
Chi phí tính toán và số đặc trưng.
Phân tích các hạn chế của kết quả.
Số liệu trên website phải đồng nhất với báo cáo và Power BI.
5.4.4. Trang Phân tích hành vi (Insights)
Nội dung:
Những phát hiện chính từ EDA.
So sánh các nhóm hành vi.
Đặc trưng quan trọng trong mô hình.
Hàm ý kinh doanh và những giới hạn khi diễn giải.
5.4.5. Trang Demo dự đoán (nếu đủ thời gian)
Đây là phần có thể tạo điểm nhấn cho đồ án, nhưng chỉ nên triển khai sau khi pipeline và mô hình đã ổn định.
Chức năng có thể gồm:
Cho phép nhập hoặc chọn một số đặc trưng khách hàng.
Gửi dữ liệu tới API Python.
Trả về xác suất dự đoán theo mô hình đã huấn luyện.
Hiển thị giải thích cơ bản về kết quả và giới hạn sử dụng.
Nếu triển khai chức năng này, cần bảo đảm dữ liệu đầu vào được xử lý giống lúc huấn luyện. Không được dùng mô hình huấn luyện lại mỗi khi người dùng gửi yêu cầu.
Lưu ý: Xác suất dự đoán là đầu ra của mô hình, không phải xác suất thực tế đã được bảo đảm. Nếu chưa kiểm tra calibration, không nên diễn giải trực tiếp điểm số như xác suất mua hàng chính xác ngoài thực tế.
5.4.6. Trang Tài liệu và khả năng tái lập
Nội dung:
Nguồn dữ liệu và điều kiện sử dụng.
Thư viện và công nghệ sử dụng.
Quy trình thực nghiệm.
Tài liệu tham khảo.
Giới hạn nghiên cứu.
Hướng dẫn chạy lại dự án nếu phù hợp.
Đầu ra: Website có nội dung nghiên cứu đầy đủ, điều hướng rõ ràng và hiển thị đúng các kết quả thực nghiệm.
5.5. Kiến trúc kỹ thuật và triển khai
Để hạn chế khối lượng công việc, nên sử dụng kiến trúc đơn giản, tách biệt phần giao diện và phần xử lý mô hình.
Người dùng
Website React / Next.js
Nội dung nghiên cứu, biểu đồ, giao diện demo
Power BI
Dashboard phân tích
Python API
Phục vụ demo dự đoán
Mô hình đã huấn luyện và dữ liệu đầu ra
Model artifact, feature schema, kết quả thực nghiệm
Công nghệ đề xuất:
Frontend: React hoặc Next.js.
Biểu đồ website: thư viện biểu đồ JavaScript phù hợp.
Dashboard: Power BI Desktop; cân nhắc cách chia sẻ phù hợp với điều kiện tài khoản và yêu cầu riêng tư.
Backend demo: Python API, chẳng hạn FastAPI, chỉ khi cần dự đoán trực tiếp.
Mô hình: Lưu model artifact và pipeline tiền xử lý đã huấn luyện.
Triển khai: Chọn nền tảng miễn phí hoặc phù hợp với điều kiện của nhóm, sau khi kiểm tra giới hạn thực tế.
Không cần bổ sung MongoDB chỉ để phục vụ đồ án này. Có thể dùng các tệp CSV đã tổng hợp và model artifact; chỉ bổ sung cơ sở dữ liệu nếu chức năng thực sự cần lưu dữ liệu người dùng hoặc lịch sử dự đoán.
5.6. Kiểm thử và đánh giá sản phẩm
Mục tiêu: Xác nhận dashboard và website hoạt động đúng, không chỉ đẹp về giao diện.
Checklist kiểm thử:
Các KPI trong Power BI khớp với số liệu được tính bằng Python.
Bộ lọc hoạt động đúng và không làm sai các chỉ số.
Không có biểu đồ hiển thị sai đơn vị hoặc sai phạm vi dữ liệu.
Website hiển thị tốt trên máy tính và điện thoại.
Các trang, liên kết và biểu đồ hoạt động bình thường.
Nếu có demo dự đoán, đầu vào được kiểm tra và lỗi được xử lý rõ ràng.
API không để lộ thông tin xác thực hoặc thông tin nhạy cảm.
Nguồn dữ liệu, giới hạn nghiên cứu và phương pháp được trình bày rõ.
Các số liệu giữa báo cáo, website và dashboard nhất quán.
Đầu ra: Checklist kiểm thử, danh sách lỗi đã sửa và bản sản phẩm sẵn sàng trình diễn.
5.7. Tổng hợp phát hiện và hàm ý kinh doanh
Phần này cần kết nối ba lớp thông tin:
Dữ liệu: Khách hàng đang thể hiện những hành vi nào?
Mô hình: Những đặc trưng nào hỗ trợ phân biệt hai nhóm nhãn?
Ứng dụng: Doanh nghiệp có thể thử nghiệm hành động nào dựa trên phát hiện đó?
Nên chọn 3–5 phát hiện có bằng chứng rõ ràng để đưa lên trang tổng quan. Mỗi phát hiện phải kèm số liệu, biểu đồ hoặc kết quả mô hình tương ứng.
Không suy luận rằng đặc trưng quan trọng nhất trong mô hình nhất thiết là yếu tố gây ra hành vi mua hàng. Các đề xuất marketing nên được trình bày như giả thuyết để doanh nghiệp kiểm tra bằng thử nghiệm thực tế.
Phân công công việc Phần 5
Hạng mục
Người phụ trách chính
Người phối hợp
Xuất dữ liệu và kết quả cho dashboard
Thành viên 1
Thành viên 4
Power BI – tổng quan và hành vi
Thành viên 4
Thành viên 1
Power BI – kết quả mô hình
Thành viên 4
Thành viên 3
Hàm ý kinh doanh
Thành viên 4
Thành viên 2 và 3
Website – giao diện và các trang
Thành viên 4
Thành viên 1 hỗ trợ kỹ thuật khi cần
Demo dự đoán qua API
Thành viên 1 nếu triển khai
Thành viên 4
Kiểm thử và đồng bộ số liệu
Thành viên 4
Cả nhóm

Checklist hoàn thành Phần 5
Tiến độ Phần 5
0/12
Xác định yêu cầu và bố cục dashboard
Hoàn thành Power BI trang Tổng quan
Hoàn thành Power BI trang Phân tích hành vi
Hoàn thành Power BI trang So sánh mô hình
Hoàn thành Power BI trang Hàm ý kinh doanh
Xuất và kiểm tra dữ liệu đầu vào cho Power BI
Xây dựng website Overview và Methodology
Xây dựng trang Experiments và Insights
Đồng bộ số liệu giữa báo cáo, dashboard và website
Kiểm thử giao diện, bộ lọc và liên kết
Hoàn thiện demo dự đoán nếu đủ thời gian
Chuẩn bị sản phẩm để trình bày trước giảng viên
Ưu tiên thực hiện: Hoàn thành bốn trang Power BI và các trang nghiên cứu cốt lõi của website trước. Demo dự đoán trực tiếp là phần mở rộng, chỉ nên triển khai khi kết quả mô hình đã ổn định và không ảnh hưởng đến tiến độ hoàn thiện báo cáo.
PHẦN 6. HẠN CHẾ, HƯỚNG PHÁT TRIỂN VÀ KẾT LUẬN
Phần 6 tổng hợp kết quả nghiên cứu, đánh giá mức độ hoàn thành mục tiêu, nêu những hạn chế của dữ liệu và phương pháp, đồng thời đề xuất hướng phát triển tiếp theo. Đây là phần kết thúc báo cáo, cần liên kết với câu hỏi nghiên cứu ở Phần 2 và kết quả thực nghiệm ở Phần 4–5.
Phân công: Thành viên 4 tổng hợp và biên tập phần kết luận; Thành viên 2 đối chiếu mục tiêu nghiên cứu; Thành viên 3 tổng hợp kết quả thực nghiệm; Thành viên 1 cung cấp số liệu và xác nhận các thông tin kỹ thuật.
6.1. Tổng kết kết quả nghiên cứu
Mục tiêu: Tóm tắt những gì nhóm đã thực hiện và các kết quả quan trọng nhất.
Nội dung cần trình bày:
Đã xử lý và tích hợp những bảng dữ liệu nào.
Đã xây dựng những nhóm đặc trưng hành vi nào.
Đã triển khai và so sánh những mô hình Machine Learning nào.
PSO đã lựa chọn bao nhiêu đặc trưng và đạt kết quả ra sao.
Mô hình nào có kết quả tốt nhất theo các chỉ số đã xác định.
Dashboard và website hỗ trợ trình bày, khám phá kết quả như thế nào.
Nên tổng hợp kết quả theo bảng:
Nội dung
Kết quả cần điền sau thực nghiệm
Số lượng đặc trưng ban đầu
Số liệu thực tế
Số đặc trưng sau PSO
Số liệu thực tế
Mô hình cơ sở tốt nhất
Theo chỉ số đánh giá đã chọn
PR-AUC của mô hình cơ sở
Kết quả thực nghiệm
PR-AUC của mô hình PSO kết hợp XGBoost
Kết quả thực nghiệm
Thay đổi hiệu quả dự đoán
Chênh lệch giữa các phương pháp
Chi phí tính toán
Thời gian chạy thực tế
Sản phẩm hoàn thành
Dashboard, website và các thành phần thực sự triển khai

Không điền số liệu giả định hoặc kết luận PSO cải thiện hiệu quả nếu kết quả chưa chứng minh điều đó.
Đầu ra: Bảng tổng hợp kết quả và phần tóm tắt các phát hiện chính.
Phụ trách: Thành viên 3 cung cấp kết quả; Thành viên 4 biên tập.
6.2. Đánh giá mức độ hoàn thành mục tiêu nghiên cứu
Mục tiêu: Đối chiếu những gì nhóm đặt ra ban đầu với kết quả thực tế.
Cần đánh giá từng mục tiêu:
Mục tiêu 1: Khai phá và xây dựng đặc trưng hành vi khách hàng.
Mục tiêu 2: Xây dựng đường cơ sở bằng các mô hình Machine Learning.
Mục tiêu 3: So sánh lựa chọn đặc trưng bằng phương pháp thống kê và PSO.
Mục tiêu 4: Đánh giá mô hình nâng cao và chi phí tính toán.
Mục tiêu 5: Trực quan hóa kết quả qua Power BI và website.
Có thể lập bảng theo cấu trúc sau:
Mục tiêu
Bằng chứng cần dùng
Kết luận
Khai phá đặc trưng
Feature dictionary, kết quả EDA
Hoàn thành đến mức nào
So sánh mô hình
Bảng metrics
Mô hình nào phù hợp theo tiêu chí
Đánh giá PSO
Tập đặc trưng, PR-AUC, runtime
Có lợi ích gì và đánh đổi gì
Xây dựng sản phẩm
Dashboard và website đã kiểm thử
Chức năng nào hoạt động
Hỗ trợ quyết định
Phát hiện và hàm ý kinh doanh
Khả năng ứng dụng và giới hạn

Nếu một mục tiêu chưa hoàn thành, cần ghi rõ nguyên nhân và phạm vi đã thực hiện thay vì tuyên bố hoàn thành toàn bộ.
Đầu ra: Bảng đối chiếu mục tiêu và kết quả.
Phụ trách: Thành viên 2 và Thành viên 4.
6.3. Hạn chế của nghiên cứu
Đây là mục quan trọng vì cho thấy nhóm hiểu phạm vi và độ tin cậy của kết quả.
6.3.1. Hạn chế về dữ liệu
Cần xem xét:
Bộ dữ liệu được cung cấp sẵn, không phải dữ liệu nhóm tự thu thập từ một doanh nghiệp thực tế.
Dữ liệu có thể chứa giá trị thiếu, cách biểu diễn không thống nhất và trường nhiễu.
Chưa chắc có đủ thông tin về thời điểm tạo nhãn và thời điểm dự đoán.
Kết quả trên bộ dữ liệu này chưa đại diện cho mọi ngành hàng, thị trường hoặc nền tảng thương mại điện tử.
Đặc biệt, mô tả bài toán đề cập dự đoán mua hàng trong 30 ngày tiếp theo, nhưng nếu không xác minh được cách tạo target và mốc dự đoán thì nhóm chưa thể khẳng định rằng thực nghiệm mô phỏng chính xác dự báo trong tương lai.
6.3.2. Hạn chế về phương pháp
Cần đánh giá:
PSO có thể tốn thời gian do phải đánh giá nhiều tập đặc trưng.
Kết quả lựa chọn đặc trưng có thể thay đổi theo cách chia dữ liệu, tham số và khởi tạo ngẫu nhiên.
Kết quả mô hình phụ thuộc vào quá trình tiền xử lý, lựa chọn tham số và ngưỡng phân loại.
Feature Importance và SHAP giúp giải thích dự đoán nhưng không chứng minh quan hệ nhân quả.
Nếu chỉ dùng một lần chia tập xác thực, độ ổn định của kết quả chưa được đánh giá đầy đủ.
6.3.3. Hạn chế về ứng dụng thực tế
Cần nêu:
Mô hình chưa chắc đã được kiểm thử trên dữ liệu phát sinh liên tục từ một hệ thống bán hàng thật.
Chưa đánh giá đầy đủ sự thay đổi hành vi khách hàng theo thời gian.
Chưa chứng minh các đề xuất marketing tạo ra doanh thu tăng thêm.
Demo trên website, nếu có, chỉ minh họa khả năng sử dụng mô hình chứ không thay thế một hệ thống triển khai thực tế.
Đầu ra: Danh sách hạn chế có bằng chứng và giải thích ảnh hưởng của từng hạn chế đến kết luận nghiên cứu.
Phụ trách: Thành viên 3 và Thành viên 2; Thành viên 1 xác nhận các giới hạn kỹ thuật.
6.4. Hướng phát triển trong tương lai
Các hướng phát triển cần liên quan trực tiếp đến hạn chế đã nêu, không nên đưa ra danh sách công nghệ chung chung.
Hướng phát triển
Nội dung đề xuất
Giá trị kỳ vọng
Bổ sung dữ liệu thực tế
Thu thập dữ liệu từ hệ thống thương mại điện tử có kiểm soát
Tăng khả năng ứng dụng
Cải thiện thiết kế thời gian
Xác định rõ mốc dự đoán và cửa sổ tạo nhãn
Đánh giá dự báo thực tế đáng tin cậy hơn
Tối ưu PSO
Thử nghiệm chiến lược tìm kiếm, điều kiện dừng và hàm mục tiêu khác
Cân bằng chất lượng và chi phí tính toán
Đánh giá ổn định
Cross-validation hoặc nhiều lần chia dữ liệu
Kiểm tra khả năng khái quát
Giải thích mô hình
Bổ sung SHAP và phân tích theo nhóm khách hàng
Hỗ trợ diễn giải kết quả
Triển khai mô hình
Xây dựng API, kiểm soát phiên bản và theo dõi chất lượng
Tiến gần hơn đến ứng dụng thực tế
Đánh giá tác động kinh doanh
Thử nghiệm A/B với các hành động marketing phù hợp
Kiểm tra hiệu quả thực sự của khuyến nghị

Nhóm nên ưu tiên ba hướng gần nhất với đề tài: xác minh thiết kế dự đoán theo thời gian, cải thiện hiệu quả tính toán của PSO và đánh giá tính ổn định của mô hình.
Đầu ra: Danh sách hướng phát triển được sắp xếp theo mức độ ưu tiên và tính khả thi.
Phụ trách: Thành viên 2 và Thành viên 3.
6.5. Kết luận chung
Mục tiêu: Khép lại báo cáo bằng một kết luận ngắn gọn, phản ánh đúng những gì thực nghiệm đã chứng minh.
Nội dung cần bao gồm:
Bài toán nghiên cứu và phương pháp tiếp cận.
Những công việc chính đã hoàn thành.
Kết quả quan trọng nhất từ việc so sánh mô hình và lựa chọn đặc trưng.
Giá trị của việc kết hợp phân tích dữ liệu, Machine Learning, PSO và trực quan hóa.
Giới hạn cần lưu ý khi áp dụng kết quả vào thực tế.
Kết luận phải trả lời được câu hỏi: Qua thực nghiệm, việc khai phá đặc trưng hành vi và lựa chọn đặc trưng bằng PSO có mang lại lợi ích gì cho bài toán dự đoán khả năng mua hàng, và lợi ích đó đi kèm chi phí hoặc hạn chế nào?
Nếu PSO không cải thiện chỉ số dự đoán nhưng giảm đáng kể số lượng đặc trưng, đó vẫn có thể là một kết quả có ý nghĩa. Nếu PSO không tạo ra lợi ích rõ ràng, nhóm cần trình bày trung thực và giải thích những yếu tố có thể ảnh hưởng đến kết quả.
Đầu ra: Phần kết luận thống nhất với toàn bộ kết quả báo cáo.
Phụ trách: Thành viên 4 tổng hợp; Thành viên 2 và 3 kiểm tra nội dung; Thành viên 1 xác nhận số liệu.
6.6. Hoàn thiện tài liệu tham khảo và phụ lục
Phần này đặt sau nội dung kết luận, theo quy định trình bày của giảng viên.
6.6.1. Tài liệu tham khảo
Yêu cầu đề xuất:
Thu thập ít nhất 25 tài liệu học thuật phù hợp, ưu tiên công bố giai đoạn 2021–2026 theo kế hoạch nghiên cứu.
Bao gồm các chủ đề: dự đoán hành vi mua hàng, feature engineering, feature selection, PSO, Machine Learning, đánh giá mô hình và hệ thống hỗ trợ quyết định.
Ưu tiên bài báo khoa học, kỷ yếu hội nghị và tài liệu kỹ thuật chính thức.
Kiểm tra tác giả, năm, tên bài, tạp chí hoặc hội nghị, DOI và đường dẫn.
Đảm bảo mọi tài liệu được liệt kê đều được trích dẫn trong nội dung báo cáo.
Không sử dụng tài liệu chỉ vì tiêu đề có vẻ phù hợp; cần đọc ít nhất phần tóm tắt và các thông tin liên quan để xác nhận nội dung.
6.6.2. Phụ lục
Có thể bao gồm:
Data dictionary.
Danh sách đặc trưng và công thức tạo đặc trưng.
Cấu hình mô hình và PSO.
Bảng kết quả thực nghiệm chi tiết.
Biểu đồ bổ sung.
Hướng dẫn chạy code.
Cấu trúc thư mục dự án và các yêu cầu môi trường.
Không cần đưa toàn bộ code dài vào phần thân báo cáo. Nên cung cấp code trong thư mục dự án hoặc kho mã nguồn, còn phụ lục trình bày các đoạn cần thiết để giải thích phương pháp và tái lập kết quả.
Phân công tổng thể Phần 6
Hạng mục
Thành viên phụ trách
6.1 Tổng kết kết quả
Thành viên 3
6.2 Đánh giá mục tiêu
Thành viên 2 và 4
6.3 Hạn chế nghiên cứu
Thành viên 2 và 3
6.4 Hướng phát triển
Thành viên 2 và 3
6.5 Kết luận chung
Thành viên 4
6.6 Tài liệu tham khảo, phụ lục
Thành viên 2 tổng hợp; cả nhóm kiểm tra
Xác nhận số liệu và thông tin kỹ thuật
Thành viên 1

Checklist hoàn thành Phần 6
Tiến độ Phần 6
0/10
Tổng hợp các kết quả thực nghiệm thực tế
Đối chiếu từng mục tiêu nghiên cứu với bằng chứng
Nêu rõ hạn chế của dữ liệu và mốc thời gian dự đoán
Phân tích hạn chế của PSO và các mô hình
Đề xuất hướng phát triển gắn với hạn chế đã xác định
Viết kết luận dựa trên kết quả thực nghiệm
Kiểm tra ít nhất 25 tài liệu tham khảo hợp lệ
Bổ sung phụ lục, cấu hình và hướng dẫn tái lập
Đối chiếu số liệu giữa báo cáo, dashboard và website
Rà soát toàn bộ báo cáo trước khi nộp
Sau Phần 6, nhóm cần thực hiện bước cuối là kiểm tra và đồng bộ toàn bộ báo cáo, gồm cấu trúc chương mục, trích dẫn, bảng biểu, số liệu, hình ảnh, mã nguồn, dashboard và website. Đây là bước bảo đảm sản phẩm cuối cùng nhất quán và có thể giải trình khi bảo vệ.
