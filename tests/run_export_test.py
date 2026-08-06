from app import create_app
from database.database import db
from services.auth_service import AuthService
import os

app = create_app()

with app.app_context():
    db.create_all()

    email = "tester@example.com"
    username = "tester"
    password = "password123"

    if not AuthService.email_exists(email):
        success, msg = AuthService.register_user(username, email, password)
        print('register:', success, msg)
    else:
        print('user exists')

    client = app.test_client()

    # Login
    resp = client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)
    print('login status', resp.status_code)

    # Ensure reports folder exists
    reports_dir = os.path.join('static', 'uploads', 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    # Test CSV export (inventory)
    r = client.get('/reports/export/csv?report_type=inventory')
    print('csv status', r.status_code, r.headers.get('Content-Type'))
    if r.status_code == 200:
        out = os.path.join(reports_dir, 'test_inventory.csv')
        with open(out, 'wb') as f:
            f.write(r.data)
        print('wrote', out)

    # Test Excel export (inventory)
    r = client.get('/reports/export/excel?report_type=inventory')
    print('excel status', r.status_code, r.headers.get('Content-Type'))
    if r.status_code == 200:
        out = os.path.join(reports_dir, 'test_inventory.xlsx')
        with open(out, 'wb') as f:
            f.write(r.data)
        print('wrote', out)

    # Test PDF export (inventory)
    r = client.get('/reports/export/pdf?report_type=inventory')
    print('pdf status', r.status_code, r.headers.get('Content-Type'))
    if r.status_code == 200:
        out = os.path.join(reports_dir, 'test_inventory.pdf')
        with open(out, 'wb') as f:
            f.write(r.data)
        print('wrote', out)

    print('done')
