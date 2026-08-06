# load_csv.py
import csv
import os
from datetime import datetime, date, timedelta
import random

from app import create_app
from database.database import db
from models.user import User
from models.medicine import Medicine
from models.supplier import Supplier
from models.sale import Sale
from models.expired_medicine import ExpiredMedicine

app = create_app()

def seed_database():
    with app.app_context():
        print("Finding target user...")
        user = User.query.first()
        if not user:
            print("No user found! Please register/login at least once.")
            return

        user_id = user.id
        print(f"Loading data for user: {user.username} (ID: {user_id})")

        # ---------------------------------------------------------
        # 1. Load Suppliers (All 15 Fields)
        # ---------------------------------------------------------
        suppliers_path = os.path.join("sample_data", "suppliers.csv")
        supplier_map = {}

        if os.path.exists(suppliers_path):
            with open(suppliers_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing = Supplier.query.filter_by(
                        name=row["name"], 
                        user_id=user_id
                    ).first()
                    
                    is_active_str = str(row.get("is_active", "True")).strip().lower()
                    is_active_val = is_active_str in ["true", "1", "yes"]

                    supplier_data = {
                        "name": row.get("name"),
                        "company_name": row.get("company_name"),
                        "gst_number": row.get("gst_number"),
                        "supplier_type": row.get("supplier_type", "Distributor"),
                        "contact_person": row.get("contact_person"),
                        "phone": row.get("phone"),
                        "email": row.get("email"),
                        "website": row.get("website"),
                        "address": row.get("address"),
                        "city": row.get("city"),
                        "state": row.get("state"),
                        "postal_code": row.get("postal_code"),
                        "country": row.get("country", "India"),
                        "is_active": is_active_val,
                        "notes": row.get("notes"),
                        "user_id": user_id
                    }

                    if not existing:
                        supp = Supplier(**supplier_data)
                        db.session.add(supp)
                        db.session.flush()  # Assigns supplier ID immediately
                        supplier_map[supp.name] = supp.id
                    else:
                        for key, val in supplier_data.items():
                            if key != "user_id":
                                setattr(existing, key, val)
                        supplier_map[existing.name] = existing.id

            db.session.commit()
            print("Suppliers imported with full fields.")

        # ---------------------------------------------------------
        # 2. Load Medicines (Linked via supplier_id)
        # ---------------------------------------------------------
        medicines_path = os.path.join("sample_data", "medicines.csv")
        inserted_medicines = []

        if os.path.exists(medicines_path):
            with open(medicines_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    exp_date = datetime.strptime(row["expiry_date"], "%Y-%m-%d").date() if row.get("expiry_date") else None
                    
                    # Look up supplier ID using supplier_name
                    supp_name = row.get("supplier_name")
                    linked_supplier_id = supplier_map.get(supp_name)

                    med = Medicine(
                        name=row["name"],
                        batch_number=row["batch_number"],
                        category=row.get("category", "General"),
                        quantity=int(row.get("quantity", 0)),
                        price=float(row.get("price", 0.0)),
                        expiry_date=exp_date,
                        low_stock_alert=int(row.get("low_stock_alert", 10)),
                        supplier_id=linked_supplier_id,
                        user_id=user_id
                    )
                    db.session.add(med)
                    inserted_medicines.append(med)

            db.session.commit()
            print("Medicines imported and linked to suppliers.")

        # ---------------------------------------------------------
        # 3. Load Expired Medicines
        # ---------------------------------------------------------
        expired_items = [
            {"name": "Aspirin Old Batch", "batch": "EX-001", "category": "Tablet", "qty": 10, "price": 2.0, "exp": date.today() - timedelta(days=12)},
            {"name": "Ciprofloxacin 500mg", "batch": "EX-002", "category": "Capsule", "qty": 15, "price": 12.0, "exp": date.today() - timedelta(days=5)},
        ]

        for item in expired_items:
            exp_med = ExpiredMedicine(
                name=item["name"],
                batch_number=item["batch"],
                category=item["category"],
                quantity=item["qty"],
                price=item["price"],
                expiry_date=item["exp"],
                original_value=item["qty"] * item["price"],
                loss_amount=item["qty"] * item["price"],
                expired_date=datetime.now() - timedelta(days=random.randint(1, 10)),
                user_id=user_id
            )
            db.session.add(exp_med)

        # ---------------------------------------------------------
        # 4. Generate Sales (WITH PROFIT MARGIN)
        # ---------------------------------------------------------
        # ---------------------------------------------------------
        # 4. Generate Sales
        # ---------------------------------------------------------
        if inserted_medicines:
            for i in range(25):
                random_med = random.choice(inserted_medicines)
                qty_sold = random.randint(1, 5)
                
                # Base cost price from Medicine table
                cost_price = float(random_med.price)
                
                # Add a markup (e.g., 20% to 40%) so sale_price > cost_price
                markup_factor = random.choice([1.20, 1.25, 1.30, 1.35, 1.40])
                selling_price = round(cost_price * markup_factor, 2)
                total_amount = round(qty_sold * selling_price, 2)
                
                sale_date = datetime.now() - timedelta(days=random.randint(0, 120))
                
                # DO NOT pass profit here; the model @property calculates it automatically
                sale = Sale(
                    medicine_id=random_med.id,
                    customer_name=f"Customer {i+1}",
                    quantity=qty_sold,
                    sale_price=selling_price,
                    total_amount=total_amount,
                    sale_date=sale_date,
                    user_id=user_id
                )
                db.session.add(sale)

        db.session.commit()
        print("Database load completed successfully!")

if __name__ == "__main__":
    seed_database()