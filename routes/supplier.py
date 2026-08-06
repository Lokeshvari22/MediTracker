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

from services.supplier_service import SupplierService


supplier_bp = Blueprint(
    "supplier",
    __name__,
    url_prefix="/suppliers"
)


# ==========================================================
# List Suppliers
# ==========================================================

@supplier_bp.route("/")
@login_required
def suppliers():

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    status = request.args.get(
        "status",
        ""
    ).strip().lower()

    if status not in ("active", "inactive"):
        status = ""

    total_suppliers = SupplierService.total_suppliers(
        current_user.id
    )

    active_suppliers = SupplierService.total_active_suppliers(
        current_user.id
    )

    total_medicines = SupplierService.total_medicines_supplied(
        current_user.id
    )

    if search:

        suppliers = SupplierService.search_suppliers(
            keyword=search,
            user_id=current_user.id,
            status=status
        )

        return render_template(
            "suppliers/suppliers.html",
            suppliers=suppliers,
            search=search,
            status=status,
            total_suppliers=total_suppliers,
            active_suppliers=active_suppliers,
            total_medicines=total_medicines
        )

    pagination = SupplierService.list_suppliers(
        user_id=current_user.id,
        page=page,
        per_page=10,
        status=status
    )

    return render_template(
        "suppliers/suppliers.html",
        suppliers=pagination.items,
        pagination=pagination,
        search=search,
        status=status,
        total_suppliers=total_suppliers,
        active_suppliers=active_suppliers,
        total_medicines=total_medicines
    )


# ==========================================================
# Add Supplier
# ==========================================================

@supplier_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_supplier():

    if request.method == "POST":

        try:

            data = {
                "name": request.form.get(
                    "supplier_name",
                    ""
                ).strip(),
                "company_name": request.form.get(
                    "company_name",
                    ""
                ).strip(),
                "gst_number": request.form.get(
                    "gst_number",
                    ""
                ).strip(),
                "supplier_type": request.form.get(
                    "supplier_type",
                    ""
                ).strip(),
                "website": request.form.get(
                    "website",
                    ""
                ).strip(),
                "contact_person": request.form.get(
                    "contact_person",
                    ""
                ).strip(),
                "email": request.form.get(
                    "email",
                    ""
                ).strip(),
                "phone": request.form.get(
                    "phone",
                    ""
                ).strip(),
                "address": request.form.get(
                    "address",
                    ""
                ).strip(),
                "city": request.form.get(
                    "city",
                    ""
                ).strip(),
                "state": request.form.get(
                    "state",
                    ""
                ).strip(),
                "postal_code": request.form.get(
                    "postal_code",
                    ""
                ).strip(),
                "country": request.form.get(
                    "country",
                    "India"
                ).strip(),
                "is_active": request.form.get(
                    "is_active",
                    "1"
                ),
                "notes": request.form.get(
                    "notes",
                    ""
                ).strip()
            }

            SupplierService.add_supplier(
                data=data,
                user_id=current_user.id
            )

            flash(
                "Supplier added successfully.",
                "success"
            )

            return redirect(
                url_for("supplier.suppliers")
            )

        except Exception as e:

            flash(
                f"Unable to add supplier. {e}",
                "danger"
            )

    return render_template(
        "suppliers/add_supplier.html"
    )


# ==========================================================
# Edit Supplier
# ==========================================================

@supplier_bp.route(
    "/edit/<int:supplier_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_supplier(supplier_id):

    supplier = SupplierService.get_supplier(
        supplier_id,
        current_user.id
    )

    if not supplier:

        flash(
            "Supplier not found.",
            "warning"
        )

        return redirect(
            url_for("supplier.suppliers")
        )

    if request.method == "POST":

        try:

            data = {
                "name": request.form.get(
                    "supplier_name",
                    ""
                ).strip(),
                "company_name": request.form.get(
                    "company_name",
                    ""
                ).strip(),
                "gst_number": request.form.get(
                    "gst_number",
                    ""
                ).strip(),
                "supplier_type": request.form.get(
                    "supplier_type",
                    ""
                ).strip(),
                "website": request.form.get(
                    "website",
                    ""
                ).strip(),
                "contact_person": request.form.get(
                    "contact_person",
                    ""
                ).strip(),
                "email": request.form.get(
                    "email",
                    ""
                ).strip(),
                "phone": request.form.get(
                    "phone",
                    ""
                ).strip(),
                "address": request.form.get(
                    "address",
                    ""
                ).strip(),
                "city": request.form.get(
                    "city",
                    ""
                ).strip(),
                "state": request.form.get(
                    "state",
                    ""
                ).strip(),
                "postal_code": request.form.get(
                    "postal_code",
                    ""
                ).strip(),
                "country": request.form.get(
                    "country",
                    "India"
                ).strip(),
                "is_active": request.form.get(
                    "is_active",
                    "1"
                ),
                "notes": request.form.get(
                    "notes",
                    ""
                ).strip()
            }

            SupplierService.update_supplier(
                supplier,
                data
            )

            flash(
                "Supplier updated successfully.",
                "success"
            )

            return redirect(
                url_for("supplier.suppliers")
            )

        except Exception as e:

            flash(
                f"Unable to update supplier. {e}",
                "danger"
            )

    return render_template(
        "suppliers/edit_supplier.html",
        supplier=supplier
    )


# ==========================================================
# Delete Supplier
# ==========================================================

@supplier_bp.route(
    "/delete/<int:supplier_id>",
    methods=["POST"]
)
@login_required
def delete_supplier(supplier_id):

    supplier = SupplierService.get_supplier(
        supplier_id,
        current_user.id
    )

    if not supplier:

        flash(
            "Supplier not found.",
            "warning"
        )

        return redirect(
            url_for("supplier.suppliers")
        )

    try:

        SupplierService.delete_supplier(
            supplier
        )

        flash(
            "Supplier deleted successfully.",
            "success"
        )

    except Exception as e:

        flash(
            f"Unable to delete supplier. {e}",
            "danger"
        )

    return redirect(
        url_for("supplier.suppliers")
    )