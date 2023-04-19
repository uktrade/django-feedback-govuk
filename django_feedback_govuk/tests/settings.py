import os

import django.utils.crypto


TESTS_PATH = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = django.utils.crypto.get_random_string(50)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "crispy_forms",
    "crispy_forms_gds",
    "django_feedback_govuk",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

MEDIA_ROOT = os.path.join(TESTS_PATH, "media")

STATIC_ROOT = os.path.join(TESTS_PATH, "static")

ROOT_URLCONF = "django_feedback_govuk.tests.urls"


# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = ["gds"]
CRISPY_TEMPLATE_PACK = "gds"

# Django Feedback GovUK
DJANGO_FEEDBACK_GOVUK = {
    "SERVICE_NAME": "Example Project",
    "FEEDBACK_NOTIFICATION_EMAIL_TEMPLATE_ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "FEEDBACK_NOTIFICATION_EMAIL_RECIPIENTS": ["email@example.com"],
}
