"""
tests/test_deliverables_and_web_assets.py
Kiểm tra tính vẹn toàn của các sản phẩm bàn giao cuối cùng:
1. Website nghiên cứu 6 trang trong web/
2. Dữ liệu web/data/metrics.json khớp 100% với metrics_comparison.csv
3. Báo cáo nghiên cứu Word (.docx) và Markdown (.md)
4. Hồ sơ đặc tả Power BI và 6 tệp CSV xuất bản
"""

import os
import json
import pytest
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(PROJECT_ROOT, "web")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")


def test_web_portal_files_and_pages_structure():
    """Kiểm tra website tồn tại đủ các file và 6 trang view bắt buộc."""
    index_html = os.path.join(WEB_DIR, "index.html")
    style_css = os.path.join(WEB_DIR, "css", "style.css")
    app_js = os.path.join(WEB_DIR, "js", "app.js")
    metrics_json = os.path.join(WEB_DIR, "data", "metrics.json")

    assert os.path.exists(index_html), "Thiếu web/index.html"
    assert os.path.exists(style_css), "Thiếu web/css/style.css"
    assert os.path.exists(app_js), "Thiếu web/js/app.js"
    assert os.path.exists(metrics_json), "Thiếu web/data/metrics.json"

    with open(index_html, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Kiểm tra đủ 6 trang theo DanY6Phan.md Mục 5.4
    expected_pages = [
        "page-overview",
        "page-methodology",
        "page-experiments",
        "page-insights",
        "page-demo",
        "page-docs"
    ]
    for page_id in expected_pages:
        assert f'id="{page_id}"' in html_content, f"Thiếu trang {page_id} trong web/index.html"

    # Kiểm tra các ID điều khiển demo dự đoán
    assert 'id="demo-cart"' in html_content
    assert 'id="demo-pages"' in html_content
    assert 'id="demo-score-text"' in html_content


def test_web_metrics_json_integrity_matches_canonical_models():
    """Kiểm tra metrics.json hiển thị trên web khớp 100% với ground truth metrics_comparison.csv."""
    metrics_json_path = os.path.join(WEB_DIR, "data", "metrics.json")
    metrics_csv_path = os.path.join(OUTPUTS_DIR, "metrics", "metrics_comparison.csv")

    assert os.path.exists(metrics_json_path)
    assert os.path.exists(metrics_csv_path)

    with open(metrics_json_path, "r", encoding="utf-8") as f:
        web_data = json.load(f)

    df_metrics = pd.read_csv(metrics_csv_path)
    xgb_row = df_metrics[df_metrics["model_name"] == "XGBoost (Full Features)"].iloc[0]

    # Kiểm tra Confusion matrix trong metrics.json
    cm = web_data["holdout_confusion_matrix"]
    assert cm["true_negatives"] == int(xgb_row["true_negatives"]) == 15740
    assert cm["false_positives"] == int(xgb_row["false_positives"]) == 9763
    assert cm["false_negatives"] == int(xgb_row["false_negatives"]) == 3078
    assert cm["true_positives"] == int(xgb_row["true_positives"]) == 3419
    assert abs(cm["pr_auc"] - float(xgb_row["pr_auc"])) < 1e-4


def test_research_reports_docx_and_md_exist_and_complete():
    """Kiểm tra báo cáo nghiên cứu hoàn chỉnh có cả bản Word .docx và Markdown .md."""
    md_path = os.path.join(DOCS_DIR, "BaoCao_NghienCuu_Global_6Phan.md")
    docx_path = os.path.join(DOCS_DIR, "BaoCao_NghienCuu_Global_6Phan.docx")

    assert os.path.exists(md_path), "Thiếu báo cáo docs/BaoCao_NghienCuu_Global_6Phan.md"
    assert os.path.exists(docx_path), "Thiếu báo cáo docs/BaoCao_NghienCuu_Global_6Phan.docx"

    # Kiểm tra kích thước tệp lớn, đầy đủ nội dung
    assert os.path.getsize(md_path) > 40000, "Báo cáo Markdown quá ngắn"
    assert os.path.getsize(docx_path) > 30000, "Báo cáo Word .docx quá nhỏ"

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Kiểm tra 6 phần chính trong báo cáo Markdown
    assert "PHẦN 1. GIỚI THIỆU NGHIÊN CỨU" in md_text
    assert "PHẦN 2. CÂU HỎI VÀ PHƯƠNG PHÁP NGHIÊN CỨU" in md_text
    assert "PHẦN 3. XỬ LÝ DỮ LIỆU VÀ PHÂN TÍCH KHÁM PHÁ (EDA)" in md_text
    assert "PHẦN 4. MACHINE LEARNING VÀ TỐI ƯU LỰA CHỌN ĐẶC TRƯNG" in md_text
    assert "PHẦN 5. XÂY DỰNG DASHBOARD VÀ WEBSITE TRÌNH BÀY KẾT QUẢ NGHIÊN CỨU" in md_text
    assert "PHẦN 6. HẠN CHẾ, HƯỚNG PHÁT TRIỂN VÀ KẾT LUẬN" in md_text
    assert "TÀI LIỆU THAM KHẢO" in md_text


def test_power_bi_specifications_and_exports_exist():
    """Kiểm tra tài liệu đặc tả Power BI và 6 tệp dữ liệu xuất bản."""
    spec_path = os.path.join(DOCS_DIR, "POWER_BI_SPECIFICATION.md")
    schema_path = os.path.join(DOCS_DIR, "DATA_MODEL_SCHEMA.md")
    pbi_dir = os.path.join(OUTPUTS_DIR, "powerbi")

    assert os.path.exists(spec_path), "Thiếu docs/POWER_BI_SPECIFICATION.md"
    assert os.path.exists(schema_path), "Thiếu docs/DATA_MODEL_SCHEMA.md"
    assert os.path.exists(pbi_dir), "Thiếu outputs/powerbi"

    expected_pbi_csvs = [
        "dashboard_customer_summary.csv",
        "dashboard_behavior_summary.csv",
        "metrics_comparison.csv",
        "pso_selected_features.csv",
        "pso_convergence.csv",
        "feature_importance.csv"
    ]
    for csv_file in expected_pbi_csvs:
        p = os.path.join(pbi_dir, csv_file)
        assert os.path.exists(p), f"Thiếu tệp Power BI CSV: {csv_file}"
        assert os.path.getsize(p) > 0, f"Tệp Power BI rỗng: {csv_file}"
