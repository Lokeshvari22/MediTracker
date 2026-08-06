# MediTrack
## User Guide

Version: 1.0

---

# 1. Introduction

## 1.1 About MediTrack

MediTrack is a Smart Medicine Inventory and Expiry Management System designed to help pharmacies and medical stores efficiently manage medicines, monitor stock levels, track expiry dates, and maintain transaction records.

The system reduces manual work by providing automated alerts for:

- Expiring medicines
- Low stock medicines
- Expired inventory
- Stock value monitoring

The application provides a centralized dashboard where users can manage medicine information and monitor pharmacy operations.

---

# 2. System Features

## 2.1 User Authentication

Users can securely access the system using their registered accounts.

Available operations:

- User registration
- Login
- Logout
- Protected dashboard access

---

# 3. Dashboard

After login, users are redirected to the dashboard.

The dashboard provides an overview of pharmacy inventory.

## Dashboard Information

### Total Medicines

Displays the total number of medicines available in inventory.

### Expiring Medicines

Shows medicines that are approaching their expiry date.

### Expired Medicines

Displays medicines that have already crossed their expiry date.

### Low Stock Alerts

Shows medicines whose quantity is below the configured minimum stock level.

### Stock Value

Displays the total value of available medicine inventory.

### Sales Summary

Provides information about recent medicine sales.

---

# 4. Medicine Management

## 4.1 Add Medicine

Users can add new medicines into the inventory.

Required details:

- Medicine Name
- Batch Number
# 10. Installation & Requirements

Minimum requirements:

- Python 3.8+
- pip
- Optional: access to SMTP credentials for email alerts

Recommended developer setup:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirement.txt
```

Notes:
- The project uses `Flask` with `Flask-SQLAlchemy`. By default it uses an SQLite file stored under `instance/`.
- If you need production deployment, consider using PostgreSQL or MySQL and a WSGI server (Gunicorn/Waitress).

---

# 11. Running the Application (Local Development)

1. Activate your virtualenv (Windows PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

2. Initialize or seed the database (if a seeder is provided):

```powershell
python database/seed.py
```

3. Run the Flask app:

```powershell
python app.py
```

4. Open the app in your browser:

http://127.0.0.1:5000/

---

# 12. Running Tests

Install test dependencies and run `pytest`:

```powershell
pip install pytest
pytest -q
```

There is a small export test runner available to exercise CSV/Excel/PDF export flows:

```powershell
python tests/run_export_test.py
# or the helper runner
python run_export_test_runner.py
```

Note: tests expect dependencies installed and a writable `Static/uploads/reports/` folder.

---
- Low stock items
- Out-of-stock medicines

---

## 6.2 Low Stock Alerts

When medicine quantity reaches the configured alert limit, the system displays a warning.

Example:

```

Medicine:
Paracetamol

Current Quantity:
5

Alert Level:
10

Status:
Low Stock

```

Recommended action:

Restock medicines before availability becomes zero.

---

# 7. Sales and Transactions

The transaction module maintains records of inventory changes.

Transactions include:

- Stock addition
- Medicine sales
- Stock reduction

Each transaction stores:

- Medicine information
- Quantity changed
- Transaction type
- Date and time
- User information

---

# 8. Reports

Users can generate useful inventory insights.

Available reports:

## Inventory Report

Contains complete medicine details.

## Expiry Report

Lists medicines based on expiry status.

## Stock Report

Shows available quantities.

## Sales Report

Provides sales-related information.

---

# 9. User Workflow

## Daily Pharmacy Workflow

### Step 1

Login into MediTrack.

### Step 2

Check dashboard alerts.

### Step 3

Review:

- Expiring medicines
- Low stock medicines

### Step 4

Add new stock when required.

### Step 5

Update transactions after sales.

### Step 6

Review reports.

---

# 10. Installation Guide

## Requirements

Software requirements:

- Python 3.x
- Database Server
- Web Browser

Hardware requirements:

- Minimum 4GB RAM
- Internet connection
- Modern browser

---

# 11. Running the Application

## Backend Setup

Navigate to backend directory:

```

cd backend

```

Create virtual environment:

```

python -m venv venv

```

Activate environment:

Windows:

```

venv\Scripts\activate

```

Install dependencies:

```

pip install -r requirements.txt

```

Run backend server:

```

python app.py

```

---

## Frontend Setup

Navigate to frontend:

```

cd frontend

```

Install packages:

```

npm install

```

Start application:

```

npm run dev

```

---

# 12. Troubleshooting

## Problem: Unable to Login

Solutions:

- Check username and password.
- Verify database connection.
- Restart the application.

---

## Problem: Medicines Not Displaying

Solutions:

- Check database status.
- Refresh the page.
- Verify API connection.

---

## Problem: Expiry Alerts Not Showing

Solutions:

- Verify medicine expiry dates.
- Check system date.
- Confirm database records.

---

# 13. Security Guidelines

Users should:

- Keep login credentials secure.
- Avoid sharing accounts.
- Logout after completing work.
- Regularly backup database records.

---

# 14. Future Enhancements

Possible improvements:

- AI-based medicine demand prediction
- Barcode scanning
- Mobile application
- Cloud deployment
- Automated supplier management
- Email/SMS expiry notifications

---

# 15. Conclusion

MediTrack provides an efficient solution for medicine inventory management by combining stock tracking, expiry monitoring, transaction management, and reporting features.

The system helps pharmacies reduce medicine wastage, improve inventory accuracy, and make better operational decisions.

-