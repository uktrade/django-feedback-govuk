from django.db import models

from django_feedback_govuk.models import BaseFeedback, SatisfactionOptions


class CustomFeedback(BaseFeedback):
    satisfaction = models.CharField(max_length=30, choices=SatisfactionOptions.choices)
    comment = models.TextField(blank=True)

    extra_comments = models.TextField(blank=True)
