from django.db import models

from django_feedback_govuk.models import Feedback


class CustomFeedback(Feedback):
    extra_comments = models.TextField(blank=True)
