from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.enums import TextChoices


class SatisfactionOptions(TextChoices):
    """
    Enum for the satisfaction options.
    """

    VERY_DISSATISFIED = "very_dissatisfied", "Very dissatisfied"
    DISSATISFIED = "dissatisfied", "Dissatisfied"
    NEUTRAL = "neutral", "Neither satisfied or dissatisfied"
    SATISFIED = "satisfied", "Satisfied"
    VERY_SATISFIED = "very_satisfied", "Very satisfied"


class Feedback(models.Model):
    """

    """
    id = models.IntegerField(primary_key=True)
    placement = models.CharField(max_length=12)
    satisfaction = models.CharField(max_length=30, choices=SatisfactionOptions.choices)
    comment = models.TextField(default="")
    issues = models.JSONField(default=None)
    activities = models.JSONField(default=None)
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    submitted_at = models.DateTimeField(null=True, auto_now_add=True)

    class Meta:
        verbose_name = "Feedback Submission"
        verbose_name_plural = "Feedback Submissions"
