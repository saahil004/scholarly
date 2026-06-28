import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_USER = os.getenv("BREVO_SMTP_USER")
SMTP_PASSWORD = os.getenv("BREVO_SMTP_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

def send_otp_email(email: str, otp: str):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Scholarly Academy - Verify Your Email"
    message["From"] = MAIL_FROM
    message["To"] = email

    html = f"""
        <h2>Welcome to Scholarly Academy</h2>
        <p>Your verification code is:</p>
        <h1 style="letter-spacing: 4px;">{otp}</h1>
        <p>This code expires in 10 minutes.</p>
        <p>If you didn't register, ignore this email.</p>
    """
    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(MAIL_FROM, email, message.as_string())