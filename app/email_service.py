import smtplib
from email.message import EmailMessage
from app.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    ADMIN_EMAIL,
)

def send_contact_email(name: str, email: str, message: str):
    msg = EmailMessage()
    msg["Subject"] = "New Contact Form Submission"
    msg["From"] = SMTP_USER
    msg["To"] = ADMIN_EMAIL

    msg.set_content(
        f"""
New contact message

Name: {name}
Email: {email}

Message:
{message}
"""
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

def send_reset_password_email(email: str, token: str):
    reset_link = f"http://localhost:5173/reset-password/{token}"

    msg = EmailMessage()
    msg["Subject"] = "Reset your FitVisionAI password"
    msg["From"] = SMTP_USER
    msg["To"] = email

    msg.set_content(
        f"""
You requested a password reset for FitVisionAI.

Click the link below to reset your password.
This link will expire in 30 minutes.

{reset_link}

If you did not request this, please ignore this email.
"""
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
