# MediTracker

**MediTracker** is a web-based **Medicine Inventory and Management System** developed using **Python and Flask**. It helps pharmacies and medical stores manage medicines, monitor stock levels, track expiry dates, manage suppliers and purchases, record sales, maintain transaction history, and generate reports.

---

## 📌 About

MediTracker provides a centralized system for managing day-to-day medicine inventory operations.

The application allows authorized users to:

* Manage medicine inventory
* Monitor available stock
* Identify low-stock medicines
* Track expired and soon-to-expire medicines
* Manage suppliers
* Record medicine purchases
* Record medicine sales
* Maintain transaction history
* Import and export medicine data
* Generate CSV, Excel, and PDF reports
* Manage users and authentication
* View dashboard statistics and charts
* Access application functionality through REST APIs

The system uses **SQLite** for persistent data storage and **SQLAlchemy / Flask-SQLAlchemy** for database interaction.

---

# ✨ Features

## 1. 🔐 User Authentication

MediTracker provides authentication and authorization functionality.

Features include:

* User registration
* User login
* User logout
* Password hashing
* Session management
* Role-based access control
* Protected routes
* Admin-only functionality

Supported roles:

* Admin
* Staff
* User

---

## 2. 💊 Medicine Inventory Management

Users can manage medicines through the Medicine Inventory section.

Features include:

* Add medicines
* View medicines
* Update medicine details
* Delete medicines
* Search medicines
* Filter by category
* Track batch numbers
* Track quantity
* Track medicine price
* Track expiry dates
* Configure low-stock thresholds
* Pagination
* Stock status monitoring

Medicine records can contain:

* Medicine name
* Category
* Batch number
* Quantity
* Price
* Expiry date
* Low-stock threshold

---

## 3. ⚠️ Low Stock Monitoring

The system automatically identifies medicines whose quantity falls below the configured stock threshold.

For example:

```text
Low Stock Limit = 10
Current Quantity = 5
Status = Low Stock
```

This helps users identify medicines that need to be replenished.

---

## 4. 📅 Expiry Tracking

MediTracker monitors medicine expiry dates and identifies:

* Expired medicines
* Medicines approaching expiry
* Valid medicines

The default expiry alert period is:

```text
30 days
```

This allows users to take action before medicines expire.

---

## 5. 📊 Dashboard

The dashboard provides a centralized overview of inventory activity.

It displays:

* Total medicines
* Low-stock medicines
* Expired medicines
* Expiring-soon medicines
* Inventory value
* Medicine category distribution
* Monthly sales information
* Low-stock medicine list
* Expiring medicine list
* Recently expired medicines
* Recent activity

Charts and tables are used to make inventory information easier to understand.

---

## 6. 🚚 Supplier Management

The Supplier Management module allows users to maintain supplier information.

Supplier details can include:

* Supplier name
* Company name
* Contact person
* Phone number
* Email
* GST number
* Supplier type
* Website
* City
* State
* Postal code
* Country
* Active/inactive status
* Notes

Users can:

* Add suppliers
* View suppliers
* Edit suppliers
* Delete suppliers
* Search suppliers
* Filter suppliers by status

---

## 7. 🛒 Purchase Management

The Purchase Management module records medicine purchases from suppliers.

Users can record:

* Supplier
* Medicine
* Purchase quantity
* Purchase price
* Discount
* GST
* Total amount
* Payment method
* Purchase status
* Notes

A purchase can increase the available medicine stock.

Example:

```text
Existing Stock = 20
Purchased Quantity = 30

New Stock = 20 + 30
          = 50
```

Purchase information is also recorded for transaction tracking and reporting.

---

## 8. 💰 Sales Management

The Sales Management module handles medicine sales and customer billing.

Users can record:

* Medicine
* Customer name
* Customer phone
* Quantity
* Sale price
* Total amount
* Invoice number
* Sale date

When a medicine is sold, the corresponding inventory quantity is reduced.

Example:

```text
Initial Stock = 100
Sold Quantity = 10

Remaining Stock = 100 - 10
                = 90
```

The sale is also recorded as a transaction.

The system can also calculate sales revenue and estimated profit.

---

## 9. 📋 Transaction Management

MediTracker maintains an inventory transaction ledger to track stock movements and important inventory activities.

Transaction types include:

```text
IN
OUT
SALE
PURCHASE
EXPIRED
```

The transaction history can contain:

* Transaction ID
* Timestamp
* Medicine
* Batch number
* Movement type
* Quantity
* User who performed the operation
* Remarks/reference

Users can filter transactions by:

* Transaction type
* Date range
* Medicine name
* Batch number

This provides an audit trail of inventory activity.

---

## 10. 📥 Import and Export

MediTracker supports data import and export functionality.

### Import

Medicine information can be imported using:

```text
CSV
```

### Export

Data can be exported as:

```text
CSV
Excel (.xlsx)
PDF
```

This allows users to maintain offline records and perform further analysis.

---

## 11. 📄 Report Generation

The system provides report generation functionality.

Supported formats:

```text
CSV
Excel (.xlsx)
PDF
```

Reports can be generated for application data such as:

* Medicine inventory
* Transactions
* Stock movements
* Sales
* Purchases

---

## 12. 📧 Email Alerts

The application contains email notification configuration for inventory alerts.

Email notifications can be used for:

* Medicine expiry alerts
* Low-stock alerts

Example email subjects include:

```text
Medicine Expiry Alert
Low Stock Alert
MediTracker Test Email
```

Email configuration is handled through environment variables.

---

## 13. 🌐 REST API

MediTracker includes an API layer for communication between the backend and external clients or frontend components.

The API uses the following prefix:

```text
/api/v1
```

The API provides structured access to application data and functionality.

---

## 14. ✅ Validation

The application includes backend validation utilities.

Validation can include:

* Email validation
* Phone number validation
* Password strength validation
* Date validation
* File extension validation
* Positive number validation

Password validation checks for:

* Minimum 8 characters
* Uppercase letter
* Lowercase letter
* Number

---

## 15. 🛠️ Utility Functions

The project contains reusable helper functions for common operations, including:

* Currency formatting
* Date formatting
* Date/time formatting
* Stock value calculation
* Safe integer conversion
* Safe float conversion
* Percentage calculation
* Invoice number generation
* Purchase number generation
* File size formatting
* Unique filename generation
* Text truncation

---

# 🧰 Technology Stack

## Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-WTF
* Werkzeug

## Database

* SQLite
* SQLAlchemy ORM

## Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap
* Font Awesome
* Jinja2

## Data Processing and Reports

* Pandas
* OpenPyXL
* ReportLab
* Matplotlib

## Authentication and Security

* Flask-Login
* Werkzeug password hashing
* Session-based authentication
* Role-based authorization
* CSRF protection

## Configuration

* python-dotenv
* Environment variables

## Testing

* Pytest

---

# 🏗️ Project Architecture

MediTracker follows a modular Flask architecture using **Blueprints**, a **service layer**, **SQLAlchemy ORM**, and reusable utilities.

```text
MediTracker/
│
├── app.py
├── config.py
├── constant.py
├── decorators.py
├── helper.py
├── validator.py
├── requirement.txt
├── README.md
│
├── database/
│   └── database.py
│
├── models/
│   ├── user.py
│   ├── medicine.py
│   ├── supplier.py
│   ├── purchase.py
│   ├── sale.py
│   └── transaction.py
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── medicine.py
│   ├── supplier.py
│   ├── purchase.py
│   ├── sales.py
│   ├── transaction.py
│   ├── report.py
│   ├── import_export.py
│   └── api.py
│
├── services/
│   ├── inventory_service.py
│   ├── supplier_service.py
│   ├── sales_service.py
│   ├── report_service.py
│   ├── csv_service.py
│   └── pdf_service.py
│
├── templates/
│   ├── auth/
│   ├── dashboard/
│   ├── medicines/
│   ├── suppliers/
│   ├── purchases/
│   ├── sales/
│   ├── transactions/
│   └── reports/
│
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
│
├── instance/
│   └── medicine_tracker.db
│
└── tests/
    ├── test_auth.py
    ├── test_import.py
    ├── test_medicine.py
    └── test_sales.py
```

---

# 🔄 Application Workflow

The overall application workflow can be represented as:

```text
                         User
                           │
                           ▼
                  Login / Registration
                           │
                           ▼
                    Authentication
                           │
                           ▼
                       Dashboard
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        Medicines      Suppliers      Reports
             │             │
             │             ▼
             │         Purchases
             │             │
             └──────┬──────┘
                    ▼
                Stock Update
                    │
                    ▼
                  Sales
                    │
                    ▼
              Transactions
                    │
                    ▼
                 Reports
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
         CSV      Excel      PDF
```

---

# 🔁 Request Flow

A typical MediTracker request follows this architecture:

```text
Browser
   │
   ▼
Flask Route / Blueprint
   │
   ▼
Service Layer
   │
   ▼
SQLAlchemy ORM
   │
   ▼
SQLite Database
   │
   ▼
Python Objects / Results
   │
   ▼
Jinja2 Template
   │
   ▼
HTML Response
   │
   ▼
Browser
```

For example, when viewing transactions:

```text
Browser
   │
   ▼
/transactions/
   │
   ▼
transaction Blueprint
   │
   ▼
transactions() route
   │
   ▼
ReportService.get_transactions()
   │
   ▼
SQLAlchemy
   │
   ▼
SQLite
   │
   ▼
Transaction records
   │
   ▼
transactions.html
   │
   ▼
Browser
```

---

# 🗄️ Database

MediTracker uses **SQLite** as its default database.

The database file is stored at:

```text
instance/medicine_tracker.db
```

SQLAlchemy is used as the ORM layer between the Flask application and SQLite.

The main database entities include:

```text
User
Medicine
Supplier
Purchase
Sale
Transaction
```

Conceptually:

```text
Flask Application
       │
       ▼
SQLAlchemy ORM
       │
       ▼
SQLite
       │
       ▼
medicine_tracker.db
```

---

# ⚙️ Configuration

Important application settings are centralized in configuration files such as `config.py` and `constant.py`.

Example configuration values:

```text
Low Stock Limit       = 10
Expiry Alert Days     = 30
Default Currency      = INR
Currency Symbol       = ₹
Items Per Page        = 10
Maximum Upload Size   = 16 MB
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd MediTracker
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirement.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/medicine_tracker.db

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

> **Important:** Never commit real passwords, API keys, email credentials, or other secrets to GitHub.

---

# ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000/
```

---

# 🧪 Testing

MediTracker uses **Pytest** for testing.

Run all tests:

```bash
pytest -q
```

Run a specific test file:

```bash
pytest tests/test_auth.py
```

```bash
pytest tests/test_medicine.py
```

```bash
pytest tests/test_sales.py
```

---

# 🧪 Testing Coverage

## Authentication Tests

Tests include:

* User registration
* Successful login
* Invalid login
* Protected route access
* Logout

## Medicine Tests

Tests include:

* Adding medicine
* Retrieving medicine
* Updating medicine
* Deleting medicine
* Expired medicine detection
* Valid expiry detection

## Sales Tests

Tests include:

* Successful medicine sale
* Stock reduction
* Preventing sales beyond available stock
* Invalid medicine handling
* Sale transaction creation

## Import Tests

Tests verify that important project components can be imported successfully, including:

* Models
* Database components
* Blueprints
* Application components

---

# 🔒 Security

MediTracker implements several security mechanisms:

* Password hashing
* Login session management
* Role-based authorization
* Protected routes
* HTTP-only session cookies
* SameSite cookie protection
* CSRF protection
* File upload validation
* Environment-based secret configuration

---

# 📈 Example Dashboard

The dashboard provides real-time inventory statistics such as:

```text
Total Medicines      : 12,123
Low Stock            : 56
Expired              : 12
Expiring Soon        : 13
Inventory Value      : ₹209,093.00
```

It also provides:

* Medicine category distribution
* Monthly sales charts
* Low-stock medicines
* Expiring medicines
* Recently expired medicines
* Recent inventory activity

---

# 🔮 Future Improvements

Possible future improvements include:

* Migration from SQLite to MySQL/PostgreSQL for production
* Cloud database support
* Advanced role and permission management
* Automated scheduled email alerts
* Barcode/QR code scanning
* Prescription management
* Advanced analytics
* Cloud deployment
* REST API authentication using JWT
* Automated database migrations using Flask-Migrate

---

# 🎯 Project Objective

The main objective of MediTracker is to provide a centralized system for managing medicine inventory and related pharmacy operations.

Instead of maintaining medicine stock, suppliers, purchases, sales, expiry information, and transaction records separately, MediTracker combines these operations into a single web application.

The project demonstrates practical implementation of:

* Python
* Flask
* Web development
* Database management
* ORM
* Authentication
* Role-based authorization
* REST APIs
* Data processing
* Report generation
* Testing
* Modular software architecture

---

# 📄 License

This project was developed as an academic/project application for learning and demonstrating Python Flask, database management, web development, testing, and software architecture.
