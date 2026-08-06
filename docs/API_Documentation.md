# MediTrack - API Documentation

## 1. Overview

This repository implements a small inventory and expiry-tracking web application built with Flask. The application exposes HTTP endpoints (mostly standard REST-style routes) for managing medicines, inventory, suppliers, purchases, sales, and reports.

Stack (project-specific):

- Backend: Python + Flask (Blueprints)
- Database: SQLite (via Flask-SQLAlchemy) — configured per environment (instance folder)
- Authentication: session-based (Flask-Login)
- Exports: CSV (builtin), Excel (`openpyxl`), PDF (`reportlab`)

Base URL (development):

```
http://localhost:5000/
```

Notes:
- Most endpoints are implemented as Flask blueprints under the `routes/` folder.
- There is an optional email helper at `mail/email_sender.py` used for sending alerts when SMTP is configured.

---

## 2. Authentication

The application uses session-based authentication via `Flask-Login`. The most common endpoints (implemented in `routes/auth.py`) are:

- `GET /login` — show login page (HTML)
- `POST /login` — authenticate user using `email` and `password` form fields (returns redirect on success)
- `GET /signup` — show registration page (HTML)
- `POST /signup` — register new user
- `GET /logout` — log out current user

For API-style integrations you can reuse these endpoints with form-encoded bodies or implement a token layer as needed.

Example login (form POST):

```
POST /login
Content-Type: application/x-www-form-urlencoded

email=john%40example.com&password=password123
```

Successful responses are typically redirects to the dashboard; API consumers should expect 200/302 on success and 401 on failure.

---

# 3. Medicine Endpoints

Routes for medicine CRUD are implemented in `routes/medicine.py` and the UI templates under `templates/medicines/`.

Common endpoints (HTML + form-backed):

- `GET /medicines` — list medicines (HTML)
- `GET /medicines/add` — form to add a medicine
- `POST /medicines/add` — create medicine (form fields: `name`, `category`, `batch_number`, `quantity`, `expiry_date`, `price`, etc.)
- `GET /medicines/<int:id>/edit` — edit form
- `POST /medicines/<int:id>/edit` — update medicine
- `POST /medicines/<int:id>/delete` — delete medicine

The routes also return JSON in some views when requested by AJAX; check the templates and JS in `Static/js/medicine.js` for client-side usage.

---

# 4. Inventory & Stock

Inventory-related views are available under `routes/dashboard.py` and `services/inventory_service.py`.

- `GET /dashboard` — dashboard summary (HTML) — shows total medicines, low-stock count, expired items, etc.
- `GET /reports/inventory` — inventory report (HTML)
- Low-stock and alerts are visible on the dashboard and handled in the backend via `services/inventory_service.py`.

Programmatic consumers can use the HTML endpoints + AJAX or extend the code to return JSON responses.

---

# 5. Expiry Tracking

Expiry reporting is implemented in `routes/medicine.py` (expired view) and `services/expiry_service.py`.

- `GET /medicines/expired` — show expired medicines (HTML)
- `GET /medicines/expiring` — medicines expiring soon (HTML)

The UI templates render `N/A` or friendly fallbacks for missing expiry dates; backend services return filtered lists used by CSV/Excel/PDF exporters.

---

# 6. Suppliers

Suppliers are managed in `routes/supplier.py` with UI templates under `templates/suppliers/`.

- `GET /suppliers` — list suppliers
- `GET /suppliers/add` — add supplier form
- `POST /suppliers/add` — create supplier
- `GET /suppliers/<int:id>/edit` — edit form
- `POST /suppliers/<int:id>/edit` — update supplier

---

# 7. Dashboard

`GET /dashboard` renders the application dashboard showing summary metrics and alert cards. Data is computed in `analytics/dashboard_metrics.py` and displayed via `templates/dashboard.html`.

---

# 8. Search

Search features are available in the UI and via simple query parameters on listing endpoints. Example:

```
GET /medicines?name=Paracetamol
```

This returns an HTML page filtered by the `name` parameter, and some endpoints support AJAX JSON responses.

---

# 9. Error Responses

Common HTTP statuses used by the app:

- `200 OK` — successful GET/POST when returning content
- `302 Found` — redirect after successful form POST (login, create, update)
- `201 Created` — resource created (API-style)
- `400 Bad Request` — validation errors
- `401 Unauthorized` — authentication required
- `403 Forbidden` — permission denied
- `404 Not Found` — resource missing
- `500 Internal Server Error` — unexpected server error

Errors are usually displayed as flash messages in the UI; API/JS callers receive JSON when endpoints are used via AJAX.

---

# 10. Exports & Reports

Export endpoints are implemented in `routes/report.py` and the export logic lives in `services/csv_service.py`, `services/pdf_service.py`, and `services/report_service.py`.

Common export usage (browser buttons call these URLs and preserve filters):

```
GET /export?format=csv&report_type=sales&from_date=2026-01-01&to_date=2026-06-30
```

Parameters:
- `format`: `csv`, `excel`, or `pdf`
- `report_type`: `sales`, `purchase`, `inventory`, `low_stock`, `expiry`, etc.
- `from_date`, `to_date`: optional `YYYY-MM-DD` filter range

Behavior:
- Exports use the same filtered dataset as the report UI (they respect `report_type` and date filters).
- Generated files are saved under `Static/uploads/reports/` (accessible via download links on the reports page).
- Export actions are recorded in the `ExportHistory` model so users can re-download past exports from the UI.

---

# 11. Email helper and Notifications

The `mail/` folder contains `email_sender.py`, a small helper that wraps `Flask-Mail` template rendering to send expiry and low-stock alerts when SMTP is configured. The app does not require SMTP to run — email sending is optional and controlled via configuration (`MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`, etc.).

---

# End of API Documentation