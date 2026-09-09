from datetime import datetime, date, timedelta

from database.database import db

from models.medicine import Medicine
from models.expired_medicine import ExpiredMedicine


class ExpiryService:

    # ==========================================================
    # Get Expired Medicines
    # ==========================================================

    @staticmethod
    def expired_medicines(user_id):

        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date.isnot(None),
            Medicine.expiry_date < date.today()
        ).order_by(
            Medicine.expiry_date.asc()
        ).all()

    # ==========================================================
    # Get Expiring Soon Medicines
    # ==========================================================

    @staticmethod
    def expiring_medicines(user_id, days=30):

        today = date.today()
        future = today + timedelta(days=days)

        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date.isnot(None),
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future
        ).order_by(
            Medicine.expiry_date.asc()
        ).all()

    # ==========================================================
    # Total Expiring Soon
    # ==========================================================

    @staticmethod
    def total_expiring(user_id, days=30):

        return len(
            ExpiryService.expiring_medicines(
                user_id,
                days
            )
        )

    # ==========================================================
    # Archive Expired Medicine
    # ==========================================================

    @staticmethod
    def archive_medicine(user_id, medicine_id):

        medicine = Medicine.query.filter_by(
            id=medicine_id,
            user_id=user_id
        ).first()

        if not medicine:
            raise ValueError(
                "Medicine not found."
            )

        # Only expired medicines can be archived
        if not medicine.expiry_date:
            raise ValueError(
                "Medicine does not have an expiry date."
            )

        if medicine.expiry_date >= date.today():
            raise ValueError(
                "Only expired medicines can be archived."
            )

        # Calculate expired stock value
        quantity = medicine.quantity or 0
        price = medicine.price or 0

        loss_amount = quantity * price

        # Create archive record
        archived = ExpiredMedicine(
            name=medicine.name,
            batch_number=medicine.batch_number,
            category=medicine.category,
            quantity=quantity,
            price=price,
            expiry_date=medicine.expiry_date,
            original_value=loss_amount,
            loss_amount=loss_amount,
            expired_date=datetime.now(),
            medicine_id=medicine.id,
            user_id=user_id
        )

        db.session.add(archived)

        # Remove from active Medicine table
        db.session.delete(medicine)

        # Save both operations together
        db.session.commit()

        return archived

    # ==========================================================
    # Delete Archived Record
    # ==========================================================

    @staticmethod
    def delete_archived_record(user_id, expired_id):

        archived = ExpiredMedicine.query.filter_by(
            id=expired_id,
            user_id=user_id
        ).first()

        if not archived:
            raise ValueError(
                "Archived record not found."
            )

        db.session.delete(archived)

        db.session.commit()

        return True