from typing import Dict

from django.conf import settings
from notifications_python_client.notifications import NotificationsAPIClient

from .settings import dfg_settings


def email(personalisation: Dict):
    notification_client = NotificationsAPIClient(
        settings.GOVUK_NOTIFY_API_KEY,
    )
    email_addresses = dfg_settings.FEEDBACK_NOTIFICATION_EMAIL_RECIPIENTS

    if len(email_addresses) < 1:
        raise Exception("No feedback recipients configured")

    for email_address in email_addresses:
        message_response = notification_client.send_email_notification(
            email_address=email_address,
            template_id=dfg_settings.FEEDBACK_NOTIFICATION_EMAIL_TEMPLATE_ID,
            personalisation=personalisation,
        )

    return message_response
