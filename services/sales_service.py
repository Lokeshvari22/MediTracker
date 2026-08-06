from datetime import date, datetime, time

from database.database import db

from models.sale import Sale
from models.purchase import Purchase
from models.medicine import Medicine
from models.transaction import Transaction


class SalesService:

    # ==================================================
    # PURCHASES
    # ==================================================

    @staticmethod
    def create_purchase(data, user_id):
        medicine = Medicine.query.filter_by(
            id=data["medicine_id"],
            user_id=user_id
        ).first()

        if not medicine:
            raise ValueError("Medicine not found.")

        medicine.quantity += data["quantity"]

        discount = float(data.get("discount", 0) or 0)
        gst = float(data.get("gst", 0) or 0)
        total_amount = data.get("total_amount")

        if total_amount is None or total_amount == "":
            subtotal = data["quantity"] * data["purchase_price"]
            subtotal_after_discount = max(0.0, subtotal - discount)
            total_amount = subtotal_after_discount + (subtotal_after_discount * (gst / 100))
        else:
            total_amount = float(total_amount)

        purchase_date = data.get(
            "purchase_date",
            None
        )

        if isinstance(purchase_date, str):
            purchase_date = datetime.strptime(
                purchase_date,
                "%Y-%m-%d"
            ).date()

        if not purchase_date:
            purchase_date = datetime.now().date()

        # If total amount was not provided, compute it from unit price, discount, and gst
        if not total_amount:
            subtotal = data["quantity"] * data["purchase_price"]
            subtotal_after_discount = max(0.0, subtotal - discount)
            total_amount = subtotal_after_discount + (subtotal_after_discount * (gst / 100))

        purchase = Purchase(
            medicine_id=medicine.id,
            supplier_id=data["supplier_id"],
            quantity=data["quantity"],
            purchase_price=data["purchase_price"],
            discount=discount,
            gst=gst,
            total_amount=total_amount,
            payment_method=data.get("payment_method", "Cash"),
            status=data.get("status", "Paid"),
            notes=data.get("notes", ""),
            purchase_date=purchase_date,
            user_id=user_id
        )

        transaction = Transaction(
            medicine_id=medicine.id,
            transaction_type="PURCHASE",
            quantity=data["quantity"],
            remarks=f"Purchased from Supplier #{data['supplier_id']}",
            transaction_date=datetime.now(),
            user_id=user_id
        )

        try:
            db.session.add(purchase)
            db.session.add(transaction)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return purchase

    # ==================================================
    # SALES
    # ==================================================

    @staticmethod
    def create_sale(data, user_id):
        medicine = Medicine.query.filter_by(
            id=data["medicine_id"],
            user_id=user_id
        ).first()

        if not medicine:
            raise ValueError("Medicine not found.")

        if medicine.quantity < data["quantity"]:
            raise ValueError("Insufficient stock.")

        medicine.quantity -= data["quantity"]

        selling_price = float(data.get("sale_price") or data.get("selling_price") or medicine.price)

        discount = float(data.get("discount", 0) or 0)
        gst = float(data.get("gst", 0) or 0)

        total_amount = data.get("total_amount")

        if total_amount is None or total_amount == "":
            subtotal = selling_price * data["quantity"]
            subtotal_after_discount = max(0.0, subtotal - discount)
            total_amount = subtotal_after_discount + (subtotal_after_discount * (gst / 100))
        else:
            total_amount = float(total_amount)

        sale_date = data.get("sale_date", None)

        if isinstance(sale_date, str):
            try:
                sale_date = datetime.strptime(sale_date, "%Y-%m-%d")
            except Exception:
                sale_date = datetime.now()

        if not sale_date:
            sale_date = datetime.now()

        sale = Sale(
            medicine_id=medicine.id,
            quantity=data["quantity"],
            sale_price=selling_price,
            total_amount=total_amount,
            discount=discount,
            gst=gst,
            customer_name=data.get("customer_name", "Walk-in Customer"),
            customer_phone=data.get("customer_phone", ""),
            payment_method=data.get("payment_method", "Cash"),
            notes=data.get("notes", ""),
            sale_date=sale_date,
            user_id=user_id
        )

        transaction = Transaction(
            medicine_id=medicine.id,
            transaction_type="SALE",
            quantity=data["quantity"],
            remarks=f"Sold to {sale.customer_name}",
            transaction_date=datetime.now(),
            user_id=user_id
        )

        db.session.add(sale)
        db.session.add(transaction)
        db.session.commit()

        return sale

    # ==================================================
    # GET PURCHASE
    # ==================================================

    @staticmethod
    def get_purchase(purchase_id, user_id):
        return Purchase.query.filter_by(
            id=purchase_id,
            user_id=user_id
        ).first()

    # ==================================================
    # GET SALE
    # ==================================================

    @staticmethod
    def get_sale(sale_id, user_id):
        return Sale.query.filter_by(
            id=sale_id,
            user_id=user_id
        ).first()

    # ==================================================
    # LIST PURCHASES
    # ==================================================

    @staticmethod
    def list_purchases(user_id, page=1, per_page=10, search=None, supplier=None, **kwargs):
        query = Purchase.query.filter_by(user_id=user_id)

        from_date = kwargs.get("from_date", "")
        to_date = kwargs.get("to_date", "")

        if supplier:
            if isinstance(supplier, int) or (isinstance(supplier, str) and str(supplier).isdigit()):
                query = query.filter_by(supplier_id=int(supplier))

        if search:
            query = query.join(Medicine).filter(
                (Medicine.name.ilike(f"%{search}%")) |
                (Purchase.invoice_number.ilike(f"%{search}%"))
            )

        if from_date:
            try:
                from_dt = datetime.strptime(from_date, "%Y-%m-%d")
                query = query.filter(Purchase.purchase_date >= datetime.combine(from_dt.date(), time.min))
            except ValueError:
                pass

        if to_date:
            try:
                to_dt = datetime.strptime(to_date, "%Y-%m-%d")
                query = query.filter(Purchase.purchase_date <= datetime.combine(to_dt.date(), time.max))
            except ValueError:
                pass

        return query.order_by(
            Purchase.purchase_date.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    # ==================================================
    # LIST SALES
    # ==================================================

    @staticmethod
    def list_sales(user_id, page=1, per_page=10, search="", customer=None, **kwargs):
        query = Sale.query.filter_by(user_id=user_id)

        if search:
            query = query.join(Medicine).filter(
                (Medicine.name.ilike(f"%{search}%")) |
                (Sale.customer_name.ilike(f"%{search}%")) |
                (Sale.invoice_number.ilike(f"%{search}%")) |
                (db.func.concat('INV-SALE-', Sale.id).ilike(f"%{search}%"))
            )

        # customer filter (name or phone)
        if customer:
            query = query.filter(
                (Sale.customer_name.ilike(f"%{customer}%")) |
                (Sale.customer_phone.ilike(f"%{customer}%"))
            )

        from_date = kwargs.get("from_date", "")
        to_date = kwargs.get("to_date", "")

        if from_date:
            try:
                from_dt = datetime.strptime(from_date, "%Y-%m-%d")
                query = query.filter(Sale.sale_date >= datetime.combine(from_dt.date(), time.min))
            except ValueError:
                pass

        if to_date:
            try:
                to_dt = datetime.strptime(to_date, "%Y-%m-%d")
                query = query.filter(Sale.sale_date <= datetime.combine(to_dt.date(), time.max))
            except ValueError:
                pass

        return query.order_by(
            Sale.sale_date.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    # ==================================================
    # LIST ALL SALES
    # ==================================================

    @staticmethod
    def list_all(user_id):
        return Sale.query.filter_by(
            user_id=user_id
        ).order_by(
            Sale.sale_date.desc()
        ).all()

    # ==================================================
    # TODAY SALES
    # ==================================================

    @staticmethod
    def today_sales(user_id):
        return Sale.query.filter(
            Sale.user_id == user_id,
            db.func.date(Sale.sale_date) == date.today()
        ).count()

    # ==================================================
    # TOTAL PROFIT
    # ==================================================

    @staticmethod
    def total_profit(user_id):
        result = db.session.query(
            db.func.sum(Sale.total_amount - (Sale.quantity * Medicine.price))
        ).join(Medicine, Sale.medicine_id == Medicine.id).filter(
            Sale.user_id == user_id
        ).scalar()

        return float(result) if result else 0.0

    # ==================================================
    # DELETE PURCHASE
    # ==================================================

    @staticmethod
    def delete_purchase(purchase):
        medicine = Medicine.query.get(purchase.medicine_id)

        if medicine:
            medicine.quantity -= purchase.quantity
            if medicine.quantity < 0:
                medicine.quantity = 0

        db.session.delete(purchase)
        db.session.commit()

    # ==================================================
    # DELETE SALE
    # ==================================================

    @staticmethod
    def delete_sale(sale):
        medicine = Medicine.query.get(sale.medicine_id)

        if medicine:
            medicine.quantity += sale.quantity

        db.session.delete(sale)
        db.session.commit()

    # ==================================================
    # TOTAL SALES
    # ==================================================

    @staticmethod
    def total_sales(user_id):
        return Sale.query.filter_by(user_id=user_id).count()

    # ==================================================
    # TOTAL PURCHASES
    # ==================================================

    @staticmethod
    def total_purchases(user_id):
        return Purchase.query.filter_by(user_id=user_id).count()

    # ==================================================
    # SALES REVENUE
    # ==================================================

    @staticmethod
    def total_revenue(user_id):
        result = db.session.query(
            db.func.sum(Sale.total_amount)
        ).filter(Sale.user_id == user_id).scalar()

        return float(result) if result else 0.0

    # ==================================================
    # PURCHASE COST
    # ==================================================

    @staticmethod
    def total_purchase_cost(user_id):
        purchases = Purchase.query.filter_by(user_id=user_id).all()
        return float(sum(p.quantity * p.purchase_price for p in purchases))

    # ==================================================
    # TOTAL PURCHASE QUANTITY
    # ==================================================

    @staticmethod
    def total_purchase_quantity(user_id):
        result = db.session.query(
            db.func.sum(Purchase.quantity)
        ).filter(Purchase.user_id == user_id).scalar()

        return int(result) if result else 0

    # ==================================================
    # TODAY PURCHASES
    # ==================================================

    @staticmethod
    def today_purchases(user_id):
        return Purchase.query.filter(
            Purchase.user_id == user_id,
            db.func.date(Purchase.purchase_date) == date.today()
        ).count()

# Service Alias for purchase route imports
PurchaseService = SalesService