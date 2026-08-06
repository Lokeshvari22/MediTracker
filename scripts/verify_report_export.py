import os
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app
from services.csv_service import CSVService

app = create_app()
with app.app_context():
    uid = 1
    for rt in ['inventory','sales','purchase','expiry']:
        path = CSVService.export_report(uid, report_type=rt)
        print(rt, os.path.exists(path), path)
        if os.path.exists(path):
            print('size:', os.path.getsize(path))
