import smtplib
from email.message import EmailMessage
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, ADMIN_EMAIL

def send_contact_email(name: str, email: str, message: str):
    msg = EmailMessage()
    msg["Subject"] = "New Contact Form Submission"
    msg["From"] = SMTP_USER
    msg["To"] = ADMIN_EMAIL

    msg.set_content(
        f"""
New contact request from FitVisionAI

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
