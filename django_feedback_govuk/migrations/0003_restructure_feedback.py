# Generated by Django 3.2.20 on 2023-08-04 08:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def migrate_from_old_to_new_feedback(apps, schema_editor):
    OldFeedback = apps.get_model("django_feedback_govuk", "OldFeedback")
    Feedback = apps.get_model("django_feedback_govuk", "Feedback")

    for old_feedback in OldFeedback.objects.all():
        new_feedback = Feedback.objects.create(
            submitter=old_feedback.submitter,
            submitted_at=old_feedback.submitted_at,
            satisfaction=old_feedback.satisfaction,
            comment=old_feedback.comment,
        )
        new_feedback.save()


def migrate_from_new_to_old_feedback(apps, schema_editor):
    OldFeedback = apps.get_model("django_feedback_govuk", "OldFeedback")
    Feedback = apps.get_model("django_feedback_govuk", "Feedback")

    for new_feedback in Feedback.objects.all():
        old_feedback = OldFeedback.objects.create(
            submitter=new_feedback.submitter,
            submitted_at=new_feedback.submitted_at,
            satisfaction=new_feedback.satisfaction,
            comment=new_feedback.comment,
        )
        old_feedback.save()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("django_feedback_govuk", "0002_alter_feedback_submitter"),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseFeedback",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("submitted_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "submitter",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterModelOptions(
            options={
                "verbose_name": "Feedback Submission",
                "verbose_name_plural": "Feedback Submissions",
            },
            name="basefeedback",
        ),
        migrations.RenameModel(
            old_name="Feedback",
            new_name="OldFeedback",
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "basefeedback_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_feedback_govuk.basefeedback",
                    ),
                ),
                (
                    "satisfaction",
                    models.CharField(
                        choices=[
                            ("very_dissatisfied", "Very dissatisfied"),
                            ("dissatisfied", "Dissatisfied"),
                            ("neutral", "Neither satisfied or dissatisfied"),
                            ("satisfied", "Satisfied"),
                            ("very_satisfied", "Very satisfied"),
                        ],
                        max_length=30,
                    ),
                ),
                ("comment", models.TextField(blank=True)),
            ],
            bases=("django_feedback_govuk.basefeedback",),
        ),
        migrations.RunPython(
            migrate_from_old_to_new_feedback,
            migrate_from_new_to_old_feedback,
        ),
        migrations.DeleteModel(
            name="OldFeedback",
        ),
    ]