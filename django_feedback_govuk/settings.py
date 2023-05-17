from typing import List

from django.conf import settings


DEFAULTS = {
    "SERVICE_NAME": (sn := "Example Service"),
    "FEEDBACK_NOTIFICATION_EMAIL_TEMPLATE_ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "FEEDBACK_NOTIFICATION_EMAIL_RECIPIENTS": [
        "email@example.com",
    ],
    "ISSUE_CHOICES": [
        ("0001", "I did not experience any issues"),
        ("0002", "Process is not clear"),
        ("0003", "Not enough guidance"),
        ("0004", "I was asked for information I did not have"),
        ("0005", "I did not get the information I expected"),
        ("0006", "Other issue (please describe below")
    ],
    "ISSUES_LEGEND": "Which of the following issues did you experience?",
    "COPY": {
        "SUBMIT_TITLE": f"Give feedback on {sn}",
        "CONFIRM_TITLE": "Feedback submitted",
        "CONFIRM_BODY": "Thank you for submitting your feedback.",
        "FIELD_SATISFACTION_LEGEND": "Overall, how did you feel about the service you received today?",
        "FIELD_COMMENT_LEGEND": "How could we improve this service?",
        "FIELD_COMMENT_HINT": "Do not include any personal or financial information, for example your National Insurance or credit card numbers.",
    },
}


class DjangoFeedbackGovUKSettings:
    SERVICE_NAME: str
    FEEDBACK_NOTIFICATION_EMAIL_TEMPLATE_ID: str
    FEEDBACK_NOTIFICATION_EMAIL_RECIPIENTS: List[str]
    COPY_SUBMIT_TITLE: str
    COPY_CONFIRM_TITLE: str
    COPY_CONFIRM_BODY: str
    COPY_FIELD_SATISFACTION_LEGEND: str
    COPY_FIELD_COMMENT_LEGEND: str
    COPY_FIELD_COMMENT_HINT: str

    def __getattr__(self, attr):
        django_settings = getattr(settings, "DJANGO_FEEDBACK_GOVUK", {})

        # Get COPY values
        if attr.startswith("COPY_"):
            copy_key = attr[5:]
            try:
                return django_settings.get("COPY", {}).get(copy_key, DEFAULTS["COPY"][copy_key])
            except KeyError:
                raise ValueError(f"No value for {attr!r} and no default provided")
        if attr in django_settings:
            # Return the value from user settings
            return django_settings[attr]

        default_value = DEFAULTS.get(attr, None)
        if default_value is None and attr not in DEFAULTS:
            raise AttributeError(f"No value set for DJANGO_FEEDBACK_GOVUK[{attr!r}]")
        # Return the value from defaults
        return default_value

dfg_settings = DjangoFeedbackGovUKSettings()
