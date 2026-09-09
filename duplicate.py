from app import create_app
from database.database import db
from models.medicine import Medicine
from models.expired_medicine import ExpiredMedicine

app = create_app()

with app.app_context():

    print("\n=== DUPLICATE MEDICINE DETAILS ===")

    duplicates = (
        db.session.query(
            Medicine.name,
            Medicine.batch_number,
            Medicine.expiry_date
        )
        .group_by(
            Medicine.name,
            Medicine.batch_number,
            Medicine.expiry_date
        )
        .having(db.func.count(Medicine.id) > 1)
        .all()
    )

    for name, batch, expiry in duplicates:

        print(f"\n{name} | {batch} | {expiry}")

        records = Medicine.query.filter_by(
            name=name,
            batch_number=batch,
            expiry_date=expiry
        ).order_by(Medicine.id).all()

        for m in records:
            print(
                f"  ID={m.id} "
                f"Qty={m.quantity} "
                f"Price={m.price} "
                f"Alert={m.low_stock_alert}"
            )


    print("\n=== DUPLICATE EXPIRED DETAILS ===")

    duplicates = (
        db.session.query(
            ExpiredMedicine.name,
            ExpiredMedicine.batch_number,
            ExpiredMedicine.expiry_date
        )
        .group_by(
            ExpiredMedicine.name,
            ExpiredMedicine.batch_number,
            ExpiredMedicine.expiry_date
        )
        .having(db.func.count(ExpiredMedicine.id) > 1)
        .all()
    )

    for name, batch, expiry in duplicates:

        print(f"\n{name} | {batch} | {expiry}")

        records = ExpiredMedicine.query.filter_by(
            name=name,
            batch_number=batch,
            expiry_date=expiry
        ).order_by(ExpiredMedicine.id).all()

        for e in records:
            print(
                f"  ID={e.id} "
                f"Qty={e.quantity} "
                f"Price={e.price} "
                f"Value={e.original_value}"
            )