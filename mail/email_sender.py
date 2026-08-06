"""
Email Sender Module
-------------------
Handles sending email notifications for:
1. Medicine expiry alerts
2. Low stock alerts

Uses Flask-Mail with Jinja HTML templates.
"""

import logging
from flask import render_template, current_app
from flask_mail import Mail, Message

# Initialize Flask-Mail extension instance
mail = Mail()

logger = logging.getLogger(__name__)


def send_email(receiver_email, subject, html_content):
    """
    Generic email sender function using Flask-Mail.
    """
    try:
        sender = current_app.config.get("MAIL_DEFAULT_SENDER") or current_app.config.get("MAIL_USERNAME")
        
        if not sender:
            logger.warning("Email sending skipped: MAIL_USERNAME or MAIL_DEFAULT_SENDER not configured.")
            return False

        msg = Message(
            subject=subject,
            recipients=[receiver_email],
            html=html_content,
            sender=sender
        )

        mail.send(msg)
        return True

    except Exception as error:
        logger.error(f"Email sending failed to {receiver_email}: {error}")
        return False


def send_expiry_alert(receiver_email, user, medicines):
    """
    Send medicine expiry notification email.
    """
    try:
        html = render_template(
            "expiry_alert.html",
            user=user,
            medicines=medicines
        )
    except Exception:
        # Fallback formatting if template is rendered without context
        html = f"""
        <h3>Medicine Expiry Alert</h3>
        <p>Hello,</p>
        <p>The following medicine is expiring soon or has expired:</p>
        <ul>
            <li><strong>Medicine:</strong> {medicines}</li>
        </ul>
        """

    return send_email(
        receiver_email,
        "MediTracker - Medicine Expiry Alert",
        html
    )


def send_low_stock_alert(receiver_email, user, medicines):
    """
    Send low stock notification email.
    """
    try:
        html = render_template(
            "low_stock_alert.html",
            user=user,
            medicines=medicines
        )
    except Exception:
        # Fallback formatting
        html = f"""
        <h3>Low Stock Alert</h3>
        <p>Hello,</p>
        <p>The following medicine inventory has fallen below the minimum stock threshold:</p>
        <ul>
            <li><strong>Medicine:</strong> {medicines}</li>
        </ul>
        """

    return send_email(
        receiver_email,
        "MediTracker - Low Stock Alert",
        html
    )