from database.database import db


class Sale(db.Model):

    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)

    invoice_number = db.Column(db.String(100), nullable=True)

    sale_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    quantity = db.Column(db.Integer, nullable=False)

    sale_price = db.Column(db.Float, nullable=False)

    total_amount = db.Column(db.Float, nullable=False)

    discount = db.Column(db.Float, default=0.0)

    gst = db.Column(db.Float, default=0.0)

    customer_name = db.Column(db.String(150), nullable=True)

    customer_phone = db.Column(db.String(20), nullable=True)

    payment_method = db.Column(db.String(50), default="Cash")

    notes = db.Column(db.Text, nullable=True)

    medicine_id = db.Column(
        db.Integer,
        db.ForeignKey("medicines.id")
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    # Relationships
    medicine = db.relationship(
        "Medicine",
        back_populates="sales"
    )

    user = db.relationship(
        "User",
        back_populates="sales"
    )

    @property
    def subtotal(self):
        return (self.quantity or 0) * (self.sale_price or 0.0)

    @property
    def profit(self):
        cost_price = self.medicine.price if self.medicine else 0.0
        return self.total_amount - (cost_price * self.quantity)

    def to_dict(self):
        return {
            "id": self.id,
            "invoice_number": self.invoice_number or f"INV-{self.id}",
            "sale_date": str(self.sale_date) if self.sale_date else None,
            "quantity": self.quantity,
            "sale_price": self.sale_price,
            "total_amount": self.total_amount,
            "discount": self.discount,
            "gst": self.gst,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "payment_method": self.payment_method,
            "profit": self.profit,
            "medicine_id": self.medicine_id
        }