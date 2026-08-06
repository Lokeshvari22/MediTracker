from datetime import date, timedelta

from database.database import db

from models.medicine import Medicine
from models.expired_medicine import ExpiredMedicine


class ExpiryService:

    # ==================================
    # Medicines Expiring Within X Days
    # ==================================

    @staticmethod
    def expiring_soon(
        user_id,
        days=30
    ):
        today = date.today()
        future = today + timedelta(days=days)

        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future
        ).order_by(
            Medicine.expiry_date.asc()
        ).all()

    # ==================================
    # Paginated Expiring Soon List
    # ==================================

    @staticmethod
    def expiring_soon_paginated(
        user_id,
        page=1,
        per_page=10,
        days=30,
        search=""
    ):
        today = date.today()
        future = today + timedelta(days=days)

        query = Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future
        )

        if search:
            query = query.filter(
                (Medicine.name.ilike(f"%{search}%")) |
                (Medicine.batch_number.ilike(f"%{search}%"))
            )

        return query.order_by(
            Medicine.expiry_date.asc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    # ==================================
    # Already Expired Medicines
    # ==================================

    @staticmethod
    def expired_medicines(
        user_id
    ):
        today = date.today()

        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date < today
        ).order_by(
            Medicine.expiry_date.asc()
        ).all()

    # ==================================
    # Move Expired Medicines to Archive
    # ==================================

    @staticmethod
    def archive_expired(
        user_id
    ):
        medicines = ExpiryService.expired_medicines(
            user_id
        )

        moved = 0

        try:
            for medicine in medicines:
                loss_val = float(medicine.quantity * medicine.price)

                expired = ExpiredMedicine(
                    medicine_id=medicine.id,
                    user_id=user_id,
                    name=medicine.name,
                    batch_number=medicine.batch_number,
                    category=medicine.category,
                    quantity=medicine.quantity,
                    price=medicine.price,
                    expiry_date=medicine.expiry_date,
                    original_value=loss_val,
                    loss_amount=loss_val
                )

                db.session.add(expired)
                db.session.delete(medicine)

                moved += 1

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return moved

    # ==================================
    # Archive Single Expired Medicine
    # ==================================

    @staticmethod
    def archive_medicine(
        user_id,
        medicine_id
    ):
        medicine = Medicine.query.filter_by(
            id=medicine_id,
            user_id=user_id
        ).first()

        if not medicine:
            raise ValueError("Medicine not found.")

        if not medicine.expiry_date or medicine.expiry_date >= date.today():
            raise ValueError("Only expired medicines can be archived.")

        loss_val = float(medicine.quantity * medicine.price)

        expired = ExpiredMedicine(
            medicine_id=medicine.id,
            user_id=user_id,
            name=medicine.name,
            batch_number=medicine.batch_number,
            category=medicine.category,
            quantity=medicine.quantity,
            price=medicine.price,
            expiry_date=medicine.expiry_date,
            original_value=loss_val,
            loss_amount=loss_val
        )

        db.session.add(expired)
        db.session.delete(medicine)
        db.session.commit()

        return expired

    # ==================================
    # Delete Archived Expired Record
    # ==================================

    @staticmethod
    def delete_archived_record(
        user_id,
        expired_id
    ):
        expired = ExpiredMedicine.query.filter_by(
            id=expired_id,
            user_id=user_id
        ).first()

        if not expired:
            raise ValueError("Archived record not found.")

        db.session.delete(expired)
        db.session.commit()

        return expired

    # ==================================
    # Total Expired Medicines
    # ==================================

    @staticmethod
    def total_expired(
        user_id
    ):
        return ExpiredMedicine.query.filter_by(
            user_id=user_id
        ).count()

    # ==================================
    # Total Expiring Soon
    # ==================================

    @staticmethod
    def total_expiring(
        user_id,
        days=30
    ):
        today = date.today()
        future = today + timedelta(days=days)

        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future
        ).count()

    # ==================================
    # Expired Stock Value
    # ==================================

    @staticmethod
    def expired_stock_value(
        user_id
    ):
        result = db.session.query(
            db.func.sum(ExpiredMedicine.original_value)
        ).filter(
            ExpiredMedicine.user_id == user_id
        ).scalar()

        return float(result) if result else 0.0

    # ==================================
    # Expiring Stock Value
    # ==================================

    @staticmethod
    def expiring_stock_value(
        user_id,
        days=30
    ):
        today = date.today()
        future = today + timedelta(days=days)

        result = db.session.query(
            db.func.sum(Medicine.quantity * Medicine.price)
        ).filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future
        ).scalar()

        return float(result) if result else 0.0

    # ==================================
    # Low Stock & Expiring Medicines
    # ==================================

    @staticmethod
    def critical_medicines(
        user_id
    ):
        today = date.today()
        future = today + timedelta(days=30)

        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.quantity <= Medicine.low_stock_alert,
            Medicine.expiry_date <= future
        ).order_by(
            Medicine.expiry_date.asc()
        ).all()

    # ==================================
    # Expiry Alert Summary
    # ==================================

    @staticmethod
    def expiry_summary(
        user_id
    ):
        return {
            "expired": ExpiryService.total_expired(
                user_id
            ),
            "expiring": ExpiryService.total_expiring(
                user_id
            ),
            "expired_value": ExpiryService.expired_stock_value(
                user_id
            ),
            "expiring_value": ExpiryService.expiring_stock_value(
                user_id
            )
        }