# django-feedback

A Django app to gather and send internal Government staff feedback, e.g. for open beta periods

## Installation

```
pip install django-feedback-govuk
```

1. Add `django-feedback` to your INSTALLED_APPS settings:

```py
INSTALLED_APPS = [
    ...
    'crispy_forms',
    'crispy_forms_gds',
    'django_feedback_govuk',
]
```

2. Create a new email template in the GovUk Notify service, making sure to create a ((feedback_url)) field.

You'll need an API key and template ID from the gov.uk Notify service.

3. Add the following settings to the file:

```py
# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = ["gds"]
CRISPY_TEMPLATE_PACK = "gds"

# Gov Notify
GOVUK_NOTIFY_API_KEY="<your-api-key>"

# Django Feedback GovUK
DJANGO_FEEDBACK_GOVUK = {
    "SERVICE_NAME": "<your-service>",
    "FEEDBACK_NOTIFICATION_EMAIL_TEMPLATE_ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "FEEDBACK_NOTIFICATION_EMAIL_RECIPIENTS": ["email@example.com"],
    "SUBMIT_TEMPLATE": "path/to/submit.html",
    "CONFIRM_TEMPLATE": "path/to/confirm.html",
    "LISTING_TEMPLATE": "path/to/listing.html",
}
```

The email addresses are for every recipient that should get an email when feedback is submitted.

<!--
3. Load the template tags into your template:

```py

```

... or use the built-in templates:

```py

```

and add it to your urls.py:

```py

```
-->
