from sqlalchemy import or_

from database.database import db

from models.medicine import Medicine
from models.supplier import Supplier


class SupplierService:

    # ----------------------------------
    # Add Supplier
    # ----------------------------------

    @staticmethod
    def add_supplier(data, user_id):

        name = data["name"].strip()

        if not name:
            raise ValueError(
                "Supplier name is required."
            )

        existing = Supplier.query.filter_by(
            name=name,
            user_id=user_id
        ).first()

        if existing:
            raise ValueError(
                "Supplier already exists."
            )

        supplier = Supplier(
            name=name,
            company_name=data.get("company_name", "").strip(),
            gst_number=data.get("gst_number", "").strip(),
            supplier_type=data.get("supplier_type", "").strip(),
            website=data.get("website", "").strip(),
            contact_person=data.get("contact_person", "").strip(),
            phone=data.get("phone", "").strip(),
            email=data.get("email", "").strip(),
            address=data.get("address", "").strip(),
            city=data.get("city", "").strip(),
            state=data.get("state", "").strip(),
            postal_code=data.get("postal_code", "").strip(),
            country=data.get("country", "India").strip() or "India",
            is_active=bool(int(data.get("is_active", "1"))),
            notes=data.get("notes", "").strip(),
            user_id=user_id
        )

        db.session.add(supplier)
        db.session.commit()

        return supplier

    # ----------------------------------
    # Get Supplier
    # ----------------------------------

    @staticmethod
    def get_supplier(
        supplier_id,
        user_id
    ):

        return Supplier.query.filter_by(

            id=supplier_id,

            user_id=user_id

        ).first()

    # ----------------------------------
    # Update Supplier
    # ----------------------------------

    @staticmethod
    def update_supplier(
        supplier,
        data
    ):

        supplier.name = data["name"].strip()
        supplier.company_name = data.get("company_name", "").strip()
        supplier.gst_number = data.get("gst_number", "").strip()
        supplier.supplier_type = data.get("supplier_type", "").strip()
        supplier.website = data.get("website", "").strip()
        supplier.contact_person = data.get("contact_person", "").strip()
        supplier.phone = data.get("phone", "").strip()
        supplier.email = data.get("email", "").strip()
        supplier.address = data.get("address", "").strip()
        supplier.city = data.get("city", "").strip()
        supplier.state = data.get("state", "").strip()
        supplier.postal_code = data.get("postal_code", "").strip()
        supplier.country = data.get("country", "India").strip() or "India"
        supplier.is_active = bool(int(data.get("is_active", "1")))
        supplier.notes = data.get("notes", "").strip()

        db.session.commit()

        return supplier

    # ----------------------------------
    # Delete Supplier
    # ----------------------------------

    @staticmethod
    def delete_supplier(
        supplier
    ):

        db.session.delete(
            supplier
        )

        db.session.commit()

    # ----------------------------------
    # List Suppliers (Pagination)
    # ----------------------------------

    @staticmethod
    def list_suppliers(
        user_id,
        page=1,
        per_page=10,
        status=""
    ):

        query = Supplier.query.filter_by(
            user_id=user_id
        )

        if status == "active":
            query = query.filter_by(is_active=True)
        elif status == "inactive":
            query = query.filter_by(is_active=False)

        return query.order_by(
            Supplier.name.asc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    # ----------------------------------
    # List All Suppliers
    # ----------------------------------

    @staticmethod
    def list_all(
        user_id
    ):

        return Supplier.query.filter_by(

            user_id=user_id

        ).order_by(

            Supplier.name.asc()

        ).all()

    # ----------------------------------
    # Search Suppliers
    # ----------------------------------

    @staticmethod
    def search(
        keyword,
        user_id,
        status=""
    ):

        query = Supplier.query.filter(
            Supplier.user_id == user_id
        )

        if keyword:
            keyword = keyword.strip()
            query = query.filter(
                or_(
                    Supplier.name.ilike(f"%{keyword}%"),
                    Supplier.company_name.ilike(f"%{keyword}%"),
                    Supplier.phone.ilike(f"%{keyword}%"),
                    Supplier.email.ilike(f"%{keyword}%"),
                    Supplier.contact_person.ilike(f"%{keyword}%")
                )
            )

        if status == "active":
            query = query.filter_by(is_active=True)
        elif status == "inactive":
            query = query.filter_by(is_active=False)

        return query.order_by(
            Supplier.name.asc()
        ).all()

    @staticmethod
    def search_suppliers(
        keyword,
        user_id,
        status=""
    ):

        return SupplierService.search(
            keyword=keyword,
            user_id=user_id,
            status=status
        )

    # ----------------------------------
    # Count Suppliers
    # ----------------------------------

    @staticmethod
    def total_suppliers(
        user_id
    ):

        return Supplier.query.filter_by(
            user_id=user_id
        ).count()

    @staticmethod
    def total_active_suppliers(
        user_id
    ):

        return Supplier.query.filter_by(
            user_id=user_id,
            is_active=True
        ).count()

    @staticmethod
    def total_medicines_supplied(
        user_id
    ):

        return Medicine.query.filter(
            Medicine.user_id == user_id,
            Medicine.supplier_id.isnot(None)
        ).count()