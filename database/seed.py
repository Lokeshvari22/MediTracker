# load_csv.py

import os
import sys
import csv
import random

from datetime import datetime, date, timedelta

# Add project root to Python path
ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


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

        print("\n========================================")
        print("       MEDI TRACKER DATABASE SEED")
        print("========================================\n")

        # ---------------------------------------------------------
        # FIND USER
        # ---------------------------------------------------------

        print("Finding target user...")

        user = User.query.first()

        if not user:
            print("No user found!")
            print("Please register/login at least once.")
            return

        user_id = user.id

        print(
            f"Loading data for user: "
            f"{user.username} (ID: {user_id})"
        )

        # =========================================================
        # 1. LOAD SUPPLIERS
        # =========================================================

        print("\n[1/4] Loading suppliers...")

        suppliers_path = os.path.join(
            "sample_data",
            "suppliers.csv"
        )

        supplier_map = {}

        if os.path.exists(suppliers_path):

            with open(
                suppliers_path,
                mode="r",
                encoding="utf-8"
            ) as f:

                reader = csv.DictReader(f)

                for row in reader:

                    supplier_name = row.get("name")

                    if not supplier_name:
                        continue

                    # -------------------------------------------------
                    # CHECK EXISTING SUPPLIER
                    # -------------------------------------------------

                    existing = Supplier.query.filter_by(
                        name=supplier_name,
                        user_id=user_id
                    ).first()

                    # -------------------------------------------------
                    # CONVERT is_active
                    # -------------------------------------------------

                    is_active_str = str(
                        row.get(
                            "is_active",
                            "True"
                        )
                    ).strip().lower()

                    is_active_val = (
                        is_active_str
                        in ["true", "1", "yes"]
                    )

                    # -------------------------------------------------
                    # SUPPLIER DATA
                    # -------------------------------------------------

                    supplier_data = {

                        "name": supplier_name,

                        "company_name":
                            row.get("company_name"),

                        "gst_number":
                            row.get("gst_number"),

                        "supplier_type":
                            row.get(
                                "supplier_type",
                                "Distributor"
                            ),

                        "contact_person":
                            row.get("contact_person"),

                        "phone":
                            row.get("phone"),

                        "email":
                            row.get("email"),

                        "website":
                            row.get("website"),

                        "address":
                            row.get("address"),

                        "city":
                            row.get("city"),

                        "state":
                            row.get("state"),

                        "postal_code":
                            row.get("postal_code"),

                        "country":
                            row.get(
                                "country",
                                "India"
                            ),

                        "is_active":
                            is_active_val,

                        "notes":
                            row.get("notes"),

                        "user_id":
                            user_id
                    }

                    # -------------------------------------------------
                    # INSERT OR UPDATE SUPPLIER
                    # -------------------------------------------------

                    if not existing:

                        supplier = Supplier(
                            **supplier_data
                        )

                        db.session.add(supplier)

                        db.session.flush()

                        supplier_map[
                            supplier.name
                        ] = supplier.id

                    else:

                        for key, value in supplier_data.items():

                            if key != "user_id":
                                setattr(
                                    existing,
                                    key,
                                    value
                                )

                        supplier_map[
                            existing.name
                        ] = existing.id

            db.session.commit()

            print("Suppliers loaded successfully.")

        else:

            print(
                "suppliers.csv not found. "
                "Skipping suppliers."
            )

        # =========================================================
        # 2. LOAD MEDICINES
        # =========================================================

        print("\n[2/4] Loading medicines...")

        medicines_path = os.path.join(
            "sample_data",
            "medicines.csv"
        )

        inserted_medicines = []

        if os.path.exists(medicines_path):

            with open(
                medicines_path,
                mode="r",
                encoding="utf-8"
            ) as f:

                reader = csv.DictReader(f)

                for row in reader:

                    name = row.get("name")
                    batch_number = row.get("batch_number")

                    if not name or not batch_number:
                        continue

                    # -------------------------------------------------
                    # EXPIRY DATE
                    # -------------------------------------------------

                    expiry_date = None

                    if row.get("expiry_date"):

                        expiry_date = datetime.strptime(
                            row["expiry_date"],
                            "%Y-%m-%d"
                        ).date()

                    # -------------------------------------------------
                    # FIND SUPPLIER
                    # -------------------------------------------------

                    supplier_name = row.get(
                        "supplier_name"
                    )

                    supplier_id = supplier_map.get(
                        supplier_name
                    )

                    # -------------------------------------------------
                    # CHECK DUPLICATE MEDICINE
                    #
                    # A medicine is considered the same when:
                    # user + name + batch + expiry date
                    # -------------------------------------------------

                    existing = Medicine.query.filter_by(

                        user_id=user_id,

                        name=name,

                        batch_number=batch_number,

                        expiry_date=expiry_date

                    ).first()

                    # -------------------------------------------------
                    # IF EXISTS
                    # -------------------------------------------------

                    if existing:

                        print(
                            f"Skipping duplicate medicine: "
                            f"{name} | {batch_number}"
                        )

                        # Use existing medicine for sales
                        inserted_medicines.append(
                            existing
                        )

                        continue

                    # -------------------------------------------------
                    # CREATE MEDICINE
                    # -------------------------------------------------

                    medicine = Medicine(

                        name=name,

                        batch_number=batch_number,

                        category=row.get(
                            "category",
                            "General"
                        ),

                        quantity=int(
                            row.get(
                                "quantity",
                                0
                            )
                        ),

                        price=float(
                            row.get(
                                "price",
                                0.0
                            )
                        ),

                        expiry_date=expiry_date,

                        low_stock_alert=int(
                            row.get(
                                "low_stock_alert",
                                10
                            )
                        ),

                        supplier_id=supplier_id,

                        user_id=user_id
                    )

                    db.session.add(medicine)

                    db.session.flush()

                    inserted_medicines.append(
                        medicine
                    )

            db.session.commit()

            print(
                f"Medicines loaded successfully: "
                f"{len(inserted_medicines)}"
            )

        else:

            print(
                "medicines.csv not found. "
                "Skipping medicines."
            )

        # =========================================================
        # 3. LOAD EXPIRED MEDICINES
        # =========================================================

        print("\n[3/4] Loading expired medicines...")

        expired_items = [

            {
                "name":
                    "Aspirin Old Batch",

                "batch":
                    "EX-001",

                "category":
                    "Tablet",

                "qty":
                    10,

                "price":
                    2.0,

                "exp":
                    date.today()
                    - timedelta(days=12)
            },

            {
                "name":
                    "Ciprofloxacin 500mg",

                "batch":
                    "EX-002",

                "category":
                    "Capsule",

                "qty":
                    15,

                "price":
                    12.0,

                "exp":
                    date.today()
                    - timedelta(days=5)
            }
        ]

        expired_count = 0

        for item in expired_items:

            # -------------------------------------------------
            # CHECK DUPLICATE EXPIRED MEDICINE
            # -------------------------------------------------

            existing = ExpiredMedicine.query.filter_by(

                user_id=user_id,

                name=item["name"],

                batch_number=item["batch"],

                expiry_date=item["exp"]

            ).first()

            if existing:

                print(
                    f"Skipping duplicate expired medicine: "
                    f"{item['name']} | {item['batch']}"
                )

                continue

            # -------------------------------------------------
            # CREATE EXPIRED MEDICINE
            # -------------------------------------------------

            original_value = (
                item["qty"]
                * item["price"]
            )

            expired_record = ExpiredMedicine(

                name=item["name"],

                batch_number=item["batch"],

                category=item["category"],

                quantity=item["qty"],

                price=item["price"],

                expiry_date=item["exp"],

                original_value=original_value,

                loss_amount=original_value,

                expired_date=(
                    datetime.now()
                    - timedelta(
                        days=random.randint(
                            1,
                            10
                        )
                    )
                ),

                user_id=user_id
            )

            db.session.add(
                expired_record
            )

            expired_count += 1

        db.session.commit()

        print(
            f"Expired medicines added: "
            f"{expired_count}"
        )

        # =========================================================
        # 4. GENERATE SALES
        # =========================================================

        print("\n[4/4] Generating sales...")

        sales_count = 0

        if inserted_medicines:

            # -----------------------------------------------------
            # CHECK WHETHER SEED SALES ALREADY EXIST
            # -----------------------------------------------------

            existing_seed_sale = Sale.query.filter_by(
                user_id=user_id,
                invoice_number="SEED-001"
            ).first()

            if existing_seed_sale:

                print(
                    "Seed sales already exist."
                )

                print(
                    "Skipping sales generation."
                )

            else:

                for i in range(25):

                    random_med = random.choice(
                        inserted_medicines
                    )

                    qty_sold = random.randint(
                        1,
                        5
                    )

                    # -------------------------------------------------
                    # COST PRICE
                    # -------------------------------------------------

                    cost_price = float(
                        random_med.price
                    )

                    # -------------------------------------------------
                    # MARKUP
                    # -------------------------------------------------

                    markup_factor = random.choice(
                        [
                            1.20,
                            1.25,
                            1.30,
                            1.35,
                            1.40
                        ]
                    )

                    selling_price = round(
                        cost_price
                        * markup_factor,
                        2
                    )

                    # -------------------------------------------------
                    # TOTAL
                    # -------------------------------------------------

                    total_amount = round(
                        qty_sold
                        * selling_price,
                        2
                    )

                    # -------------------------------------------------
                    # SALE DATE
                    # -------------------------------------------------

                    sale_date = (
                        datetime.now()
                        - timedelta(
                            days=random.randint(
                                0,
                                120
                            )
                        )
                    )

                    # -------------------------------------------------
                    # UNIQUE SEED INVOICE
                    # -------------------------------------------------

                    invoice_number = (
                        f"SEED-{i + 1:03d}"
                    )

                    # -------------------------------------------------
                    # EXTRA SAFETY CHECK
                    # -------------------------------------------------

                    existing_sale = Sale.query.filter_by(

                        user_id=user_id,

                        invoice_number=invoice_number

                    ).first()

                    if existing_sale:

                        print(
                            f"Skipping existing sale: "
                            f"{invoice_number}"
                        )

                        continue

                    # -------------------------------------------------
                    # CREATE SALE
                    # -------------------------------------------------

                    sale = Sale(

                        invoice_number=
                            invoice_number,

                        medicine_id=
                            random_med.id,

                        customer_name=
                            f"Customer {i + 1}",

                        quantity=
                            qty_sold,

                        sale_price=
                            selling_price,

                        total_amount=
                            total_amount,

                        sale_date=
                            sale_date,

                        user_id=
                            user_id
                    )

                    db.session.add(
                        sale
                    )

                    sales_count += 1

                db.session.commit()

        else:

            print(
                "No medicines available. "
                "Skipping sales."
            )

        # =========================================================
        # COMPLETE
        # =========================================================

        print("\n========================================")
        print("       DATABASE LOAD COMPLETED")
        print("========================================")

        print(
            f"Suppliers : {len(supplier_map)}"
        )

        print(
            f"Medicines : {len(inserted_medicines)}"
        )

        print(
            f"Expired   : {expired_count}"
        )

        print(
            f"Sales     : {sales_count}"
        )

        print("========================================\n")


if __name__ == "__main__":
    seed_database()