from database.database import db
from sqlalchemy.ext.hybrid import hybrid_property


class Purchase(db.Model):
    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True)

    purchase_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    quantity = db.Column(db.Integer)

    purchase_price = db.Column(db.Float)

    discount = db.Column(db.Float, default=0.0)

    gst = db.Column(db.Float, default=0.0)

    total_amount = db.Column(db.Float, default=0.0)

    payment_method = db.Column(db.String(50), default="Cash")

    status = db.Column(db.String(50), default="Paid")

    notes = db.Column(db.Text, nullable=True)

    invoice_number = db.Column(db.String(100))

    medicine_id = db.Column(
        db.Integer,
        db.ForeignKey("medicines.id")
    )

    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id")
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    # Relationships
    medicine = db.relationship(
        "Medicine",
        back_populates="purchases"
    )

    supplier = db.relationship(
        "Supplier",
        back_populates="purchases"
    )

    user = db.relationship(
        "User",
        back_populates="purchases"
    )

    # Alias property for created_at compatibility
    @hybrid_property
    def created_at(self):
        return self.purchase_date

    @created_at.expression
    def created_at(cls):
        return cls.purchase_date