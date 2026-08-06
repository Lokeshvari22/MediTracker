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

from services.sales_service import SalesService
from services.inventory_service import InventoryService


sales_bp = Blueprint(
    "sales",
    __name__,
    url_prefix="/sales"
)


# ==========================================================
# Sales List
# ==========================================================

@sales_bp.route("/")
@login_required
def sales():

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    customer = request.args.get("customer", "").strip()

    from_date = request.args.get("from_date", "")

    to_date = request.args.get("to_date", "")

    pagination = SalesService.list_sales(
        user_id=current_user.id,
        page=page,
        per_page=10,
        search=search,
        customer=customer,
        from_date=from_date,
        to_date=to_date
    )

    return render_template(
        "sales/sales.html",
        sales=pagination.items,
        pagination=pagination,
        search=search
        ,
        customer=customer,
        from_date=from_date,
        to_date=to_date,
        total_sales=SalesService.total_sales(current_user.id),
        today_sales=SalesService.today_sales(current_user.id),
        total_revenue=SalesService.total_revenue(current_user.id),
        total_profit=SalesService.total_profit(current_user.id)
    )


# ==========================================================
# Sell Medicine
# ==========================================================

@sales_bp.route(
    "/sell",
    methods=["GET", "POST"]
)
@login_required
def sell_medicine():

    medicines = InventoryService.list_available(
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

                "quantity": int(
                    request.form.get(
                        "quantity"
                    )
                ),

                "sale_price": float(
                    request.form.get(
                        "sale_price",
                        0
                    ) or 0
                ),
                "discount": float(request.form.get("discount", 0) or 0),
                "gst": float(request.form.get("gst", 0) or 0),
                "total_amount": request.form.get("total_amount", "") or "",

                "customer_name": request.form.get(
                    "customer_name",
                    ""
                ).strip(),

                "customer_phone": request.form.get(
                    "customer_phone",
                    ""
                ).strip()

            }

            sale = SalesService.create_sale(
                data=data,
                user_id=current_user.id
            )

            flash(
                "Sale completed successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "sales.invoice",
                    sale_id=sale.id
                )
            )

        except Exception as e:

            flash(
                f"Unable to complete sale. {e}",
                "danger"
            )

    return render_template(
        "sales/sell_medicine.html",
        medicines=medicines
    )


# ==========================================================
# Invoice
# ==========================================================

@sales_bp.route(
    "/invoice/<int:sale_id>"
)
@login_required
def invoice(sale_id):

    sale = SalesService.get_sale(
        sale_id,
        current_user.id
    )

    if not sale:

        flash(
            "Invoice not found.",
            "warning"
        )

        return redirect(
            url_for("sales.sales")
        )

    return render_template(
        "sales/invoice.html",
        sale=sale
    )


# ==========================================================
# Delete Sale
# ==========================================================

@sales_bp.route(
    "/delete/<int:sale_id>",
    methods=["POST"]
)
@login_required
def delete_sale(sale_id):

    sale = SalesService.get_sale(
        sale_id,
        current_user.id
    )

    if not sale:

        flash(
            "Sale not found.",
            "warning"
        )

        return redirect(
            url_for("sales.sales")
        )

    try:

        SalesService.delete_sale(
            sale
        )

        flash(
            "Sale deleted successfully.",
            "success"
        )

    except Exception as e:

        flash(
            f"Unable to delete sale. {e}",
            "danger"
        )

    return redirect(
        url_for("sales.sales")
    )