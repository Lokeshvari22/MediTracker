import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app
from services.report_service import ReportService
from services.analytics_service import AnalyticsService

app = create_app()
with app.app_context():
    uid = 1
    print('Report summary:', ReportService.get_report_summary(uid))
    print('Dashboard summary:', ReportService.dashboard_summary(uid))
    print('\nStock report sample (5):')
    stock = ReportService.stock_report(uid)
    for s in stock[:5]:
        print(s.id, s.name, s.quantity)
    print('\nSales report sample (5):')
    sales = ReportService.sales_report(uid)
    for s in sales[:5]:
        print(s.id, s.invoice_number, s.total_amount)
    print('\nPurchase report sample (5):')
    purchases = ReportService.purchase_report(uid)
    for p in purchases[:5]:
        print(p.id, p.supplier_id, p.total_amount)
    print('\nExpiry report sample (5):')
    expiry = ReportService.expiry_report(uid)
    for e in expiry[:5]:
        print(e.id, e.name, e.quantity)
    print('\nAnalytics dashboard data sample:')
    print(AnalyticsService.get_dashboard_data(uid))
