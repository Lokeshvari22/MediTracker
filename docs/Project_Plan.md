# Medicine Inventory & Expiry System
## Project Plan

---

## 1. Project Overview

The MediTrack project is a Flask-based web application to help pharmacies and clinics manage medicine inventory, track expiry dates, record purchases and sales, and generate exportable reports (CSV/Excel/PDF).

The system aims to reduce waste, improve inventory visibility, and provide simple reporting for day-to-day operations.

---

## 2. Problem Statement

Manual inventory management leads to missed expiries, financial loss, and inefficient operations. MediTrack centralizes records, adds alerts, and provides reporting to address these issues.

---

## 3. Project Objectives

Key objectives:

- Reliable medicine CRUD and batch tracking
- Accurate expiry monitoring and alerts
- Exportable reports (CSV/Excel/PDF) that respect filters
- Simple role-based access and authentication
- Basic analytics for stock and sales

---

## 4. Target Users

Designed for:

- Small pharmacies and medical stores
- Clinic inventory managers
- Pharmacy admins who need exportable records

---

## 5. Technology Stack

| Component | Technology |
| --------- | ---------- |
| Backend | Python + Flask (Blueprints) |
| ORM | Flask-SQLAlchemy (SQLite by default) |
| Auth | Flask-Login |
| Exports | CSV (builtin), openpyxl (Excel), reportlab (PDF) |
| Frontend | Jinja2 templates, Bootstrap, client-side JS |

---

## 6. System Modules

## 6.1 Authentication Module

Responsibilities:

- User login
- User logout
- Password hashing
- Session management
- Role-based access control


---

## 6.2 Medicine Management Module

Responsibilities:

- Add medicine
- Update medicine
- Delete medicine
- Search medicine
- Filter medicine
- Pagination support

---

## 6.3 Batch Management Module

Responsibilities:

- Maintain batch numbers
- Track quantity
- Store expiry dates
- Store purchase dates
- Maintain batch history

---

## 6.4 Supplier Management Module

Responsibilities:

- Add suppliers
- Update supplier details
- Delete suppliers
- Maintain supplier history

---

## 6.5 Dashboard Module

Responsibilities:

- Display inventory statistics
- Show medicine count
- Show expiry information
- Display recent activities

---

## 6.6 Reporting Module

Responsibilities:

- Generate inventory reports
- Generate expiry reports
- Generate supplier reports
- Export PDF reports
- Export Excel reports

---

## 6.7 Automation Module

Responsibilities:

- Scheduled expiry checking
- Automatic reminder generation
- Email notifications

---

## 6.8 Analytics Module

Responsibilities:

- Inventory analysis
- Expiry trend analysis
- Stock monitoring
- Visual charts

---

# 7. Development Roadmap

## Phase 1 — Project Setup

Goals:

- Setup Flask project
- Configure database (SQLite by default; can be switched to MySQL/Postgres in production)
- Create GitHub repository
- Setup virtual environment
- Create project structure

Deliverable:

✅ Running Flask application

---

## Phase 2 — Authentication

Goals:

- Implement login system
- Implement logout
- Add password hashing
- Add session management
- Implement user roles

Deliverable:

✅ Secure authentication system

---

## Phase 3 — Medicine Management

Goals:

- Create medicine CRUD operations
- Add searching
- Add filtering
- Add pagination

Deliverable:

✅ Complete medicine management module

---

## Phase 4 — Batch Management

Goals:

- Store batch information
- Track quantity
- Track expiry dates
- Maintain purchase details

Deliverable:

✅ Batch-wise inventory management

---

## Phase 5 — Supplier Management

Goals:

- Create supplier module
- Manage supplier records
- Maintain supplier history

Deliverable:

✅ Supplier management module

---

## Phase 6 — Dashboard

Goals:

- Create dashboard interface
- Add statistics cards
- Display recent activities

Deliverable:

✅ Inventory dashboard

---

## Phase 7 — Reports

Goals:

- Generate inventory reports
- Generate expiry reports
- Generate supplier reports
- Add PDF and Excel export

Deliverable:

✅ Reporting system

---

## Phase 8 — Automation

Goals:

- Setup scheduler
- Create expiry checker
- Configure email reminders

Deliverable:

✅ Automated expiry notification system

---

## Phase 9 — Analytics

Goals:

- Add charts
- Analyze inventory data
- Provide business insights

Deliverable:

✅ Analytics dashboard

---

# 8. Project Structure

Below is a concise overview of the main project folders and their purpose:

- `app.py` — application entry point
- `config.py` — runtime configuration
- `routes/` — Flask blueprints for auth, medicines, purchases, sales, reports, suppliers, transactions
- `services/` — business logic and helpers (exports, analytics, inventory)
- `models/` — SQLAlchemy models
- `templates/` — Jinja2 HTML templates
- `Static/` — CSS, JS, images and upload folders (`uploads/reports/`)
- `database/` — database connection and seed scripts
- `tests/` — pytest test files
- `docs/` — user and developer documentation
- `mail/` — optional email sender helper and templates

