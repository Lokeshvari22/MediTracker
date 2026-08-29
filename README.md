# MediTracker

MediTracker is a web-based **Medicine Inventory and Management System** developed using Python and Flask. It helps pharmacies or medical stores manage medicines, monitor stock levels, track expiry dates, manage suppliers and purchases, record sales, maintain transaction history, and generate reports.

---

## About

MediTracker provides a centralized system for managing day-to-day medicine inventory operations.

The application allows authorized users to:

- Manage medicine inventory
- Monitor available stock
- Identify low-stock medicines
- Track expired and soon-to-expire medicines
- Manage suppliers
- Record medicine purchases
- Record medicine sales
- Maintain transaction history
- Import and export medicine data
- Generate CSV, Excel, and PDF reports
- Manage users and authentication
- Provide dashboard statistics and charts
- Access application functionality through APIs

The system uses **SQLite** for persistent data storage and Flask-SQLAlchemy for database interaction.

---

## Features

### 1. User Authentication

MediTracker provides a secure authentication system.

Features include:

- User registration
- User login
- User logout
- Password hashing
- Session management
- Role-based access control
- Admin-only functionality
- Protected routes

Supported roles include:

- Admin
- Staff
- User

---

### 2. Medicine Inventory Management

Users can manage medicine inventory from the Medicine Inventory page.

Features include:

- Add medicines
- View medicines
- Update medicine details
- Delete medicines
- Search medicines
- Filter by category
- Track batch numbers
- Track quantity
- Track medicine price
- Track expiry dates
- Pagination
- Stock status monitoring

Each medicine can contain information such as:

- Medicine name
- Category
- Batch number
- Quantity
- Price
- Expiry date
- Low-stock threshold

---

### 3. Low Stock Monitoring

The system automatically identifies medicines whose quantity falls below the configured stock threshold.

For example:

```text
Low Stock Limit = 10
````

If a medicine has:

```text
Quantity = 5
```

the system can display it as:

```text
Low Stock
```

This helps prevent medicine shortages.

---

### 4. Expiry Tracking

MediTracker monitors medicine expiry dates.

The system identifies:

* Expired medicines
* Medicines approaching expiry
* Valid medicines

The default expiry alert period is:

```text
30 days
```

This allows users to take action before medicines expire.

---

### 5. Dashboard

The dashboard provides a summary of the inventory.

It displays information such as:

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

The dashboard uses charts and tables to make inventory information easier to understand.

---

### 6. Supplier Management

The system provides supplier management functionality.

Users can manage supplier information such as:

* Supplier name
* Company name
* GST number
* Supplier type
* Website
* City
* State
* Postal code
* Country
* Active/inactive status
* Notes

This allows medicine suppliers to be maintained separately from inventory records.

---

### 7. Purchase Management

MediTracker supports medicine purchasing.

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

Purchase information can also be used to update medicine stock.

---

### 8. Sales Management

The application supports medicine sales.

Users can record:

* Medicine sold
* Customer name
* Quantity
* Sale price
* Total amount

When a medicine is sold, the corresponding inventory quantity is reduced.

For example:

```text
Initial stock = 100
Sold quantity = 10
Remaining stock = 90
```

The sale is also stored as a transaction record.

---

### 9. Transaction Management

MediTracker maintains transaction history for inventory-related activities.

Transaction types include:

```text
Purchase
Sale
Return
Expired
```

This provides a history of inventory movement.

---

### 10. Import and Export

The system supports importing and exporting data.

Supported formats include:

* CSV
* Excel
* PDF

Users can import medicine information from CSV files and export reports for further analysis or record keeping.

---

### 11. Report Generation

MediTracker can generate reports in different formats.

Supported formats:

```text
CSV
Excel (.xlsx)
PDF
```

Reports can be generated for different types of application data, such as inventory and transactions.

---

### 12. Email Alerts

The application contains configuration for email notifications.

Email alerts can be used for:

* Medicine expiry alerts
* Low-stock alerts

Configured email subjects include:

```text
Medicine Expiry Alert
Low Stock Alert
MediTracker Test Email
```

Email configuration is managed through environment variables.

---

### 13. REST API

The project also includes an API layer.

The API uses the following prefix:

```text
/api/v1
```

The API provides a structured way for external applications or frontend components to communicate with the MediTracker backend.

---

### 14. Validation

The project contains backend validation utilities.

Validation includes:

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

### 15. Utility Functions

The project includes reusable helper functions for:

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

## Technology Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-WTF
* Werkzeug

### Database

* SQLite
* SQLAlchemy ORM

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap
* Font Awesome

### Data Processing & Reports

* Pandas
* OpenPyXL
* ReportLab
* Matplotlib

### Authentication & Security

* Flask-Login
* Werkzeug password hashing
* Session-based authentication
* Role-based authorization

### Configuration

* python-dotenv
* Environment variables

### Testing

* Pytest

---

## Project Architecture

The project follows a modular Flask architecture using **Application Factory** and **Blueprints**.

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
└── tests/
    ├── test_auth.py
    ├── test_import.py
    ├── test_medicine.py
    └── test_sales.py
```

---

## Application Workflow

The main application workflow is:

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
 ├───────────────┐
 ▼               ▼
Medicine       Supplier
Management     Management
 │               │
 ▼               ▼
Inventory       Purchases
 │               │
 └───────┬───────┘
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
 ┌───────┼────────┐
 ▼       ▼        ▼
 CSV    Excel     PDF
```

---

## Database

MediTracker uses SQLite as its default database.

The database file is stored inside the application's `instance` directory:

```text
instance/medicine_tracker.db
```

SQLAlchemy is used to communicate with the database.

The application uses models to represent different entities such as:

```text
User
Medicine
Supplier
Purchase
Sale
Transaction
```

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd MediTracker
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirement.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key

DATABASE_URL=sqlite:///instance/medicine_tracker.db

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

Do not commit sensitive credentials to GitHub.

---

## Running the Application

Start the Flask application:

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000/
```

---

## Running Tests

Install Pytest if necessary:

```bash
pip install pytest
```

Run all tests:

```bash
pytest -q
```

Run a specific test file:

```bash
pytest tests/test_auth.py
```

or:

```bash
pytest tests/test_medicine.py
```

---

## Testing Coverage

The project includes tests for important application functionality.

### Authentication Tests

Tests include:

* User registration
* Successful login
* Invalid login
* Protected route access
* Logout

### Medicine Tests

Tests include:

* Adding medicine
* Retrieving medicine
* Updating medicine
* Deleting medicine
* Expired medicine detection
* Valid expiry detection

### Sales Tests

Tests include:

* Successful medicine sale
* Stock reduction
* Preventing sales beyond available stock
* Invalid medicine handling
* Sale transaction creation

### Import Tests

Tests verify that important:

* Models
* Database components
* Blueprints
* Application factory

can be imported successfully.

---

## Configuration

Important application settings are centralized in `config.py` and `constant.py`.

Examples include:

```text
Low Stock Limit       = 10
Expiry Alert Days     = 30
Default Currency      = INR
Currency Symbol       = ₹
Items Per Page        = 10
Maximum Upload Size   = 16 MB
```

---

## Security

The application implements several security mechanisms:

* Password hashing
* Login session management
* Role-based authorization
* HTTP-only session cookies
* SameSite cookie protection
* CSRF configuration
* File upload validation
* Environment-based secret configuration
* Protected routes

---

## Future Improvements

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

## Project Objective

The main objective of MediTracker is to provide a simple and centralized system for managing medicine inventory and related pharmacy operations.

Instead of maintaining medicine stock, purchases, sales, expiry information, and transaction records separately, MediTracker combines these operations into one web application.

---

## License

This project was developed as an academic/project application for learning and demonstrating Python Flask, database management, web development, testing, and software architecture.

```

### One important correction

I would **not** keep this old description:

> "MediTracker is a Medicine Expiry Alert Giver."

Your actual project is much better described as:

> **"MediTracker is a web-based Medicine Inventory and Management System that helps manage medicines, stock, suppliers, purchases, sales, transactions, expiry dates, alerts, and reports."**

That description matches the code and the UI you showed much more accurately.
```
