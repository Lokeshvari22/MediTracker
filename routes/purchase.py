from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from services.inventory_service import InventoryService
from services.supplier_service import SupplierService
from services.sales_service import PurchaseService


purchase_bp = Blueprint(
    "purchase",
    __name__,
    url_prefix="/purchases"
)


# ==========================================================
# Purchase List
# ==========================================================

@purchase_bp.route("/")
@login_required
def purchases():

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    supplier = request.args.get(
        "supplier",
        ""
    ).strip()

    from_date = request.args.get(
        "from_date",
        ""
    ).strip()

    to_date = request.args.get(
        "to_date",
        ""
    ).strip()

    pagination = PurchaseService.list_purchases(
        user_id=current_user.id,
        page=page,
        per_page=10,
        search=search,
        supplier=supplier,
        from_date=from_date,
        to_date=to_date
    )

    suppliers = SupplierService.list_all(
        current_user.id
    )

    return render_template(
        "purchases/purchases.html",
        purchases=pagination.items,
        pagination=pagination,
        suppliers=suppliers,
        search=search,
        selected_supplier=supplier,
        from_date=from_date,
        to_date=to_date,
        total_purchases=PurchaseService.total_purchases(current_user.id),
        today_purchases=PurchaseService.today_purchases(current_user.id),
        total_quantity=PurchaseService.total_purchase_quantity(current_user.id),
        total_value=PurchaseService.total_purchase_cost(current_user.id)
    )


# ==========================================================
# Add Purchase
# ==========================================================

@purchase_bp.route(
    "/add",
    methods=["GET", "POST"]
)
@login_required
def add_purchase():

    medicines = InventoryService.list_all(
        current_user.id
    )

    suppliers = SupplierService.list_all(
        current_user.id
    )

    if request.method == "POST":

        try:

            data = {

                "medicine_id": int(
                    request.form.get(
                        "medicine_id"
                    )
                ),

                "supplier_id": int(
                    request.form.get(
                        "supplier_id"
                    )
                ),

                "quantity": int(
                    request.form.get(
                        "quantity"
                    )
                ),

                "purchase_price": float(
                    request.form.get(
                        "purchase_price"
                    )
                ),

                "discount": float(
                    request.form.get(
                        "discount",
                        0
                    ) or 0
                ),

                "gst": float(
                    request.form.get(
                        "gst",
                        0
                    ) or 0
                ),

                "total_amount": float(
                    request.form.get(
                        "total_amount",
                        0
                    ) or 0
                ),

                "payment_method": request.form.get(
                    "payment_method",
                    "Cash"
                ).strip(),

                "status": request.form.get(
                    "status",
                    "Paid"
                ).strip(),

                "notes": request.form.get(
                    "notes",
                    ""
                ).strip(),

                "invoice_number": request.form.get(
                    "invoice_number",
                    ""
                ).strip(),

                "purchase_date": request.form.get(
                    "purchase_date"
                )

            }

            PurchaseService.create_purchase(
                data=data,
                user_id=current_user.id
            )

            flash(
                "Purchase recorded successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "purchase.purchases"
                )
            )

        except Exception as e:

            flash(
                f"Unable to save purchase. {e}",
                "danger"
            )

    return render_template(
        "purchases/add_purchase.html",
        medicines=medicines,
        suppliers=suppliers
    )


# ==========================================================
# Purchase Details
# ==========================================================

@purchase_bp.route(
    "/<int:purchase_id>"
)
@login_required
def purchase_details(
    purchase_id
):

    purchase = PurchaseService.get_purchase(
        purchase_id,
        current_user.id
    )

    if not purchase:

        flash(
            "Purchase not found.",
            "warning"
        )

        return redirect(
            url_for(
                "purchase.purchases"
            )
        )

    return render_template(
        "purchases/purchase_details.html",
        purchase=purchase
    )


# ==========================================================
# Delete Purchase
# ==========================================================

@purchase_bp.route(
    "/delete/<int:purchase_id>",
    methods=["POST"]
)
@login_required
def delete_purchase(
    purchase_id
):

    purchase = PurchaseService.get_purchase(
        purchase_id,
        current_user.id
    )

    if not purchase:

        flash(
            "Purchase not found.",
            "warning"
        )

        return redirect(
            url_for(
                "purchase.purchases"
            )
        )

    try:

        PurchaseService.delete_purchase(
            purchase
        )

        flash(
            "Purchase deleted successfully.",
            "success"
        )

    except Exception as e:

        flash(
            f"Unable to delete purchase. {e}",
            "danger"
        )

    return redirect(
        url_for(
            "purchase.purchases"
        )
    )