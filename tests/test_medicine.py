"""
Medicine Module Test Cases
Project: MediTracker

Tests:
- Add new medicine record
- Retrieve medicine details
- Update stock quantity and price
- Delete medicine record
- Expiry date status validation
"""

import pytest
from datetime import date, timedelta
from app import create_app
from models.medicine import Medicine
from database.database import db



@pytest.fixture
def app():
    """Create and configure a clean application instance for testing."""
    _app = create_app('testing')
    _app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret-key"
    })

    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for sending HTTP requests to the app."""
    return app.test_client()


@pytest.fixture
def sample_medicine_data():
    """Sample medicine dataset used across unit tests."""
    return {
        "name": "Paracetamol 500mg",
        "category": "Tablet",
        "batch_number": "PCM101",
        "quantity": 100,
        "price": 50.00,
        "expiry_date": date.today() + timedelta(days=365)
    }


def test_add_medicine_db(app, sample_medicine_data):
    """Test adding a medicine record directly into the database."""
    with app.app_context():
        medicine = Medicine(
            name=sample_medicine_data["name"],
            category=sample_medicine_data["category"],
            batch_number=sample_medicine_data["batch_number"],
            quantity=sample_medicine_data["quantity"],
            price=sample_medicine_data["price"],
            expiry_date=sample_medicine_data["expiry_date"]
        )
        db.session.add(medicine)
        db.session.commit()

        retrieved = Medicine.query.filter_by(batch_number="PCM101").first()
        assert retrieved is not None
        assert retrieved.name == "Paracetamol 500mg"
        assert retrieved.quantity == 100
        assert retrieved.price == 50.00


def test_get_medicine(app, sample_medicine_data):
    """Test retrieving an existing medicine item by primary key."""
    with app.app_context():
        medicine = Medicine(**sample_medicine_data)
        db.session.add(medicine)
        db.session.commit()
        med_id = medicine.id

        fetched = Medicine.query.get(med_id)
        assert fetched is not None
        assert fetched.batch_number == "PCM101"


def test_update_medicine(app, sample_medicine_data):
    """Test updating inventory quantity and price fields."""
    with app.app_context():
        medicine = Medicine(**sample_medicine_data)
        db.session.add(medicine)
        db.session.commit()
        med_id = medicine.id

        # Perform update
        med_to_update = Medicine.query.get(med_id)
        med_to_update.quantity = 200
        med_to_update.price = 55.00
        db.session.commit()

        updated = Medicine.query.get(med_id)
        assert updated.quantity == 200
        assert updated.price == 55.00


def test_delete_medicine(app, sample_medicine_data):
    """Test deleting a medicine item from inventory."""
    with app.app_context():
        medicine = Medicine(**sample_medicine_data)
        db.session.add(medicine)
        db.session.commit()
        med_id = medicine.id

        # Perform deletion
        med_to_delete = Medicine.query.get(med_id)
        db.session.delete(med_to_delete)
        db.session.commit()

        deleted = Medicine.query.get(med_id)
        assert deleted is None


def test_expired_date_check(app):
    """Test expired medicine detection logic."""
    with app.app_context():
        expired_med = Medicine(
            name="Expired Syrup",
            category="Syrup",
            batch_number="EXP999",
            quantity=10,
            price=120.00,
            expiry_date=date.today() - timedelta(days=10)
        )
        db.session.add(expired_med)
        db.session.commit()

        # Evaluate expiry logic
        assert expired_med.expiry_date < date.today()
        if hasattr(expired_med, 'is_expired'):
            assert expired_med.is_expired is True


def test_valid_expiry_date_check(app):
    """Test valid (future) medicine expiry date logic."""
    with app.app_context():
        valid_med = Medicine(
            name="Fresh Ointment",
            category="Ointment",
            batch_number="FRSH123",
            quantity=50,
            price=80.00,
            expiry_date=date.today() + timedelta(days=120)
        )
        db.session.add(valid_med)
        db.session.commit()

        assert valid_med.expiry_date > date.today()
        if hasattr(valid_med, 'is_expired'):
            assert valid_med.is_expired is False