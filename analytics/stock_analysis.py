from sqlalchemy import func
from database.database import db
from models.medicine import Medicine


class StockAnalysis:

    # ==================================
    # Total Inventory Value
    # ==================================
    @staticmethod
    def total_inventory_value(user_id):
        value = db.session.query(
            func.sum(
                Medicine.quantity * Medicine.price
            )
        ).filter(
            Medicine.user_id == user_id
        ).scalar()
        return value or 0.0

    # ==================================
    # Total Stock Quantity
    # ==================================
    @staticmethod
    def total_stock(user_id):
        quantity = db.session.query(
            func.sum(Medicine.quantity)
        ).filter(
            Medicine.user_id == user_id
        ).scalar()
        return quantity or 0

    # ==================================
    # Low Stock Medicines
    # ==================================
    @staticmethod
    def low_stock(user_id):
        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.quantity <= Medicine.low_stock_alert
        ).order_by(
            Medicine.quantity.asc()
        ).all()

    # Alias to resolve AttributeError in DashboardMetrics
    @staticmethod
    def low_stock_items(user_id):
        return StockAnalysis.low_stock(user_id)

    # ==================================
    # Out Of Stock Medicines
    # ==================================
    @staticmethod
    def out_of_stock(user_id):
        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.quantity == 0
        ).order_by(
            Medicine.name.asc()
        ).all()

    # ==================================
    # Medicines By Category
    # ==================================
    @staticmethod
    def category_distribution(user_id):
        result = db.session.query(
            Medicine.category,
            func.count(Medicine.id)
        ).filter(
            Medicine.user_id == user_id
        ).group_by(
            Medicine.category
        ).all()

        return [
            {
                "category": row[0] or "Uncategorized",
                "count": row[1]
            }
            for row in result
        ]

    # ==================================
    # Top Valuable Medicines
    # ==================================
    @staticmethod
    def top_inventory_value(user_id, limit=10):
        medicines = Medicine.query.filter_by(
            user_id=user_id
        ).all()

        medicines.sort(
            key=lambda medicine: (medicine.quantity or 0) * (medicine.price or 0.0),
            reverse=True
        )
        return medicines[:limit]

    # ==================================
    # Stock Summary
    # ==================================
    @staticmethod
    def summary(user_id):
        return {
            "total_stock": StockAnalysis.total_stock(user_id),
            "inventory_value": StockAnalysis.total_inventory_value(user_id),
            "low_stock": len(StockAnalysis.low_stock(user_id)),
            "out_of_stock": len(StockAnalysis.out_of_stock(user_id))
        }