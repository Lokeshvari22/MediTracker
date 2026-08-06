from sqlalchemy import func

from database.database import db

from models.medicine import Medicine
from models.sale import Sale
from models.purchase import Purchase
from models.expired_medicine import ExpiredMedicine


class AnalyticsService:

    # ==================================
    # Dashboard Statistics
    # ==================================

    @staticmethod
    def get_dashboard_data(user_id):

        total_medicines = Medicine.query.filter_by(
            user_id=user_id
        ).count()

        total_stock = db.session.query(
            func.coalesce(func.sum(Medicine.quantity), 0)
        ).filter(
            Medicine.user_id == user_id
        ).scalar()

        inventory_value = db.session.query(
            func.coalesce(func.sum(Medicine.quantity * Medicine.price), 0.0)
        ).filter(
            Medicine.user_id == user_id
        ).scalar()

        total_sales = db.session.query(
            func.coalesce(func.sum(Sale.total_amount), 0.0)
        ).filter(
            Sale.user_id == user_id
        ).scalar()

        total_purchases = db.session.query(
            func.coalesce(func.sum(Purchase.quantity * Purchase.purchase_price), 0.0)
        ).filter(
            Purchase.user_id == user_id
        ).scalar()

        expired_count = ExpiredMedicine.query.filter_by(
            user_id=user_id
        ).count()

        expired_loss = db.session.query(
            func.coalesce(func.sum(ExpiredMedicine.original_value), 0.0)
        ).filter(
            ExpiredMedicine.user_id == user_id
        ).scalar()

        low_stock = Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.quantity <= Medicine.low_stock_alert
        ).count()

        return {
            "total_medicines": total_medicines,
            "total_stock": float(total_stock),
            "inventory_value": float(inventory_value),
            "total_sales": float(total_sales),
            "total_purchases": float(total_purchases),
            "net_profit": float(total_sales - total_purchases),
            "expired_loss": float(expired_loss),
            "expired_medicines": expired_count,
            "low_stock": low_stock
        }

    # ==================================
    # Dashboard Cards
    # ==================================

    @staticmethod
    def get_dashboard_cards(user_id):
        return AnalyticsService.get_dashboard_data(user_id)

    # ==================================
    # Category Chart
    # ==================================

    @staticmethod
    def medicines_by_category(user_id):
        category_col = func.coalesce(Medicine.category, "Uncategorized")

        result = db.session.query(
            category_col,
            func.count(Medicine.id)
        ).filter(
            Medicine.user_id == user_id
        ).group_by(
            category_col
        ).all()

        return {
            "labels": [row[0] for row in result],
            "values": [row[1] for row in result]
        }

    # ==================================
    # Monthly Sales Chart
    # ==================================

    @staticmethod
    def monthly_sales(user_id):
        month_col = func.strftime("%Y-%m", Sale.sale_date)

        result = db.session.query(
            month_col,
            func.sum(Sale.total_amount)
        ).filter(
            Sale.user_id == user_id
        ).group_by(
            month_col
        ).order_by(
            month_col.asc()
        ).all()

        return {
            "labels": [row[0] for row in result if row[0]],
            "values": [float(row[1]) for row in result if row[0]]
        }

    # ==================================
    # Monthly Purchase Chart
    # ==================================

    @staticmethod
    def monthly_purchases(user_id):
        month_col = func.strftime("%Y-%m", Purchase.purchase_date)

        result = db.session.query(
            month_col,
            func.sum(Purchase.quantity * Purchase.purchase_price)
        ).filter(
            Purchase.user_id == user_id
        ).group_by(
            month_col
        ).order_by(
            month_col.asc()
        ).all()

        return {
            "labels": [row[0] for row in result if row[0]],
            "values": [float(row[1]) for row in result if row[0]]
        }

    # ==================================
    # Expiry Chart
    # ==================================

    @staticmethod
    def expiry_statistics(user_id):
        expired = ExpiredMedicine.query.filter_by(
            user_id=user_id
        ).count()

        active = Medicine.query.filter_by(
            user_id=user_id
        ).count()

        return {
            "labels": ["Available", "Expired"],
            "values": [active, expired]
        }

    # ==================================
    # Complete Chart Data
    # ==================================

    @staticmethod
    def get_chart_data(user_id):
        return {
            "category": AnalyticsService.medicines_by_category(user_id),
            "sales": AnalyticsService.monthly_sales(user_id),
            "purchases": AnalyticsService.monthly_purchases(user_id),
            "expiry": AnalyticsService.expiry_statistics(user_id)
        }

    # ==================================
    # Top Selling Medicines
    # ==================================

    @staticmethod
    def top_selling(user_id, limit=5):
        result = db.session.query(
            Medicine.name,
            func.sum(Sale.quantity).label("total")
        ).join(
            Sale,
            Sale.medicine_id == Medicine.id
        ).filter(
            Sale.user_id == user_id
        ).group_by(
            Medicine.id, Medicine.name
        ).order_by(
            func.sum(Sale.quantity).desc()
        ).limit(limit).all()

        return [{"name": row[0], "total": int(row[1])} for row in result]

    # ==================================
    # Dashboard Summary
    # ==================================

    @staticmethod
    def dashboard_summary(user_id):
        return AnalyticsService.get_dashboard_data(user_id)