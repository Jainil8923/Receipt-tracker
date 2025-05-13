import os
from email.message import EmailMessage
import aiosmtplib
from dotenv import load_dotenv

load_dotenv()

async def send_verification_email(to_email: str, token: str):
    verification_link = f"http://localhost:8000/auth/verify-email?token={token}"
    message = EmailMessage()
    message["From"] = os.getenv("SMTP_USER")
    message["To"] = to_email
    message["Subject"] = "Verify your email"
    message.set_content(f"Click the link to verify your email: {verification_link}")

    await aiosmtplib.send(
        message,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT")),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASS"),
        start_tls=True,
    )
