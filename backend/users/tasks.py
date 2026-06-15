from celery import shared_task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_email_task(subject, message, from_email, recipient_list, html_message=None):
    """
    Asynchronous task to send an email.
    """
    logger.info(f"Sending email to {recipient_list} with subject: {subject}")
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {recipient_list}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_list}: {str(e)}")
        # Optionally retry the task
        # raise self.retry(exc=e)
