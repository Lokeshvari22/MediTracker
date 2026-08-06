from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from database.database import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    medicines = db.relationship(
        "Medicine",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    purchases = db.relationship(
        "Purchase",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    sales = db.relationship(
        "Sale",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    transactions = db.relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    exports = db.relationship(
        "ExportHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @property
    def role(self):
        return "Admin" if self.is_admin else "User"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)