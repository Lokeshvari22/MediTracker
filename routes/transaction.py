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
from services.csv_service import CSVService
from services.pdf_service import PDFService


transaction_bp = Blueprint(
    "transaction",
    __name__,
    url_prefix="/transactions"
)


# ==========================================================
# Transaction History
# ==========================================================

@transaction_bp.route("/")
@login_required
def transactions():

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    transaction_type = request.args.get(
        "transaction_type",
        ""
    ).strip()

    from_date = request.args.get(
        "from_date",
        ""
    )

    to_date = request.args.get(
        "to_date",
        ""
    )

    pagination = ReportService.get_transactions(
        user_id=current_user.id,
        page=page,
        per_page=10,
        search=search,
        transaction_type=transaction_type,
        from_date=from_date,
        to_date=to_date
    )

    summary = ReportService.transaction_summary(
        current_user.id
    )

    return render_template(
        "transactions/transactions.html",
        transactions=pagination.items,
        pagination=pagination,
        search=search,
        selected_type=transaction_type,
        from_date=from_date,
        to_date=to_date,
        stock_in_count=summary.get("stock_in_count", 0),
        stock_out_count=summary.get("stock_out_count", 0),
        sales_count=summary.get("sales_count", 0),
        purchase_count=summary.get("purchase_count", 0)
    )


# ==========================================================
# Export CSV
# ==========================================================

@transaction_bp.route("/export/csv")
@login_required
def export_csv():

    filepath = CSVService.export_transactions(
        current_user.id
    )

    flash(
        "CSV exported successfully.",
        "success"
    )

    return send_file(
        filepath,
        as_attachment=True
    )


# ==========================================================
# Export Excel
# ==========================================================

@transaction_bp.route("/export/excel")
@login_required
def export_excel():

    filepath = CSVService.export_transactions_excel(
        current_user.id
    )

    flash(
        "Excel exported successfully.",
        "success"
    )

    return send_file(
        filepath,
        as_attachment=True
    )


# ==========================================================
# Export PDF
# ==========================================================

@transaction_bp.route("/export/pdf")
@login_required
def export_pdf():

    filepath = PDFService.export_transactions(
        current_user.id
    )

    flash(
        "PDF exported successfully.",
        "success"
    )

    return send_file(
        filepath,
        as_attachment=True
    )