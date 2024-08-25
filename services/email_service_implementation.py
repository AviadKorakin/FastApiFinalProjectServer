import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

from services.email_service import EmailService

# Load environment variables from .env file
load_dotenv()

class EmailServiceImplementation(EmailService):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EmailService, cls).__new__(cls)
        return cls._instance

    def send_verification_email(self, recipient_email: str, verification_url: str):
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        sender_email = os.getenv("SMTP_SENDER_EMAIL", smtp_username)

        subject = "Your Verification Email"
        body = (
            f"Please verify your email address by clicking the following link:\n\n"
            f"{verification_url}\n\n"
            f"If you did not request this verification, please ignore this email."
        )

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Establish a secure session with the server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            print(f"Verification email sent to {recipient_email} with verification URL: {verification_url}")
        except Exception as e:
            print(f"Failed to send verification email to {recipient_email}: {str(e)}")