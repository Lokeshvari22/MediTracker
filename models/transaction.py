from database.database import db


class Transaction(db.Model):

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    transaction_type = db.Column(db.String(20))

    quantity = db.Column(db.Integer)

    remarks = db.Column(db.String(255))

    transaction_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    medicine_id = db.Column(
        db.Integer,
        db.ForeignKey("medicines.id")
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    medicine = db.relationship(
        "Medicine",
        back_populates="transactions"
    )

    user = db.relationship(
        "User",
        back_populates="transactions"
    )