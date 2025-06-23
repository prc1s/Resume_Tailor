"""
Email sending utility for CVTailor.
"""
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config.settings import settings

logger = logging.getLogger(__name__)

class EmailSender:
    """Handles sending emails with attachments."""

    def send_email_with_attachments(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        attachments: list[tuple[bytes, str, str]]
    ):
        """
        Sends an email with one or more attachments.
        
        Args:
            recipient_email: The email address of the recipient.
            subject: The subject of the email.
            body: The HTML body of the email.
            attachments: A list of tuples, where each tuple contains
                         (attachment_bytes, filename, mime_type).
        """
        if not all([settings.EMAIL_HOST, settings.EMAIL_PORT, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD]):
            logger.error("Email settings are not configured. Cannot send email.")
            raise ValueError("Email server is not configured by the administrator.")

        msg = MIMEMultipart()
        msg['From'] = f"{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_HOST_USER}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        for content, filename, mime_type in attachments:
            part = MIMEApplication(content, Name=filename)
            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            msg.attach(part)
        
        try:
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.send_message(msg)
            logger.info(f"Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            raise

# Global email sender instance
email_sender = EmailSender() 