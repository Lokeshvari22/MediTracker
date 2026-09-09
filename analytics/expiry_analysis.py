from datetime import date, timedelta

from sqlalchemy import func

from database.database import db
from models.medicine import Medicine
from models.expired_medicine import ExpiredMedicine


class ExpiryAnalysis:

    # ==================================
    # Expiring Within X Days
    # ==================================

    @staticmethod
    def expiring_soon(user_id, days=30):

        today = date.today()
        future = today + timedelta(days=days)

        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date.isnot(None),
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future,
            Medicine.quantity > 0
        ).order_by(
            Medicine.expiry_date.asc()
        ).all()

    # ==================================
    # Already Expired
    # ==================================

    @staticmethod
    def expired(user_id):

        return ExpiredMedicine.query.filter_by(
            user_id=user_id
        ).order_by(
            ExpiredMedicine.expiry_date.desc()
        ).all()

    # ==================================
    # Recently Expired
    # ==================================

    @staticmethod
    def recently_expired(user_id, limit=5):

        results = []

        # First get records already moved to expired_medicines
        expired_records = ExpiredMedicine.query.filter_by(
            user_id=user_id
        ).order_by(
            ExpiredMedicine.expiry_date.desc()
        ).limit(limit).all()

        results.extend(expired_records)

        # If not enough records exist there,
        # also check medicines table.
        if len(results) < limit:

            more = Medicine.query.filter(
                Medicine.user_id == user_id,
                Medicine.expiry_date.isnot(None),
                Medicine.expiry_date < date.today()
            ).order_by(
                Medicine.expiry_date.desc()
            ).limit(
                limit - len(results)
            ).all()

            results.extend(more)

        return results

    # ==================================
    # Total Expiring Soon
    # ==================================

    @staticmethod
    def total_expiring(user_id, days=30):

        today = date.today()
        future = today + timedelta(days=days)

        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date.isnot(None),
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future,
            Medicine.quantity > 0
        ).count()

    # ==================================
    # Total Expired
    # ==================================

    @staticmethod
    def total_expired(user_id):

        return ExpiredMedicine.query.filter_by(
            user_id=user_id
        ).count()

    # ==================================
    # Expired Stock Value
    # ==================================

    @staticmethod
    def expired_value(user_id):

        result = db.session.query(
            func.coalesce(
                func.sum(
                    ExpiredMedicine.original_value
                ),
                0.0
            )
        ).filter(
            ExpiredMedicine.user_id == user_id
        ).scalar()

        return float(result or 0.0)

    # ==================================
    # Expiring Stock Value
    # ==================================

    @staticmethod
    def expiring_value(user_id, days=30):

        today = date.today()
        future = today + timedelta(days=days)

        result = db.session.query(
            func.coalesce(
                func.sum(
                    Medicine.quantity * Medicine.price
                ),
                0.0
            )
        ).filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date.isnot(None),
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future,
            Medicine.quantity > 0
        ).scalar()

        return float(result or 0.0)

    # ==================================
    # Expiry By Category
    # ==================================

    @staticmethod
    def category_summary(user_id, days=30):

        today = date.today()
        future = today + timedelta(days=days)

        category_col = func.coalesce(
            Medicine.category,
            "Uncategorized"
        )

        result = db.session.query(
            category_col,
            func.count(Medicine.id)
        ).filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date.isnot(None),
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future,
            Medicine.quantity > 0
        ).group_by(
            category_col
        ).all()

        return {
            row[0]: int(row[1] or 0)
            for row in result
        }

    # ==================================
    # Critical Medicines
    # ==================================

    @staticmethod
    def critical_medicines(user_id, days=30):

        today = date.today()
        future = today + timedelta(days=days)

        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date.isnot(None),
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= future,
            Medicine.quantity > 0,
            Medicine.quantity <= Medicine.low_stock_alert
        ).order_by(
            Medicine.expiry_date.asc()
        ).all()

    # ==================================
    # Expiry Summary
    # ==================================

    @staticmethod
    def summary(user_id):

        return {
            "expired":
                ExpiryAnalysis.total_expired(user_id),

            "expiring":
                ExpiryAnalysis.total_expiring(user_id),

            "expired_value":
                ExpiryAnalysis.expired_value(user_id),

            "expiring_value":
                ExpiryAnalysis.expiring_value(user_id)
        }