# django-feedback

A Django app to gather and send internal Government staff feedback, e.g. for open beta periods

## Installation

```
pip install django-feedback
```

1. Add `django-feedback` to your INSTALLED_APPS settings:

```py
INSTALLED_APPS = [
    ...
    "django_feedback_govuk"
]
```

2. Create a new email template in the GovUk Notify service

You'll need an API key and template ID from the gov.uk Notify service.

3. Add the following settings to the file:

```py
GOVUK_NOTIFY_API_KEY=<your-api-key>
DJANGO_FEEDBACK_GOVUK = {
    SERVICE_NAME = <your-service>
    FEEDBACK_NOTIFICATION_EMAIL_TEMPLATE_ID = xxx
    FEEDBACK_NOTIFICATION_EMAIL_RECIPIENTS = ["email@domain.com", ]
}
```

The email addresses are for every recipient that should get an email when feedback is submitted.

<!--
3. Load the template tags into your template:

```py

```
-->
