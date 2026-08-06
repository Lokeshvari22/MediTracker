from flask import (
    Blueprint,
    jsonify,
    request
)

from flask_login import (
    login_required,
    current_user
)

from services.inventory_service import InventoryService
from services.supplier_service import SupplierService
from services.sales_service import SalesService
from services.report_service import ReportService


api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


# ==========================================================
# Dashboard Metrics API
# ==========================================================

@api_bp.route("/dashboard")
@login_required
def dashboard_api():

    data = ReportService.dashboard_summary(
        current_user.id
    )

    return jsonify(data)


# ==========================================================
# Medicines API
# ==========================================================

@api_bp.route("/medicines")
@login_required
def medicines():

    medicines = InventoryService.list_all(
        current_user.id
    )

    return jsonify([
        medicine.to_dict()
        for medicine in medicines
    ])


# ==========================================================
# Medicine Details API
# ==========================================================

@api_bp.route("/medicines/<int:medicine_id>")
@login_required
def medicine_details(
    medicine_id
):

    medicine = InventoryService.get_medicine(
        medicine_id,
        current_user.id
    )

    if not medicine:

        return jsonify(
            {
                "success": False,
                "message": "Medicine not found."
            }
        ), 404

    return jsonify(
        medicine.to_dict()
    )


# ==========================================================
# Suppliers API
# ==========================================================

@api_bp.route("/suppliers")
@login_required
def suppliers():

    suppliers = SupplierService.list_all(
        current_user.id
    )

    return jsonify([
        supplier.to_dict()
        for supplier in suppliers
    ])


# ==========================================================
# Sales API
# ==========================================================

@api_bp.route("/sales")
@login_required
def sales():

    sales = SalesService.list_all(
        current_user.id
    )

    return jsonify([
        sale.to_dict()
        for sale in sales
    ])


# ==========================================================
# Search Medicines API
# ==========================================================

@api_bp.route("/search")
@login_required
def search():

    keyword = request.args.get(
        "keyword",
        ""
    )

    medicines = InventoryService.search(
        keyword=keyword,
        user_id=current_user.id
    )

    return jsonify([
        medicine.to_dict()
        for medicine in medicines
    ])


# ==========================================================
# Low Stock API
# ==========================================================

@api_bp.route("/low-stock")
@login_required
def low_stock():

    medicines = InventoryService.low_stock(
        current_user.id
    )

    return jsonify([
        medicine.to_dict()
        for medicine in medicines
    ])


# ==========================================================
# Expiring Medicines API
# ==========================================================

@api_bp.route("/expiring")
@login_required
def expiring():

    medicines = InventoryService.expiring(
        days=30,
        user_id=current_user.id
    )

    return jsonify([
        medicine.to_dict()
        for medicine in medicines
    ])


# ==========================================================
# Transaction Summary API
# ==========================================================

@api_bp.route("/summary")
@login_required
def summary():

    data = ReportService.transaction_summary(
        current_user.id
    )

    return jsonify(data)