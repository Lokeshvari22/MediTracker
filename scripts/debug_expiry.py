import os
import sys
ROOT = os.path.abspath(os.path.dirname(__file__) + "\\..")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app
from models.expired_medicine import ExpiredMedicine
from models.medicine import Medicine

app = create_app()
with app.app_context():
    expired = ExpiredMedicine.query.limit(50).all()
    print('Expired count', len(expired))
    for e in expired:
        print('EXPIRED', e.id, e.name, e.batch_number, e.expiry_date, type(e.expiry_date), 'med_id', e.medicine_id)

    medicines = Medicine.query.filter(Medicine.expiry_date != None).limit(50).all()
    print('Medicines with expiry dates:', len(medicines))
    for m in medicines:
        print('MED', m.id, m.name, m.batch_number, m.expiry_date)
