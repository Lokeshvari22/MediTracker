from datetime import date

from database.database import db

from models.medicine import Medicine
from models.expired_medicine import ExpiredMedicine


class InventoryService:

    # ----------------------------------
    # Add Medicine
    # ----------------------------------

    @staticmethod
    def add_medicine(data, user_id):

        medicine = Medicine(

            name=data["name"],

            batch_number=data["batch_number"],

            category=data["category"],

            quantity=data["quantity"],

            price=data["price"],

            expiry_date=data["expiry_date"],

            low_stock_alert=data.get(
                "low_stock_alert",
                10
            ),

            user_id=user_id

        )

        db.session.add(medicine)

        db.session.commit()

        return medicine

    # ----------------------------------
    # Get Medicine
    # ----------------------------------

    @staticmethod
    def get_medicine(medicine_id, user_id):

        return Medicine.query.filter_by(

            id=medicine_id,

            user_id=user_id

        ).first()

    # ----------------------------------
    # Update Medicine
    # ----------------------------------

    @staticmethod
    def update_medicine(
        medicine,
        data
    ):

        medicine.name = data["name"]

        medicine.batch_number = data["batch_number"]

        medicine.category = data["category"]

        medicine.quantity = data["quantity"]

        medicine.price = data["price"]

        medicine.expiry_date = data["expiry_date"]

        medicine.low_stock_alert = data.get(
            "low_stock_alert",
            medicine.low_stock_alert
        )

        db.session.commit()

        return medicine

    # ----------------------------------
    # Delete Medicine
    # ----------------------------------

    @staticmethod
    def delete_medicine(medicine):

        db.session.delete(medicine)

        db.session.commit()

    # ----------------------------------
    # List Medicines
    # ----------------------------------

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

    # ----------------------------------
    # List Available Medicines
    # ----------------------------------

    @staticmethod
    def list_available(user_id):

        return Medicine.query.filter(

            Medicine.user_id == user_id,
            Medicine.quantity > 0

        ).order_by(

            Medicine.name.asc()

        ).all()

    # ----------------------------------
    # List All Medicines
    # ----------------------------------

    @staticmethod
    def list_all(user_id):

        return Medicine.query.filter_by(

            user_id=user_id

        ).order_by(

            Medicine.name.asc()

        ).all()

    # ----------------------------------
    # Search Medicines
    # ----------------------------------

    @staticmethod
    def search(
        keyword,
        user_id
    ):

        return Medicine.query.filter(

            Medicine.user_id == user_id,

            Medicine.name.ilike(
                f"%{keyword}%"
            )

        ).all()

    # ----------------------------------
    # Filter Category
    # ----------------------------------

    @staticmethod
    def filter_category(
        category,
        user_id
    ):

        return Medicine.query.filter_by(

            category=category,

            user_id=user_id

        ).all()

    # ----------------------------------
    # Low Stock
    # ----------------------------------

    @staticmethod
    def low_stock(user_id):

        return Medicine.query.filter(

            Medicine.user_id == user_id,

            Medicine.quantity <= Medicine.low_stock_alert

        ).all()

    # ----------------------------------
    # Expiring Soon
    # ----------------------------------

    @staticmethod
    def expiring(days, user_id):

        today = date.today()

        from datetime import timedelta

        future = today + timedelta(days=days)

        return Medicine.query.filter(

            Medicine.user_id == user_id,

            Medicine.expiry_date >= today,

            Medicine.expiry_date <= future

        ).all()

    # ----------------------------------
    # Move Expired Medicines
    # ----------------------------------

    @staticmethod
    def move_expired(user_id):

        today = date.today()

        expired = Medicine.query.filter(

            Medicine.user_id == user_id,

            Medicine.expiry_date < today

        ).all()

        for medicine in expired:

            expired_record = ExpiredMedicine(

                medicine_id=medicine.id,

                user_id=user_id,

                name=medicine.name,

                batch_number=medicine.batch_number,

                category=medicine.category,

                quantity=medicine.quantity,

                price=medicine.price,

                expiry_date=medicine.expiry_date,

                original_value=medicine.price * medicine.quantity

            )

            db.session.add(expired_record)

            db.session.delete(medicine)

        db.session.commit()

        return len(expired)