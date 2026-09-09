from sqlalchemy import func
from datetime import datetime, time

from database.database import db

from models.medicine import Medicine
from models.sale import Sale
from models.purchase import Purchase
from models.transaction import Transaction
from models.expired_medicine import ExpiredMedicine


class ReportService:

    # ==================================
    # Dashboard Summary
    # ==================================

    @staticmethod
    def dashboard_summary(user_id):

        return {

            "total_medicines": Medicine.query.filter_by(
                user_id=user_id
            ).count(),

            "total_sales": Sale.query.filter_by(
                user_id=user_id
            ).count(),

            "total_purchases": Purchase.query.filter_by(
                user_id=user_id
            ).count(),

            "expired_medicines": ExpiredMedicine.query.filter_by(
                user_id=user_id
            ).count()

        }

    # ==================================
    # Report Summary
    # ==================================

    @staticmethod
    def get_report_summary(user_id):

        inventory_value = db.session.query(
            func.sum(
                Medicine.quantity *
                Medicine.price
            )
        ).filter(
            Medicine.user_id == user_id
        ).scalar() or 0

        sales_value = db.session.query(
            func.sum(
                Sale.total_amount
            )
        ).filter(
            Sale.user_id == user_id
        ).scalar() or 0

        # Fixed: Replaced Purchase.total_amount with (Purchase.quantity * Purchase.purchase_price)
        purchase_value = db.session.query(
            func.sum(
                Purchase.quantity *
                Purchase.purchase_price
            )
        ).filter(
            Purchase.user_id == user_id
        ).scalar() or 0

        return {

            "inventory_value": inventory_value,

            "sales_value": sales_value,

            "purchase_value": purchase_value,

            "profit": sales_value - purchase_value

        }

    # ==================================
    # Stock Report
    # ==================================

    @staticmethod
    def stock_report(user_id):

        return Medicine.query.filter_by(

            user_id=user_id

        ).order_by(

            Medicine.name.asc()

        ).all()

    # ==================================
    # Sales Report
    # ==================================

    @staticmethod
    def sales_report(user_id, from_date=None, to_date=None):

        query = Sale.query.filter_by(
            user_id=user_id
        )

        if from_date:
            query = query.filter(Sale.sale_date >= from_date)

        if to_date:
            query = query.filter(Sale.sale_date <= to_date)

        return query.order_by(
            Sale.sale_date.desc()
        ).all()

    # ==================================
    # Purchase Report
    # ==================================

    @staticmethod
    def purchase_report(user_id, from_date=None, to_date=None):

        query = Purchase.query.filter_by(
            user_id=user_id
        )

        if from_date:
            query = query.filter(Purchase.purchase_date >= from_date)

        if to_date:
            query = query.filter(Purchase.purchase_date <= to_date)

        return query.order_by(
            Purchase.purchase_date.desc()
        ).all()

    # ==================================
    # Expiry Report
    # ==================================

    @staticmethod
    def expiry_report(user_id, from_date=None, to_date=None):

        query = Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.expiry_date.isnot(None),
            Medicine.expiry_date < datetime.today().date()
        )

        if from_date:
            query = query.filter(
                Medicine.expiry_date >= from_date.date()
                if isinstance(from_date, datetime)
                else Medicine.expiry_date >= from_date
            )

        if to_date:
            query = query.filter(
                Medicine.expiry_date <= to_date.date()
                if isinstance(to_date, datetime)
                else Medicine.expiry_date <= to_date
            )

        return query.order_by(
            Medicine.expiry_date.desc()
        ).all()

    # ==================================
    # Transaction History
    # ==================================

    @staticmethod
    def get_transactions(

        user_id,

        page=1,

        per_page=10,

        search="",

        transaction_type="",

        from_date=None,

        to_date=None

    ):


        query = Transaction.query.filter_by(
            user_id=user_id
        )

        if transaction_type:
            query = query.filter(
                func.upper(Transaction.transaction_type) == transaction_type.upper()
            )

        # search by medicine name or batch
        if search:
            query = query.join(Medicine).filter(
                (Medicine.name.ilike(f"%{search}%")) |
                (Medicine.batch_number.ilike(f"%{search}%")) |
                (Transaction.remarks.ilike(f"%{search}%"))
            )

        # parse date strings if provided
        if from_date:
            try:
                from_dt = datetime.strptime(from_date, "%Y-%m-%d")
                query = query.filter(Transaction.transaction_date >= datetime.combine(from_dt.date(), time.min))
            except Exception:
                pass

        if to_date:
            try:
                to_dt = datetime.strptime(to_date, "%Y-%m-%d")
                query = query.filter(Transaction.transaction_date <= datetime.combine(to_dt.date(), time.max))
            except Exception:
                pass

        return query.order_by(

            Transaction.transaction_date.desc()

        ).paginate(

            page=page,

            per_page=per_page,

            error_out=False

        )

    # ==================================
    # Transaction Summary
    # ==================================

    @staticmethod
    def transaction_summary(user_id):

        purchases = Purchase.query.filter_by(user_id=user_id).count()

        sales = Sale.query.filter_by(user_id=user_id).count()

        transactions = Transaction.query.filter_by(user_id=user_id).count()

        # Treat PURCHASE and IN as stock-in, SALE and OUT as stock-out
        stock_in = Transaction.query.filter(
            Transaction.user_id == user_id,
            func.upper(Transaction.transaction_type).in_(["IN", "PURCHASE"])  # noqa: E501
        ).count()

        stock_out = Transaction.query.filter(
            Transaction.user_id == user_id,
            func.upper(Transaction.transaction_type).in_(["OUT", "SALE"])  # noqa: E501
        ).count()

        return {
            "transactions": transactions,
            "sales": sales,
            "purchases": purchases,
            "stock_in_count": stock_in,
            "stock_out_count": stock_out,
            "sales_count": sales,
            "purchase_count": purchases
        }

    # ==================================
    # Monthly Sales
    # ==================================

    @staticmethod
    def monthly_sales(user_id):

        return db.session.query(

            func.strftime(

                "%Y-%m",

                Sale.sale_date

            ),

            func.sum(

                Sale.total_amount

            )

        ).filter(

            Sale.user_id == user_id

        ).group_by(

            func.strftime(

                "%Y-%m",

                Sale.sale_date

            )

        ).all()

    # ==================================
    # Monthly Purchases
    # ==================================

    @staticmethod
    def monthly_purchases(user_id):

        # Fixed: Replaced Purchase.total_amount with (Purchase.quantity * Purchase.purchase_price)
        return db.session.query(

            func.strftime(

                "%Y-%m",

                Purchase.purchase_date

            ),

            func.sum(

                Purchase.quantity *
                Purchase.purchase_price

            )

        ).filter(

            Purchase.user_id == user_id

        ).group_by(

            func.strftime(

                "%Y-%m",

                Purchase.purchase_date

            )

        ).all()