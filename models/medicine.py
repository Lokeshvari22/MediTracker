from datetime import date, timedelta

from database.database import db


class Medicine(db.Model):

    __tablename__ = "medicines"

    # ==========================================================
    # Primary Key
    # ==========================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================================
    # Medicine Information
    # ==========================================================

    name = db.Column(
        db.String(150),
        nullable=False
    )

    batch_number = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    quantity = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    expiry_date = db.Column(
        db.Date
    )

    low_stock_alert = db.Column(
        db.Integer,
        default=10,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # ==========================================================
    # Foreign Keys
    # ==========================================================

    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "suppliers.id"
        ),
        nullable=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id"
        ),
        nullable=False
    )

    # ==========================================================
    # Relationships
    # ==========================================================

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

    # ----------------------------------------------------------
    # Expired Medicine Relationship
    # ----------------------------------------------------------
    #
    # One Medicine can have zero or more archived records.
    #
    # Do NOT use uselist=False here.
    #

    expired = db.relationship(
        "ExpiredMedicine",
        back_populates="medicine",
        foreign_keys="ExpiredMedicine.medicine_id"
    )

    # ==========================================================
    # Properties
    # ==========================================================

    @property
    def is_low_stock(self):
        """
        Returns True when current quantity is less than
        or equal to the configured low-stock alert level.
        """

        quantity = self.quantity or 0
        alert_level = self.low_stock_alert or 0

        return quantity <= alert_level

    # ----------------------------------------------------------

    @property
    def is_expired(self):
        """
        Returns True when the medicine expiry date
        is before today's date.
        """

        if not self.expiry_date:
            return False

        return self.expiry_date < date.today()

    # ----------------------------------------------------------

    @property
    def is_expiring_soon(self):
        """
        Returns True when the medicine expires between
        today and the next 30 days.
        """

        if not self.expiry_date:
            return False

        today = date.today()
        future_date = today + timedelta(days=30)

        return (
            today <= self.expiry_date <= future_date
        )

    # ----------------------------------------------------------

    @property
    def stock_value(self):
        """
        Current inventory value.
        """

        quantity = self.quantity or 0
        price = self.price or 0.0

        return quantity * price

    # ==========================================================
    # Dictionary
    # ==========================================================

    def to_dict(self):

        return {

            "id": self.id,

            "name": self.name,

            "batch_number": self.batch_number,

            "category": self.category,

            "quantity": self.quantity,

            "price": self.price,

            "expiry_date": (
                str(self.expiry_date)
                if self.expiry_date
                else None
            ),

            "low_stock_alert": self.low_stock_alert,

            "is_low_stock": self.is_low_stock,

            "is_expired": self.is_expired,

            "is_expiring_soon": self.is_expiring_soon,

            "stock_value": self.stock_value,

            "supplier_id": self.supplier_id,

            "user_id": self.user_id

        }