from typing import Dict

from django.conf import settings
from notifications_python_client.notifications import NotificationsAPIClient


def email(personalisation: Dict):
    notification_client = NotificationsAPIClient(
        settings.GOVUK_NOTIFY_API_KEY,
    )
    email_addresses = settings.FEEDBACK_NOTIFICATION_EMAIL_RECIPIENTS

    for email_address in email_addresses:
        message_response = notification_client.send_email_notification(
            email_address=email_address,
            template_id=settings.FEEDBACK_NOTIFICATION_EMAIL_TEMPLATE_ID.value,
            personalisation=personalisation,
        )

    return message_response
