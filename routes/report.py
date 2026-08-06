import os
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    send_file
)

from flask_login import (
    login_required,
    current_user
)

from services.report_service import ReportService
from services.analytics_service import AnalyticsService
from services.csv_service import CSVService
from services.pdf_service import PDFService
from services.export_history_service import ExportHistoryService


report_bp = Blueprint(
    "report",
    __name__,
    url_prefix="/reports"
)


# ==========================================================
# Reports Dashboard
# ==========================================================

@report_bp.route("/")
@login_required
def reports():

    # Read filters
    report_type = request.args.get("report_type", "inventory")
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")
    page = request.args.get("page", default=1, type=int)

    # High-level summaries
    summary = ReportService.get_report_summary(current_user.id)
    dashboard = ReportService.dashboard_summary(current_user.id)

    total_medicines = dashboard.get("total_medicines", 0)
    inventory_value = summary.get("inventory_value", 0.0)
    total_sales = summary.get("sales_value", 0.0)
    expired_count = dashboard.get("expired_medicines", 0)

    # parse optional date filters
    from_dt = None
    to_dt = None
    if from_date:
        try:
            from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        except Exception:
            from_dt = None

    if to_date:
        try:
            to_dt = datetime.strptime(to_date, "%Y-%m-%d")
        except Exception:
            to_dt = None

    # Report data selection
    reports = []
    pagination = None

    if report_type == "inventory":
        reports = ReportService.stock_report(current_user.id)

    elif report_type == "sales":
        reports = ReportService.sales_report(current_user.id, from_date=from_dt, to_date=to_dt)

    elif report_type == "purchase":
        reports = ReportService.purchase_report(current_user.id, from_date=from_dt, to_date=to_dt)

    elif report_type == "expiry":
        reports = ReportService.expiry_report(current_user.id, from_date=from_dt, to_date=to_dt)

    elif report_type == "low_stock":
        from services.inventory_service import InventoryService
        reports = InventoryService.low_stock(current_user.id)

    history = ExportHistoryService.recent_exports(current_user.id)

    return render_template(
        "reports/reports.html",
        reports=reports,
        pagination=pagination,
        total_medicines=total_medicines,
        inventory_value=inventory_value,
        total_sales=total_sales,
        expired_count=expired_count,
        selected_report_type=report_type,
        from_date=from_date,
        to_date=to_date,
        history=history,
    )


# ==========================================================
# Analytics Dashboard
# ==========================================================

@report_bp.route("/analytics")
@login_required
def analytics():

    analytics_data = AnalyticsService.get_dashboard_data(
        current_user.id
    )

    return render_template(
        "reports/analytics.html",
        analytics=analytics_data
    )


# ==========================================================
# Charts
# ==========================================================

@report_bp.route("/charts")
@login_required
def charts():

    chart_data = AnalyticsService.get_chart_data(
        current_user.id
    )

    return render_template(
        "reports/charts.html",
        charts=chart_data
    )


# ==========================================================
# Stock Report
# ==========================================================

@report_bp.route("/stock")
@login_required
def stock_report():

    stock = ReportService.stock_report(
        current_user.id
    )

    return render_template(
        "reports/reports.html",
        stock=stock
    )


# ==========================================================
# Expiry Report
# ==========================================================

@report_bp.route("/expiry")
@login_required
def expiry_report():

    expiry = ReportService.expiry_report(
        current_user.id
    )

    return render_template(
        "reports/reports.html",
        expiry=expiry
    )


# ==========================================================
# Sales Report
# ==========================================================

@report_bp.route("/sales")
@login_required
def sales_report():

    sales = ReportService.sales_report(
        current_user.id
    )

    return render_template(
        "reports/reports.html",
        sales=sales
    )


# ==========================================================
# Unified Export Handler
# ==========================================================

@report_bp.route("/export", endpoint="export_report")
@login_required
def export_report():
    export_format = request.args.get("format", "csv").lower()
    report_type = request.args.get("report_type", "inventory")
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")

    if export_format == "pdf":
        return export_pdf()
    elif export_format == "csv":
        return export_csv()
    return export_csv()


# ==========================================================
# Export Reports - CSV
# ==========================================================

@report_bp.route("/export/csv")
@login_required
def export_csv():

    report_type = request.args.get("report_type", "inventory")
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")

    file_path = CSVService.export_report(
        current_user.id,
        report_type=report_type,
        from_date=from_date,
        to_date=to_date
    )

    ExportHistoryService.log_export(
        current_user.id,
        report_type=report_type,
        file_type="csv",
        file_name=os.path.basename(file_path)
    )

    flash(
        "CSV Report Generated.",
        "success"
    )

    return send_file(
        file_path,
        as_attachment=True
    )


# ==========================================================
# Export Reports - EXCEL
# ==========================================================

@report_bp.route("/export/excel")
@login_required
def export_excel():

    report_type = request.args.get("report_type", "inventory")
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")

    file_path = CSVService.export_report_excel(
        current_user.id,
        report_type=report_type,
        from_date=from_date,
        to_date=to_date
    )

    ExportHistoryService.log_export(
        current_user.id,
        report_type=report_type,
        file_type="excel",
        file_name=os.path.basename(file_path)
    )

    flash(
        "Excel Report Generated.",
        "success"
    )

    return send_file(
        file_path,
        as_attachment=True
    )


# ==========================================================
# Export Reports - PDF
# ==========================================================

@report_bp.route("/export/pdf")
@login_required
def export_pdf():
    report_type = request.args.get("report_type", "inventory")
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")

    file_path = PDFService.export_report(
        current_user.id,
        report_type=report_type,
        from_date=from_date,
        to_date=to_date
    )

    ExportHistoryService.log_export(
        current_user.id,
        report_type=report_type,
        file_type="pdf",
        file_name=os.path.basename(file_path)
    )

    flash(
        "PDF Report Generated.",
        "success"
    )

    return send_file(
        file_path,
        as_attachment=True
    )