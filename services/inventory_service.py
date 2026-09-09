from datetime import date, timedelta

from database.database import db

from models.medicine import Medicine
from models.expired_medicine import ExpiredMedicine


class InventoryService:

    # ==================================================
    # Add Medicine
    # ==================================================

    @staticmethod
    def add_medicine(data, user_id):

        name = str(data.get("name", "")).strip()
        batch_number = str(
            data.get("batch_number", "")
        ).strip()
        category = str(
            data.get("category", "")
        ).strip()

        if not name:
            raise ValueError(
                "Medicine name is required."
            )

        if not batch_number:
            raise ValueError(
                "Batch number is required."
            )

        if not category:
            raise ValueError(
                "Category is required."
            )

        try:
            quantity = int(
                data.get("quantity", 0)
            )
        except (TypeError, ValueError):
            raise ValueError(
                "Quantity must be a valid number."
            )

        if quantity < 0:
            raise ValueError(
                "Quantity cannot be negative."
            )

        try:
            price = float(
                data.get("price", 0)
            )
        except (TypeError, ValueError):
            raise ValueError(
                "Price must be a valid number."
            )

        if price < 0:
            raise ValueError(
                "Price cannot be negative."
            )

        try:
            low_stock_alert = int(
                data.get(
                    "low_stock_alert",
                    10
                )
            )
        except (TypeError, ValueError):
            raise ValueError(
                "Low stock alert must be a valid number."
            )

        if low_stock_alert < 1:
            raise ValueError(
                "Low stock alert must be at least 1."
            )

        expiry_date = data.get(
            "expiry_date"
        )

        # ----------------------------------------------
        # Duplicate batch check per user
        # ----------------------------------------------

        existing = Medicine.query.filter_by(
            batch_number=batch_number,
            user_id=user_id
        ).first()

        if existing:
            raise ValueError(
                f"Batch number '{batch_number}' "
                "already exists."
            )

        medicine = Medicine(
            name=name,
            batch_number=batch_number,
            category=category,
            quantity=quantity,
            price=price,
            expiry_date=expiry_date,
            low_stock_alert=low_stock_alert,
            user_id=user_id
        )

        db.session.add(medicine)
        db.session.commit()

        return medicine

    # ==================================================
    # Get Medicine
    # ==================================================

    @staticmethod
    def get_medicine(
        medicine_id,
        user_id
    ):

        return Medicine.query.filter_by(
            id=medicine_id,
            user_id=user_id
        ).first()

    # ==================================================
    # Update Medicine
    # ==================================================

    @staticmethod
    def update_medicine(
        medicine,
        data
    ):

        name = str(
            data.get("name", "")
        ).strip()

        batch_number = str(
            data.get("batch_number", "")
        ).strip()

        category = str(
            data.get("category", "")
        ).strip()

        if not name:
            raise ValueError(
                "Medicine name is required."
            )

        if not batch_number:
            raise ValueError(
                "Batch number is required."
            )

        if not category:
            raise ValueError(
                "Category is required."
            )

        # ----------------------------------------------
        # Check duplicate batch during edit
        # ----------------------------------------------

        existing = Medicine.query.filter(
            Medicine.user_id == medicine.user_id,
            Medicine.batch_number == batch_number,
            Medicine.id != medicine.id
        ).first()

        if existing:
            raise ValueError(
                f"Batch number '{batch_number}' "
                "already exists."
            )

        try:
            quantity = int(
                data.get("quantity", 0)
            )
        except (TypeError, ValueError):
            raise ValueError(
                "Quantity must be a valid number."
            )

        if quantity < 0:
            raise ValueError(
                "Quantity cannot be negative."
            )

        try:
            price = float(
                data.get("price", 0)
            )
        except (TypeError, ValueError):
            raise ValueError(
                "Price must be a valid number."
            )

        if price < 0:
            raise ValueError(
                "Price cannot be negative."
            )

        try:
            low_stock_alert = int(
                data.get(
                    "low_stock_alert",
                    medicine.low_stock_alert
                )
            )
        except (TypeError, ValueError):
            raise ValueError(
                "Low stock alert must be a valid number."
            )

        if low_stock_alert < 1:
            raise ValueError(
                "Low stock alert must be at least 1."
            )

        medicine.name = name
        medicine.batch_number = batch_number
        medicine.category = category
        medicine.quantity = quantity
        medicine.price = price
        medicine.expiry_date = data.get(
            "expiry_date"
        )
        medicine.low_stock_alert = low_stock_alert

        db.session.commit()

        return medicine

    # ==================================================
    # Delete Medicine
    # ==================================================

    @staticmethod
    def delete_medicine(
        medicine
    ):

        db.session.delete(medicine)
        db.session.commit()

    # ==================================================
    # List Medicines
    # ==================================================

    @staticmethod
    def list_medicines(
        user_id,
        page=1,
        per_page=10
    ):

        return Medicine.query.filter_by(
            user_id=user_id
        ).order_by(
            Medicine.name.asc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    # ==================================================
    # Search Medicines
    # ==================================================

    @staticmethod
    def search(
        keyword,
        user_id,
        page=1,
        per_page=10
    ):

        keyword = str(
            keyword or ""
        ).strip()

        query = Medicine.query.filter(
            Medicine.user_id == user_id
        )

        if keyword:

            query = query.filter(
                db.or_(
                    Medicine.name.ilike(
                        f"%{keyword}%"
                    ),
                    Medicine.batch_number.ilike(
                        f"%{keyword}%"
                    )
                )
            )

        return query.order_by(
            Medicine.name.asc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    # ==================================================
    # Filter Category
    # ==================================================

    @staticmethod
    def filter_category(
        category,
        user_id,
        page=1,
        per_page=10
    ):

        query = Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.category == category
        )

        return query.order_by(
            Medicine.name.asc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    # ==================================================
    # Low Stock
    # ==================================================

    @staticmethod
    def low_stock(
        user_id,
        page=None,
        per_page=10
    ):

        query = Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.quantity <= Medicine.low_stock_alert
        ).order_by(
            Medicine.name.asc()
        )

        if page is not None:

            return query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

        return query.all()

    # ==================================================
    # Expiring Soon
    # ==================================================

    @staticmethod
    def expiring(
        days,
        user_id,
        page=None,
        per_page=10
    ):

        today = date.today()
        future = today + timedelta(
            days=days
        )

        query = Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future
        ).order_by(
            Medicine.expiry_date.asc()
        )

        if page is not None:

            return query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

        return query.all()

    # ==================================================
    # Move Expired Medicines
    # ==================================================

    @staticmethod
    def move_expired(
        user_id
    ):

        today = date.today()

        expired = Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date < today
        ).all()

        moved = 0

        try:

            for medicine in expired:

                value = float(
                    (medicine.quantity or 0)
                    * (medicine.price or 0)
                )

                expired_record = ExpiredMedicine(
                    medicine_id=medicine.id,
                    user_id=user_id,
                    name=medicine.name,
                    batch_number=medicine.batch_number,
                    category=medicine.category,
                    quantity=medicine.quantity,
                    price=medicine.price,
                    expiry_date=medicine.expiry_date,
                    original_value=value,
                    loss_amount=value
                )

                db.session.add(
                    expired_record
                )

                db.session.delete(
                    medicine
                )

                moved += 1

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return moved