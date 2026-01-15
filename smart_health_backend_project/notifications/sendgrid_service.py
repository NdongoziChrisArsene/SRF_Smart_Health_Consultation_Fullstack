import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger("email")

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@example.com")


def send_health_consultation_email(to_email, dynamic_data, template_id):
    if not all([to_email, template_id, SENDGRID_API_KEY]):
        logger.error("SendGrid email missing required data.")
        return False

    message = Mail(from_email=FROM_EMAIL, to_emails=to_email)
    message.template_id = template_id
    message.dynamic_template_data = dynamic_data

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return True
    except Exception as e:
        logger.error("SendGrid error", exc_info=True)
        return False






















