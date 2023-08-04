from crispy_forms_gds.layout import Field, Fieldset, Size
from custom_feedback.models import CustomFeedback

from django_feedback_govuk.forms import SUBMIT_BUTTON, FeedbackForm


class CustomFeedbackForm(FeedbackForm):
    class Meta:
        model = CustomFeedback
        fields = ["satisfaction", "comment", "submitter", "extra_comments"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["extra_comments"].label = ""

        self.helper.layout.remove(SUBMIT_BUTTON)
        self.helper.layout.append(
            Fieldset(
                Field("extra_comments"),
                legend="Extra comments",
                legend_size=Size.MEDIUM,
            )
        )
        self.helper.layout.append(SUBMIT_BUTTON)
