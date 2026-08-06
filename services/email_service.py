from flask import render_template

from flask_mail import Message

from mail.email_sender import mail

from models.user import User

from services.expiry_service import ExpiryService
from services.inventory_service import InventoryService


class EmailService:

    # ==================================
    # Send Email
    # ==================================

    @staticmethod
    def send_email(

        recipient,

        subject,

        html

    ):

        message = Message(

            subject=subject,

            recipients=[recipient],

            html=html

        )

        mail.send(message)

    # ==================================
    # Expiry Alert
    # ==================================

    @staticmethod
    def send_expiry_alert(

        user_id,

        days=30

    ):

        user = User.query.get(user_id)

        if not user:

            return False

        medicines = ExpiryService.expiring_soon(

            user_id,

            days

        )

        if not medicines:

            return False

        html = render_template(

            "expiry_alert.html",

            user=user,

            medicines=medicines,

            days=days

        )

        EmailService.send_email(

            recipient=user.email,

            subject="Medicine Expiry Alert",

            html=html

        )

        return True

    # ==================================
    # Low Stock Alert
    # ==================================

    @staticmethod
    def send_low_stock_alert(

        user_id

    ):

        user = User.query.get(user_id)

        if not user:

            return False

        medicines = InventoryService.low_stock(

            user_id

        )

        if not medicines:

            return False

        html = render_template(

            "low_stock_alert.html",

            user=user,

            medicines=medicines

        )

        EmailService.send_email(

            recipient=user.email,

            subject="Low Stock Alert",

            html=html

        )

        return True

    # ==================================
    # Send Daily Alerts
    # ==================================

    @staticmethod
    def send_daily_notifications():

        users = User.query.all()

        sent = 0

        for user in users:

            expiry = EmailService.send_expiry_alert(

                user.id

            )

            low_stock = EmailService.send_low_stock_alert(

                user.id

            )

            if expiry or low_stock:

                sent += 1

        return sent

    # ==================================
    # Test Email
    # ==================================

    @staticmethod
    def send_test_email(

        email

    ):

        html = """

        <h2>MediTracker</h2>

        <p>Email configuration is working successfully.</p>

        """

        EmailService.send_email(

            recipient=email,

            subject="MediTracker Test Email",

            html=html

        )

        return True

    # ==================================
    # Custom Email
    # ==================================

    @staticmethod
    def send_custom_email(

        email,

        subject,

        message

    ):

        html = f"""

        <h2>{subject}</h2>

        <p>{message}</p>

        """

        EmailService.send_email(

            recipient=email,

            subject=subject,

            html=html

        )

        return True