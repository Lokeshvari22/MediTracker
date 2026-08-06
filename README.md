# MediTracker — Smart Medicine Inventory & Expiry System

A comprehensive web application built with Python and Flask to manage medicine stock, track expiration dates, process point-of-sale transactions, and maintain supplier records.

---

## About

**MediTracker** is a multi-tenant inventory and expiry tracking platform designed for pharmacies, clinics, and medical stock managers. It provides real-time stock monitoring, automated low-stock and expiry alert thresholds, point-of-sale (POS) billing with dynamic profit margin tracking, supplier management, and immutable stock transaction audit logs.

---

## Features

- **Multi-Tenant Architecture:** Secure user authentication with complete data isolation per user account.
- **Dashboard Analytics:** High-level metrics for total inventory, stock valuation, low stock alerts, near-expiry alerts, daily sales revenue, and calculated profit margins.
- **Medicine Stock Management:** Complete CRUD functionality for medicines, including batch tracking, category assignment, cost pricing, expiry dates, and customizable low-stock alert thresholds.
- **Supplier Directory:** Comprehensive database of suppliers, distributors, and manufacturers with GSTIN codes, contact details, active status toggles, and item linkage.
- **Purchase Management:** Track replenishment orders from suppliers with automatic inventory quantity updates, GST rate calculations, and invoice logging.
- **Point-of-Sale (POS) & Sales Tracking:** Real-time billing system that computes sales subtotals, records customer details, updates stock levels automatically, and tracks profit margins dynamically.
- **Expiry & Loss Management:** Dedicated tracking for expired and near-expiry stock, featuring an archived history table to log disposed inventory financial loss.
- **Stock Movement Audit Logs:** Immutable audit trail logging every stock-in and stock-out event (purchases, sales, and manual adjustments) with timestamps.
- **Report Generation:** Comprehensive filter options and PDF reporting export capabilities for sales, inventory, and expiry data.

---

## Technology Stack

- **Backend:** [Python 3](https://www.python.org/) using the [Flask](https://flask.palletsprojects.com/) web framework and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) ORM.
- **Database:** [SQLite](https://www.sqlite.org/index.html) with relational table constraints and multi-tenant foreign keys.
- **Authentication:** Flask-Login with secure password hashing via Werkzeug.
- **Frontend:** HTML5, CSS3, JavaScript, Jinja2 Templating, and Bootstrap 5.

---

## Project Structure

```text
MediTracker/
│
├── app.py                               # Flask application entry point
├── config.py                            # Application configuration
├── requirements.txt                     # Python dependencies
├── README.md                            # Project documentation
├── .env                                 # Environment variables
├── .gitignore                           # Git ignored files
│
├── instance/
│   └── medicine_tracker.db              # SQLite database
│
├── database/
│   ├── __init__.py
│   ├── database.py                      # SQLAlchemy initialization
│   └── seed.py                          # Seed sample data
│
├── models/
│   ├── __init__.py
│   ├── user.py                          # User model
│   ├── medicine.py                      # Medicine inventory model
│   ├── supplier.py                      # Supplier model
│   ├── purchase.py                      # Purchase model
│   ├── sale.py                          # Sales model
│   ├── transaction.py                   # Stock transaction model
│   └── expired_medicine.py              # Expired medicine model
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                          # Authentication routes
│   ├── dashboard.py                     # Dashboard routes
│   ├── medicine.py                      # Medicine CRUD routes
│   ├── supplier.py                      # Supplier routes
│   ├── purchase.py                      # Purchase routes
│   ├── sales.py                         # POS & sales routes
│   ├── transaction.py                   # Transaction history routes
│   ├── report.py                        # Reports routes
│   ├── import_export.py                 # CSV Import/Export routes
│   └── api.py                           # REST API endpoints
│
├── services/
│   ├── auth_service.py                  # Authentication logic
│   ├── inventory_service.py             # Inventory management
│   ├── expiry_service.py                # Expiry detection
│   ├── sales_service.py                 # Sales processing
│   ├── supplier_service.py              # Supplier operations
│   ├── report_service.py                # Report generation
│   ├── csv_service.py                   # CSV import/export
│   ├── pdf_service.py                   # PDF generation
│   ├── analytics_service.py             # Dashboard analytics
│   └── email_service.py                 # Email notifications
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   │
│   ├── dashboard.html
│   │
│   ├── medicines/
│   │   ├── medicines.html
│   │   ├── add_medicine.html
│   │   ├── edit_medicine.html
│   │   ├── import_csv.html
│   │   ├── export.html
│   │   └── expired.html
│   │
│   ├── suppliers/
│   │   ├── suppliers.html
│   │   ├── add_supplier.html
│   │   └── edit_supplier.html
│   │
│   ├── purchases/
│   │   ├── purchases.html
│   │   ├── add_purchase.html
│   │   └── purchase_details.html
│   │
│   ├── sales/
│   │   ├── sales.html
│   │   ├── sell_medicine.html
│   │   └── invoice.html
│   │
│   ├── reports/
│   │   ├── reports.html
│   │   ├── analytics.html
│   │   └── charts.html
│   │
│   └── transactions/
│       └── transactions.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── dashboard.css
│   │   ├── medicine.css
│   │   ├── report.css
│   │   └── auth.css
│   │
│   ├── js/
│   │   ├── dashboard.js
│   │   ├── medicine.js
│   │   ├── import.js
│   │   ├── report.js
│   │   └── validation.js
│   │
│   ├── images/
│   │
│   └── uploads/
│       ├── csv/
│       ├── reports/
│       └── invoices/
│
├── utils/
│   ├── validators.py                    # Input validation
│   ├── helpers.py                       # Helper functions
│   ├── constants.py                     # Global constants
│   └── decorators.py                    # Custom decorators
│
├── analytics/
│   ├── stock_analysis.py                # Stock analytics
│   ├── expiry_analysis.py               # Expiry analytics
│   ├── sales_analysis.py                # Sales analytics
│   └── dashboard_metrics.py             # Dashboard KPIs
│
├── reports/
│   ├── pdf_generator.py                 # PDF reports
│   ├── excel_generator.py               # Excel reports
│   └── csv_generator.py                 # CSV reports
│
├── mail/
│   ├── email_sender.py                  # Email sender
│   └── templates/
│       ├── expiry_alert.html
│       └── low_stock_alert.html
│
├── sample_data/
│   ├── medicines.csv
│   ├── suppliers.csv
│   └── demo_database.db
│
├── tests/
│   ├── test_auth.py
│   ├── test_medicine.py
│   ├── test_sales.py
│   └── test_import.py
│
└── docs/
    ├── Project_Plan.md
    ├── Database_Schema.md
    ├── API_Documentation.md
    ├── User_Guide.md
    └── Screenshots/
```

---

# Getting Started

Follow these steps to set up and run the project locally.

## Prerequisites

- Python 3.10 or higher
- pip (Python Package Installer)
- Git

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/MediTracker.git
cd MediTracker
```

---

### 2. Create a Virtual Environment

#### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Seed Sample Data (Optional)

Populate the database with sample medicines, suppliers, purchases, and transactions.

```bash
python -m database.seed
```

---

# Running the Application

### Start the Flask Development Server

```bash
python app.py
```

You should see output similar to:

```text
* Running on http://127.0.0.1:5000/
```

---

## Open in Browser

Visit:

```text
http://127.0.0.1:5000/
```

---

## Login / Register

Create a new account or log in with your existing credentials to access the dashboard.

---

# Running Tests

Execute the test suite using:

```bash
pytest -q
```

---

# Reports

The application can generate reports for:

- Inventory Summary
- Sales Report
- Purchase Report
- Expired Medicines Report
- Profit Analysis
- Low Stock Report
- Near Expiry Report

Reports can be filtered by date range and exported as PDF.

---

# Future Enhancements

- Barcode Scanner Integration
- Email Notifications for Expiry Alerts
- QR Code Based Billing
- GST Invoice Printing
- Customer Management Module
- Role-Based Access Control (Admin/Staff)
- REST API Support
- Docker Deployment
- PostgreSQL/MySQL Support
- Cloud Backup
- Mobile Responsive Dashboard

---

# License

This project is intended for educational and portfolio purposes.

---

# Author

**Lokeshvari S.**

