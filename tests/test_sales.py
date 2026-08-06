import pytest
from app import create_app
from database.database import db
from models.user import User
from models.medicine import Medicine
from models.sale import Sale


@pytest.fixture
def app_instance():
    """Create and configure a clean testing application instance."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app_instance):
    """Return a test client instance."""
    return app_instance.test_client()


@pytest.fixture
def authenticated_client(client, app_instance):
    """Provide a test client logged in with an active session."""
    with app_instance.app_context():
        user = User(username="sales_user", email="sales@test.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Log in using the auth route
    client.post(
        "/login",
        data={"email": "sales@test.com", "password": "password123"},
        follow_redirects=True
    )
    return client, user_id


def create_test_medicine(user_id, initial_quantity=100):
    """Helper utility to seed a medicine record."""
    medicine = Medicine(
        name="Paracetamol 500mg",
        category="Painkiller",
        quantity=initial_quantity,
        price=10.00,
        low_stock_alert=10,
        user_id=user_id
    )
    db.session.add(medicine)
    db.session.commit()
    return medicine


def test_successful_sale(authenticated_client, app_instance):
    """Test medicine sale decreases stock quantity."""
    client, user_id = authenticated_client
    with app_instance.app_context():
        medicine = create_test_medicine(user_id, initial_quantity=100)
        med_id = medicine.id

        response = client.post(
            "/sales/sell",
            data={
                "medicine_id": med_id,
                "customer_name": "John Doe",
                "quantity": 10,
                "sale_price": 10.00,
                "total_amount": 100.00
            },
            follow_redirects=True
        )

        assert response.status_code == 200

        updated_medicine = db.session.get(Medicine, med_id)
        assert updated_medicine.quantity == 90


def test_sale_more_than_available_stock(authenticated_client, app_instance):
    """Test selling quantity greater than available inventory."""
    client, user_id = authenticated_client
    with app_instance.app_context():
        medicine = create_test_medicine(user_id, initial_quantity=100)
        med_id = medicine.id

        response = client.post(
            "/sales/sell",
            data={
                "medicine_id": med_id,
                "customer_name": "John Doe",
                "quantity": 200,
                "sale_price": 10.00,
                "total_amount": 2000.00
            },
            follow_redirects=True
        )

        # Check for error validation response or un-updated stock
        updated_medicine = db.session.get(Medicine, med_id)
        assert updated_medicine.quantity == 100


def test_sale_invalid_medicine(authenticated_client, app_instance):
    """Test sale request with non-existent medicine ID."""
    client, user_id = authenticated_client
    with app_instance.app_context():
        response = client.post(
            "/sales/sell",
            data={
                "medicine_id": 9999,
                "customer_name": "Test Customer",
                "quantity": 5,
                "sale_price": 10.00
            },
            follow_redirects=True
        )

        assert response.status_code in [200, 400, 404]


def test_sale_record_created(authenticated_client, app_instance):
    """Test sale transaction history record creation."""
    client, user_id = authenticated_client
    with app_instance.app_context():
        medicine = create_test_medicine(user_id, initial_quantity=100)
        med_id = medicine.id

        client.post(
            "/sales/sell",
            data={
                "medicine_id": med_id,
                "customer_name": "Jane Smith",
                "quantity": 20,
                "sale_price": 10.00,
                "total_amount": 200.00
            },
            follow_redirects=True
        )

        sale = Sale.query.filter_by(medicine_id=med_id).first()
        assert sale is not None
        assert sale.quantity == 20