from flask import Flask
from flask_login import LoginManager
from sqlalchemy import text

from config import Config
from database.database import db
from mail.email_sender import mail
from models.user import User

# Import all Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.medicine import medicine_bp
from routes.supplier import supplier_bp
from routes.purchase import purchase_bp
from routes.sales import sales_bp
from routes.transaction import transaction_bp
from routes.report import report_bp
from routes.import_export import import_export_bp
from routes.api import api_bp


login_manager = LoginManager()


def ensure_supplier_columns():
    with db.engine.begin() as conn:
        result = conn.execute(text("PRAGMA table_info(suppliers)"))
        columns = {row[1] for row in result.fetchall()}

        alter_stmts = []

        if "company_name" not in columns:
            alter_stmts.append("ALTER TABLE suppliers ADD COLUMN company_name VARCHAR(150)")
        if "gst_number" not in columns:
            alter_stmts.append("ALTER TABLE suppliers ADD COLUMN gst_number VARCHAR(50)")
        if "supplier_type" not in columns:
            alter_stmts.append("ALTER TABLE suppliers ADD COLUMN supplier_type VARCHAR(50)")
        if "website" not in columns:
            alter_stmts.append("ALTER TABLE suppliers ADD COLUMN website VARCHAR(255)")
        if "city" not in columns:
            alter_stmts.append("ALTER TABLE suppliers ADD COLUMN city VARCHAR(100)")
        if "state" not in columns:
            alter_stmts.append("ALTER TABLE suppliers ADD COLUMN state VARCHAR(100)")
        if "postal_code" not in columns:
            alter_stmts.append("ALTER TABLE suppliers ADD COLUMN postal_code VARCHAR(20)")
        if "country" not in columns:
            alter_stmts.append("ALTER TABLE suppliers ADD COLUMN country VARCHAR(100) DEFAULT 'India'")
        if "is_active" not in columns:
            alter_stmts.append("ALTER TABLE suppliers ADD COLUMN is_active BOOLEAN DEFAULT 1")
        if "notes" not in columns:
            alter_stmts.append("ALTER TABLE suppliers ADD COLUMN notes TEXT")

        for stmt in alter_stmts:
            conn.execute(text(stmt))


def ensure_purchase_columns():
    with db.engine.begin() as conn:
        result = conn.execute(text("PRAGMA table_info(purchases)"))
        columns = {row[1] for row in result.fetchall()}

        alter_stmts = []

        if "discount" not in columns:
            alter_stmts.append("ALTER TABLE purchases ADD COLUMN discount FLOAT DEFAULT 0.0")
        if "gst" not in columns:
            alter_stmts.append("ALTER TABLE purchases ADD COLUMN gst FLOAT DEFAULT 0.0")
        if "total_amount" not in columns:
            alter_stmts.append("ALTER TABLE purchases ADD COLUMN total_amount FLOAT DEFAULT 0.0")
        if "payment_method" not in columns:
            alter_stmts.append("ALTER TABLE purchases ADD COLUMN payment_method VARCHAR(50) DEFAULT 'Cash'")
        if "status" not in columns:
            alter_stmts.append("ALTER TABLE purchases ADD COLUMN status VARCHAR(50) DEFAULT 'Paid'")
        if "notes" not in columns:
            alter_stmts.append("ALTER TABLE purchases ADD COLUMN notes TEXT")

        for stmt in alter_stmts:
            conn.execute(text(stmt))


# In app.py

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable testing mode if requested by pytest
    if config_name == "testing":
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["WTF_CSRF_ENABLED"] = False

    # Auto-create upload directories & instance folder
    Config.init_app()

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register all Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(medicine_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(purchase_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(import_export_bp)
    app.register_blueprint(api_bp)

    # Ensure database tables exist and required columns are present
    with app.app_context():
        db.create_all()
        ensure_supplier_columns()
        ensure_purchase_columns()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)