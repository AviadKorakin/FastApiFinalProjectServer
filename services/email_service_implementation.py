import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from services.email_service import EmailService


class EmailServiceImplementation(EmailService):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EmailServiceImplementation, cls).__new__(cls)
        return cls._instance

    async def send_verification_email(self, recipient_email: str, verification_url: str):
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        sender_email = os.getenv("SMTP_SENDER_EMAIL", smtp_username)

        if not smtp_username or not smtp_password:
            raise ValueError("SMTP credentials are missing. Ensure SMTP_USERNAME and SMTP_PASSWORD are set.")

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
        msg.attach(MIMEText(body, 'plain'))

        # Convert message to string
        message = msg.as_string()

        try:
            # Use aiosmtplib for async email sending
            await aiosmtplib.send(
                message,
                hostname=smtp_server,
                port=smtp_port,
                start_tls=True,  # Enable TLS
                username=smtp_username,
                password=smtp_password,
                sender=sender_email,
                recipients=[recipient_email],
            )
            print(f"Verification email sent to {recipient_email} with verification URL: {verification_url}")
        except aiosmtplib.SMTPException as e:
            print(f"Failed to send verification email to {recipient_email}: {str(e)}")
            raise ValueError(f"Failed to send email: {str(e)}")

