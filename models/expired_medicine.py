from database.database import db


class ExpiredMedicine(db.Model):

    __tablename__ = "expired_medicines"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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
        default=0,
        nullable=False
    )

    expiry_date = db.Column(
        db.Date
    )

    original_value = db.Column(
        db.Float,
        default=0
    )

    loss_amount = db.Column(
        db.Float,
        default=0
    )

    expired_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    medicine_id = db.Column(
        db.Integer,
        db.ForeignKey("medicines.id"),
        nullable=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    medicine = db.relationship(
        "Medicine",
        back_populates="expired"
    )

    user = db.relationship(
        "User",
        back_populates="expired_medicines"
    )

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    medicine = db.relationship(
        "Medicine",
        back_populates="expired"
    )

    user = db.relationship(
        "User"
    )

    # --------------------------------------------------
    # Dictionary
    # --------------------------------------------------

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
            "original_value": self.original_value,
            "loss_amount": self.loss_amount,
            "expired_date": (
                str(self.expired_date)
                if self.expired_date
                else None
            ),
            "medicine_id": self.medicine_id
        }