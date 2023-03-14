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
    "django-feedback"
]
```

2. Add the following settings to the file:

```py
GOVUK_NOTIFY_API_KEY=<your-api-key>
FEEDBACK_NOTIFICATION_EMAIL_TEMPLATE_ID = xxx
FEEDBACK_NOTIFICATION_EMAIL_RECIPIENTS = ["email@domain.com", ]
```

3. Load the template tags and add the dev client plus any css and js:

```py

```
