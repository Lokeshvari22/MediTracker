import re
from datetime import datetime


class Validator:
    """
    MediTracker Utility Validators
    Provides backend validation helpers for email, phone, passwords, dates, and uploaded files.
    """

    EMAIL_REGEX = re.compile(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )

    PHONE_REGEX = re.compile(
        r"^\+?[0-9]{7,15}$"
    )

    ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "pdf"}

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validates if the provided email string matches standard email formats.
        """
        if not email or not isinstance(email, str):
            return False
        return bool(Validator.EMAIL_REGEX.match(email.strip()))

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        Validates international and local phone number strings.
        """
        if not phone:
            return True  # Phone is optional in most forms
        clean_phone = phone.strip().replace(" ", "").replace("-", "")
        return bool(Validator.PHONE_REGEX.match(clean_phone))

    @staticmethod
    def is_strong_password(password: str) -> tuple[bool, str]:
        """
        Validates password strength criteria:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        """
        if not password or len(password) < 8:
            return False, "Password must be at least 8 characters long."

        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."

        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."

        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one digit."

        return True, "Password is strong."

    @staticmethod
    def is_valid_date(date_str: str, date_format: str = "%Y-%m-%d") -> bool:
        """
        Checks if a string matches a given date format (default: YYYY-MM-DD).
        """
        if not date_str or not isinstance(date_str, str):
            return False
        try:
            datetime.strptime(date_str.strip(), date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def allowed_file(filename: str, allowed_extensions: set = None) -> bool:
        """
        Checks if an uploaded file has a valid allowed extension.
        """
        if not filename or "." not in filename:
            return False

        ext = filename.rsplit(".", 1)[1].lower()
        targets = allowed_extensions if allowed_extensions else Validator.ALLOWED_EXTENSIONS
        return ext in targets

    @staticmethod
    def validate_positive_number(value) -> bool:
        """
        Ensures quantities or prices are non-negative numeric values.
        """
        try:
            num = float(value)
            return num >= 0
        except (ValueError, TypeError):
            return False