from sqlalchemy import func

from database.database import db

from models.medicine import Medicine
from models.sale import Sale
from models.purchase import Purchase


class SalesAnalysis:

    # ==================================
    # Total Sales Revenue
    # ==================================

    @staticmethod
    def total_sales(user_id):

        total = db.session.query(
            func.coalesce(
                func.sum(Sale.total_amount),
                0.0
            )
        ).filter(
            Sale.user_id == user_id
        ).scalar()

        return float(total or 0.0)

    # ==================================
    # Total Purchase Cost
    # ==================================

    @staticmethod
    def total_purchases(user_id):

        total = db.session.query(
            func.coalesce(
                func.sum(
                    Purchase.quantity *
                    Purchase.purchase_price
                ),
                0.0
            )
        ).filter(
            Purchase.user_id == user_id
        ).scalar()

        return float(total or 0.0)

    # ==================================
    # Cost Of Goods Sold
    # ==================================

    @staticmethod
    def cost_of_goods_sold(user_id):

        """
        Calculate the cost of medicines that were actually sold.

        IMPORTANT:
        select_from(Sale) explicitly tells SQLAlchemy
        that Sale is the starting table.

        join(
            Medicine,
            Sale.medicine_id == Medicine.id
        )

        explicitly defines the relationship.

        This fixes:
        InvalidRequestError:
        Don't know how to join to Medicine
        """

        cost = db.session.query(
            func.coalesce(
                func.sum(
                    Sale.quantity * Medicine.price
                ),
                0.0
            )
        ).select_from(
            Sale
        ).join(
            Medicine,
            Sale.medicine_id == Medicine.id
        ).filter(
            Sale.user_id == user_id
        ).scalar()

        return float(cost or 0.0)

    # ==================================
    # Total Profit
    # ==================================

    @staticmethod
    def total_profit(user_id):

        revenue = SalesAnalysis.total_sales(user_id)

        cost_of_sold = SalesAnalysis.cost_of_goods_sold(
            user_id
        )

        return float(
            revenue - cost_of_sold
        )

    # ==================================
    # Monthly Sales
    # ==================================

    @staticmethod
    def monthly_sales(user_id):

        month_col = func.strftime(
            "%Y-%m",
            Sale.sale_date
        )

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

        return [
            {
                "month": row[0],
                "sales": float(row[1] or 0.0)
            }
            for row in result
            if row[0]
        ]

    # ==================================
    # Monthly Purchases
    # ==================================

    @staticmethod
    def monthly_purchases(user_id):

        month_col = func.strftime(
            "%Y-%m",
            Purchase.purchase_date
        )

        result = db.session.query(
            month_col,
            func.sum(
                Purchase.quantity *
                Purchase.purchase_price
            )
        ).filter(
            Purchase.user_id == user_id
        ).group_by(
            month_col
        ).order_by(
            month_col.asc()
        ).all()

        return [
            {
                "month": row[0],
                "purchase": float(row[1] or 0.0)
            }
            for row in result
            if row[0]
        ]

    # ==================================
    # Top Selling Medicines
    # ==================================

    @staticmethod
    def top_selling(user_id, limit=10):

        result = db.session.query(
            Medicine.name,
            func.sum(Sale.quantity).label("sold")
        ).select_from(
            Sale
        ).join(
            Medicine,
            Sale.medicine_id == Medicine.id
        ).filter(
            Sale.user_id == user_id
        ).group_by(
            Medicine.id,
            Medicine.name
        ).order_by(
            func.sum(Sale.quantity).desc()
        ).limit(
            limit
        ).all()

        return [
            {
                "medicine": row[0],
                "quantity": int(row[1] or 0)
            }
            for row in result
        ]

    # ==================================
    # Recent Sales
    # ==================================

    @staticmethod
    def recent_sales(user_id, limit=10):

        return Sale.query.filter_by(
            user_id=user_id
        ).order_by(
            Sale.sale_date.desc()
        ).limit(
            limit
        ).all()

    # ==================================
    # Highest Sale
    # ==================================

    @staticmethod
    def highest_sale(user_id):

        return Sale.query.filter_by(
            user_id=user_id
        ).order_by(
            Sale.total_amount.desc()
        ).first()

    # ==================================
    # Sales Statistics
    # ==================================

    @staticmethod
    def statistics(user_id):

        return {
            "sales":
                SalesAnalysis.total_sales(user_id),

            "purchases":
                SalesAnalysis.total_purchases(user_id),

            "profit":
                SalesAnalysis.total_profit(user_id),

            "transactions":
                Sale.query.filter_by(
                    user_id=user_id
                ).count()
        }

    # ==================================
    # Complete Dashboard Data
    # ==================================

    @staticmethod
    def dashboard(user_id):

        return {
            "statistics":
                SalesAnalysis.statistics(user_id),

            "monthly_sales":
                SalesAnalysis.monthly_sales(user_id),

            "monthly_purchases":
                SalesAnalysis.monthly_purchases(user_id),

            "top_selling":
                SalesAnalysis.top_selling(user_id),

            "recent_sales":
                SalesAnalysis.recent_sales(
                    user_id
                )
        }