# ==========================================================
# Application
# ==========================================================

APP_NAME = "MediTracker"

APP_VERSION = "1.0.0"

DEFAULT_TIMEZONE = "Asia/Kolkata"

DEFAULT_CURRENCY = "INR"

CURRENCY_SYMBOL = "₹"


# ==========================================================
# Pagination
# ==========================================================

DEFAULT_PAGE = 1

DEFAULT_PER_PAGE = 10

MAX_PER_PAGE = 100


# ==========================================================
# Stock
# ==========================================================

DEFAULT_LOW_STOCK_ALERT = 10

EXPIRY_ALERT_DAYS = 30

MAX_QUANTITY = 100000


# ==========================================================
# Medicine Categories
# ==========================================================

MEDICINE_CATEGORIES = [

    "Tablet",

    "Capsule",

    "Syrup",

    "Injection",

    "Cream",

    "Ointment",

    "Drops",

    "Powder",

    "Gel",

    "Spray",

    "Inhaler",

    "Others"

]


# ==========================================================
# Transaction Types
# ==========================================================

PURCHASE = "Purchase"

SALE = "Sale"

RETURN = "Return"

EXPIRED = "Expired"

TRANSACTION_TYPES = [

    PURCHASE,

    SALE,

    RETURN,

    EXPIRED

]


# ==========================================================
# User Roles
# ==========================================================

ADMIN = "Admin"

STAFF = "Staff"

USER = "User"

ROLES = [

    ADMIN,

    STAFF,

    USER

]


# ==========================================================
# Report Formats
# ==========================================================

CSV = "csv"

EXCEL = "xlsx"

PDF = "pdf"

REPORT_FORMATS = [

    CSV,

    EXCEL,

    PDF

]


# ==========================================================
# Upload Settings
# ==========================================================

UPLOAD_FOLDER = "static/uploads"

CSV_UPLOAD_FOLDER = "static/uploads/csv"

REPORT_FOLDER = "static/uploads/reports"

INVOICE_FOLDER = "static/uploads/invoices"

ALLOWED_EXTENSIONS = {

    "csv",

    "xlsx",

    "pdf"

}


# ==========================================================
# Email
# ==========================================================

EXPIRY_EMAIL_SUBJECT = "Medicine Expiry Alert"

LOW_STOCK_EMAIL_SUBJECT = "Low Stock Alert"

TEST_EMAIL_SUBJECT = "MediTracker Test Email"


# ==========================================================
# Flash Message Categories
# ==========================================================

SUCCESS = "success"

DANGER = "danger"

WARNING = "warning"

INFO = "info"


# ==========================================================
# Database
# ==========================================================

DATABASE_NAME = "medicine_tracker.db"


# ==========================================================
# Session
# ==========================================================

REMEMBER_COOKIE_DAYS = 30


# ==========================================================
# Dashboard
# ==========================================================

RECENT_SALES_LIMIT = 10

TOP_SELLING_LIMIT = 10

CHART_MONTHS = 12


# ==========================================================
# File Names
# ==========================================================

MEDICINE_CSV = "medicines.csv"

MEDICINE_EXCEL = "medicines.xlsx"

MEDICINE_PDF = "medicines.pdf"

TRANSACTION_CSV = "transactions.csv"

TRANSACTION_EXCEL = "transactions.xlsx"

TRANSACTION_PDF = "transactions.pdf"


# ==========================================================
# Date Formats
# ==========================================================

DATE_FORMAT = "%d-%m-%Y"

DATETIME_FORMAT = "%d-%m-%Y %I:%M %p"

DATABASE_DATE = "%Y-%m-%d"


# ==========================================================
# API
# ==========================================================

API_PREFIX = "/api/v1"

API_SUCCESS = "success"

API_ERROR = "error"