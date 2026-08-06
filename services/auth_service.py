from database.database import db
from models.user import User


class AuthService:
    """
    Handles all authentication-related business logic.
    """

    @staticmethod
    def register_user(username, email, password):
        """
        Register a new user after validation.
        Returns:
            (True, message)  -> Success
            (False, message) -> Failure
        """

        username = username.strip()
        email = email.strip().lower()

        if not username:
            return False, "Username cannot be empty."

        if not email:
            return False, "Email cannot be empty."

        if len(password) < 6:
            return False, "Password must contain at least 6 characters."

        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            return False, "Email already registered."

        existing_username = User.query.filter_by(username=username).first()

        if existing_username:
            return False, "Username already exists."

        user = User(
            username=username,
            email=email
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return True, "Registration Successful."

    @staticmethod
    def authenticate_user(email, password):
        """
        Verify login credentials.
        Returns:
            User object -> Success
            None -> Invalid credentials
        """

        email = email.strip().lower()

        user = User.query.filter_by(email=email).first()

        if not user:
            return None

        if not user.check_password(password):
            return None

        return user

    @staticmethod
    def get_user_by_id(user_id):
        """
        Returns user by ID.
        """

        return User.query.get(user_id)

    @staticmethod
    def email_exists(email):
        """
        Check if email already exists.
        """

        return User.query.filter_by(
            email=email.strip().lower()
        ).first() is not None

    @staticmethod
    def username_exists(username):
        """
        Check if username already exists.
        """

        return User.query.filter_by(
            username=username.strip()
        ).first() is not None