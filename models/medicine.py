from datetime import date

from database.database import db


class Medicine(db.Model):

    __tablename__ = "medicines"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    batch_number = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(100))

    quantity = db.Column(db.Integer, default=0)

    price = db.Column(db.Float, nullable=False)

    expiry_date = db.Column(db.Date)

    low_stock_alert = db.Column(db.Integer, default=10)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id")
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    # Relationships
    supplier = db.relationship(
        "Supplier",
        back_populates="medicines"
    )

    user = db.relationship(
        "User",
        back_populates="medicines"
    )

    purchases = db.relationship(
        "Purchase",
        back_populates="medicine",
        cascade="all, delete-orphan"
    )

    sales = db.relationship(
        "Sale",
        back_populates="medicine",
        cascade="all, delete-orphan"
    )

    transactions = db.relationship(
        "Transaction",
        back_populates="medicine",
        cascade="all, delete-orphan"
    )

    expired = db.relationship(
        "ExpiredMedicine",
        back_populates="medicine",
        uselist=False,
        cascade="all, delete-orphan"
    )

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_alert

    @property
    def is_expired(self):
        if not self.expiry_date:
            return False
        return self.expiry_date < date.today()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "batch_number": self.batch_number,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price,
            "expiry_date": str(self.expiry_date) if self.expiry_date else None,
            "is_low_stock": self.is_low_stock,
            "is_expired": self.is_expired,
            "supplier_id": self.supplier_id
        }