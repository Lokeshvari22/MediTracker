from datetime import datetime, date, timedelta

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

from models.medicine import Medicine
from models.expired_medicine import ExpiredMedicine
from services.expiry_service import ExpiryService
from services.inventory_service import InventoryService


# ==========================================================
# Medicine Blueprint
# ==========================================================

medicine_bp = Blueprint(
    "medicine",
    __name__,
    url_prefix="/medicines"
)


# ==========================================================
# List Medicines
# ==========================================================

@medicine_bp.route("/")
@login_required
def medicines():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()

    category = request.args.get(
        "category",
        "",
        type=str
    ).strip()

    per_page = 10

    if search:

        pagination = InventoryService.search(
            search,
            current_user.id,
            page=page,
            per_page=per_page
        )

    elif category:

        pagination = InventoryService.filter_category(
            category,
            current_user.id,
            page=page,
            per_page=per_page
        )

    else:

        pagination = InventoryService.list_medicines(
            current_user.id,
            page=page,
            per_page=per_page
        )

    return render_template(
        "medicines/medicines.html",
        medicines=pagination.items,
        pagination=pagination,
        search=search,
        category=category
    )


# ==========================================================
# Add Medicine
# ==========================================================

@medicine_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_medicine():

    if request.method == "POST":

        try:

            raw_expiry = request.form.get(
                "expiry_date"
            )

            parsed_expiry = (
                datetime.strptime(
                    raw_expiry,
                    "%Y-%m-%d"
                ).date()
                if raw_expiry
                else None
            )

            data = {

                "name": request.form.get(
                    "name",
                    ""
                ).strip(),

                "batch_number": request.form.get(
                    "batch_number",
                    ""
                ).strip(),

                "category": request.form.get(
                    "category",
                    ""
                ).strip(),

                "quantity": int(
                    request.form.get(
                        "quantity",
                        0
                    )
                ),

                "price": float(
                    request.form.get(
                        "price",
                        0
                    )
                ),

                "expiry_date": parsed_expiry,

                "low_stock_alert": int(
                    request.form.get(
                        "low_stock_alert",
                        10
                    )
                )
            }

            InventoryService.add_medicine(
                data=data,
                user_id=current_user.id
            )

            flash(
                "Medicine added successfully.",
                "success"
            )

            return redirect(
                url_for("medicine.medicines")
            )

        except Exception as e:

            flash(
                f"Unable to add medicine. {e}",
                "danger"
            )

    return render_template(
        "medicines/add_medicine.html"
    )


# ==========================================================
# Edit Medicine
# ==========================================================

@medicine_bp.route(
    "/edit/<int:medicine_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_medicine(medicine_id):

    medicine = InventoryService.get_medicine(
        medicine_id,
        current_user.id
    )

    if not medicine:

        flash(
            "Medicine not found.",
            "warning"
        )

        return redirect(
            url_for("medicine.medicines")
        )

    if request.method == "POST":

        try:

            raw_expiry = request.form.get(
                "expiry_date"
            )

            parsed_expiry = (
                datetime.strptime(
                    raw_expiry,
                    "%Y-%m-%d"
                ).date()
                if raw_expiry
                else None
            )

            data = {

                "name": request.form.get(
                    "name",
                    ""
                ).strip(),

                "batch_number": request.form.get(
                    "batch_number",
                    ""
                ).strip(),

                "category": request.form.get(
                    "category",
                    ""
                ).strip(),

                "quantity": int(
                    request.form.get(
                        "quantity",
                        0
                    )
                ),

                "price": float(
                    request.form.get(
                        "price",
                        0
                    )
                ),

                "expiry_date": parsed_expiry,

                "low_stock_alert": int(
                    request.form.get(
                        "low_stock_alert",
                        10
                    )
                )
            }

            InventoryService.update_medicine(
                medicine,
                data
            )

            flash(
                "Medicine updated successfully.",
                "success"
            )

            return redirect(
                url_for("medicine.medicines")
            )

        except Exception as e:

            flash(
                f"Unable to update medicine. {e}",
                "danger"
            )

    return render_template(
        "medicines/edit_medicine.html",
        medicine=medicine
    )


# ==========================================================
# Delete Medicine
# ==========================================================

@medicine_bp.route(
    "/delete/<int:medicine_id>",
    methods=["POST"]
)
@login_required
def delete_medicine(medicine_id):

    medicine = InventoryService.get_medicine(
        medicine_id,
        current_user.id
    )

    if not medicine:

        flash(
            "Medicine not found.",
            "warning"
        )

        return redirect(
            url_for("medicine.medicines")
        )

    try:

        InventoryService.delete_medicine(
            medicine
        )

        flash(
            "Medicine deleted successfully.",
            "success"
        )

    except Exception as e:

        flash(
            f"Unable to delete medicine. {e}",
            "danger"
        )

    return redirect(
        url_for("medicine.medicines")
    )


# ==========================================================
# Low Stock Medicines
# ==========================================================

@medicine_bp.route("/low-stock")
@login_required
def low_stock_medicines():

    medicines = InventoryService.low_stock(
        current_user.id
    )

    return render_template(
        "medicines/medicines.html",
        medicines=medicines,
        pagination=None,
        search="",
        category="",
        low_stock=True
    )


# ==========================================================
# Expiring / Expired Medicines
# ==========================================================

@medicine_bp.route("/expiring")
@login_required
def expiring_medicines():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()

    status = request.args.get(
        "status",
        "",
        type=str
    )

    days = request.args.get(
        "days",
        30,
        type=int
    )

    today = date.today()

    future = today + timedelta(
        days=days
    )

    # ------------------------------------------------------
    # Current inventory medicines that are expired
    # or expiring soon
    # ------------------------------------------------------

    query = Medicine.query.filter(
        Medicine.user_id == current_user.id,
        Medicine.expiry_date.isnot(None),
        Medicine.expiry_date <= future
    )

    # ------------------------------------------------------
    # Status filter
    # ------------------------------------------------------

    if status == "expired":

        query = query.filter(
            Medicine.expiry_date < today
        )

    elif status == "soon":

        query = query.filter(
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future
        )

    # ------------------------------------------------------
    # Search filter
    # ------------------------------------------------------

    if search:

        query = query.filter(
            (Medicine.name.ilike(
                f"%{search}%"
            )) |
            (Medicine.batch_number.ilike(
                f"%{search}%"
            ))
        )

    medicines = query.order_by(
        Medicine.expiry_date.asc()
    ).all()

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    expired_count = len(
        ExpiryService.expired_medicines(
            current_user.id
        )
    )

    expiring_count = ExpiryService.total_expiring(
        current_user.id,
        days=days
    )

    total_medicines = Medicine.query.filter_by(
        user_id=current_user.id
    ).count()

    safe_count = max(
        total_medicines
        - expired_count
        - expiring_count,
        0
    )

    # ------------------------------------------------------
    # Archived expired medicines
    # ------------------------------------------------------

    archived_records = ExpiredMedicine.query.filter_by(
        user_id=current_user.id
    ).order_by(
        ExpiredMedicine.expired_date.desc()
    ).all()

    return render_template(
        "medicines/expired.html",

        medicines=medicines,

        archived_records=archived_records,

        days=days,

        search=search,

        status=status,

        expired_count=expired_count,

        expiring_count=expiring_count,

        total_medicines=total_medicines,

        safe_count=safe_count
    )


# ==========================================================
# Move Expired Medicines
# ==========================================================

@medicine_bp.route("/move-expired")
@login_required
def move_expired_medicines():

    try:

        moved = InventoryService.move_expired(
            current_user.id
        )

        flash(
            f"{moved} expired medicines moved successfully.",
            "success"
        )

    except Exception as e:

        flash(
            f"Unable to move expired medicines. {e}",
            "danger"
        )

    return redirect(
        url_for("medicine.expiring_medicines")
    )


# ==========================================================
# Archive One Expired Medicine
# ==========================================================

@medicine_bp.route(
    "/archive/<int:medicine_id>",
    methods=["POST"]
)
@login_required
def archive_medicine(medicine_id):

    try:

        ExpiryService.archive_medicine(
            user_id=current_user.id,
            medicine_id=medicine_id
        )

        flash(
            "Medicine archived successfully.",
            "success"
        )

    except Exception as e:

        flash(
            f"Unable to archive medicine. {e}",
            "danger"
        )

    return redirect(
        url_for("medicine.expiring_medicines")
    )


# ==========================================================
# Delete Archived Medicine
# ==========================================================

@medicine_bp.route(
    "/archive/delete/<int:expired_id>",
    methods=["POST"]
)
@login_required
def delete_archived_medicine(expired_id):

    try:

        ExpiryService.delete_archived_record(
            user_id=current_user.id,
            expired_id=expired_id
        )

        flash(
            "Archived record deleted successfully.",
            "success"
        )

    except Exception as e:

        flash(
            f"Unable to delete archived record. {e}",
            "danger"
        )

    return redirect(
        url_for("medicine.expiring_medicines")
    )
