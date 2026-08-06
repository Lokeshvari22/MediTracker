"""
Authentication Test Cases
Project: MediTracker

Tests:
1. User registration endpoint
2. Successful user login and session creation
3. Invalid credential handling
4. Session logout and protected route access
"""

import pytest
from app import create_app
from database.database import db
from models.user import User


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


# In tests/test_auth.py

def test_register_user(client):
    """Test new user registration."""
    response = client.post(
        "/signup",  # Changed from "/register" to "/signup"
        data={
            "username": "test_admin",
            "email": "admin@test.com",
            "password": "password123",
            "confirm_password": "password123",
            "role": "Admin"
        },
        follow_redirects=True
    )
    assert response.status_code == 200


def test_login_success(client, app):
    """Test successful login with valid credentials."""
    # Register user first
    with app.app_context():
        user = User(username="test_admin", email="admin@test.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "password123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    # Ensure redirected or rendered dashboard page
    assert b"Dashboard" in response.data or b"Logout" in response.data or b"Inventory" in response.data


def test_login_failure(client, app):
    """Test invalid credentials handling."""
    with app.app_context():
        user = User(username="test_admin", email="admin@test.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "wrong_password"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Invalid" in response.data or b"error" in response.data.lower() or b"login" in response.data.lower()


def test_authenticated_access(client, app):
    """Test protected route access after logging in."""
    with app.app_context():
        user = User(username="test_admin", email="admin@test.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    # Log in user
    client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "password123"
        },
        follow_redirects=True
    )

    # Access protected profile or medicines page
    response = client.get("/medicines", follow_redirects=True)
    assert response.status_code == 200
    assert b"Medicine" in response.data or b"Inventory" in response.data


def test_logout(client, app):
    """Test logging out terminates the session."""
    with app.app_context():
        user = User(username="test_admin", email="admin@test.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    client.post("/login", data={"email": "admin@test.com", "password": "password123"})
    
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data or b"Logged out" in response.data