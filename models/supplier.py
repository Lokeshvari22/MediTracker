from database.database import db
from sqlalchemy.orm import synonym


class Supplier(db.Model):

    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    name = db.Column(db.String(150), nullable=False)
    supplier_name = synonym("name")
    company_name = db.Column(db.String(150))
    gst_number = db.Column(db.String(50))
    supplier_type = db.Column(db.String(50))
    website = db.Column(db.String(255))
    contact_person = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(150))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default="India")
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    medicines = db.relationship(
        "Medicine",
        back_populates="supplier"
    )

    purchases = db.relationship(
        "Purchase",
        back_populates="supplier"
    )

    @property
    def status(self):
        is_active = getattr(self, "is_active", None)
        if is_active is None:
            return "Active"
        return "Active" if is_active else "Inactive"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company_name": self.company_name,
            "gst_number": self.gst_number,
            "supplier_type": self.supplier_type,
            "website": self.website,
            "contact_person": self.contact_person,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country,
            "is_active": self.is_active,
            "notes": self.notes,
            "created_at": str(self.created_at) if self.created_at else None
        }