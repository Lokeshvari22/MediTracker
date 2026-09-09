import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # ==================================================
    # Flask Core
    # ==================================================
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")

    # ==================================================
    # Database
    # ==================================================
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "medicine_tracker.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==================================================
    # Upload Directories
    # ==================================================
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    CSV_FOLDER = os.path.join(UPLOAD_FOLDER, "csv")
    REPORT_FOLDER = os.path.join(UPLOAD_FOLDER, "reports")
    INVOICE_FOLDER = os.path.join(UPLOAD_FOLDER, "invoices")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    ALLOWED_EXTENSIONS = {"csv", "xlsx", "pdf"}

    # ==================================================
    # Mail Settings (Flask-Mail)
    # ==================================================
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "t")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() in ("true", "1", "t")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME"))

    # ==================================================
    # Session & Cookie Security
    # ==================================================
    REMEMBER_COOKIE_DURATION = 86400 * 30  # 30 days
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() in ("true", "1", "t")

    # ==================================================
    # Application Thresholds & Limits
    # ==================================================
    MEDICINE_PER_PAGE = 10
    SALES_PER_PAGE = 10
    PURCHASE_PER_PAGE = 10
    TRANSACTION_PER_PAGE = 10

    LOW_STOCK_LIMIT = 10
    EXPIRY_ALERT_DAYS = 30

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # ==================================================
    # Directory Initialization
    # ==================================================
    @staticmethod
    def init_app():
        folders = [
            Config.UPLOAD_FOLDER,
            Config.CSV_FOLDER,
            Config.REPORT_FOLDER,
            Config.INVOICE_FOLDER,
            os.path.join(Config.BASE_DIR, "instance")
        ]

        for folder in folders:
            os.makedirs(folder, exist_ok=True)