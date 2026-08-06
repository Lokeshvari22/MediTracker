from app import create_app
from database.database import db
from models.purchase import Purchase

app = create_app()

with app.app_context():
    purchases = Purchase.query.all()
    for purchase in purchases:
        updated = False

        if purchase.discount is None:
            purchase.discount = 0.0
            updated = True

        if purchase.gst is None:
            purchase.gst = 0.0
            updated = True

        if purchase.total_amount is None or purchase.total_amount == 0:
            subtotal = (purchase.quantity or 0) * (purchase.purchase_price or 0.0)
            subtotal_after_discount = max(0.0, subtotal - (purchase.discount or 0.0))
            purchase.total_amount = subtotal_after_discount + (subtotal_after_discount * ((purchase.gst or 0.0) / 100))
            updated = True

        if updated:
            db.session.add(purchase)

    db.session.commit()
    print(f"Backfilled {len(purchases)} purchase rows.")
