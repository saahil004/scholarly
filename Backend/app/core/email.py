import os
from typing import Dict
import resend

resend.api_key = os.getenv("RESEND_API_KEY")
MAIL_FROM = os.getenv("MAIL_FROM")

def send_otp_email(email: str, otp: str) -> Dict:
    params: resend.Emails.SendParams = {
        "from": MAIL_FROM,
        "to": [email],
        "subject": "Scholarly Academy - Verify Your Email",
        "html": f"<h2>Your OTP is: <strong>{otp}</strong></h2><p>Expires in 10 minutes.</p>"
    }
    response: resend.Emails.SendResponse = resend.Emails.send(params)
    return response