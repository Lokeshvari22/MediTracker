import os
import sys

# Ensure project root is on sys.path when running this script directly
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app

from services.report_service import ReportService
from services.sales_service import SalesService
from models.purchase import Purchase
from database.database import db

app = create_app()

with app.app_context():
    uid = 1
    print('=== Transaction Summary for user_id=', uid)
    summary = ReportService.transaction_summary(uid)
    print(summary)

    pag = ReportService.get_transactions(user_id=uid, page=1, per_page=5)
    print('\nFetched transactions page 1 - total:', pag.total)
    for t in pag.items:
        print('T', t.id, t.transaction_type, t.quantity, getattr(t, 'batch_number', None), t.transaction_date)

    # Quick filter checks
    for ttype in ['SALE', 'PURCHASE', 'IN', 'OUT']:
        p = ReportService.get_transactions(user_id=uid, page=1, per_page=1, transaction_type=ttype)
        print(f"Filter {ttype}: total={p.total}")

    # Date filter: today
    from datetime import date
    today = date.today().isoformat()
    p_today = ReportService.get_transactions(user_id=uid, page=1, per_page=5, from_date=today, to_date=today)
    print('Transactions today total (by date filter):', p_today.total)

    # Search filter (empty string likely returns all)
    p_search = ReportService.get_transactions(user_id=uid, page=1, per_page=5, search='')
    print('Search empty returns:', p_search.total)

    print('\nSales counts and revenue:')
    print('total_sales:', SalesService.total_sales(uid))
    try:
        print('today_sales:', SalesService.today_sales(uid))
    except Exception as e:
        print('today_sales error', e)
    print('total_revenue:', SalesService.total_revenue(uid))
    try:
        print('total_profit:', SalesService.total_profit(uid))
    except Exception as e:
        print('total_profit error', e)

    print('\nPurchase counts:')
    purchases = Purchase.query.filter_by(user_id=uid).count()
    print('purchases:', purchases)
