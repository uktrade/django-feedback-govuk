from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Fieldset, Hidden, Layout, Size, Submit
from django.forms import ModelForm, RadioSelect

from django_feedback_govuk.models import BaseFeedback, Feedback, SatisfactionOptions
from django_feedback_govuk.settings import dfg_settings


SUBMIT_BUTTON = Submit("submit", "Send feedback")


class BaseFeedbackForm(ModelForm):
    class Meta:
        model = BaseFeedback
        fields = ["submitter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        submitter = self.initial["submitter"]
        submitter_id = str(submitter.id) if submitter.id else ""

        self.fields["submitter"].required = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Hidden("submitter", submitter_id),
            SUBMIT_BUTTON,
        )


class FeedbackForm(BaseFeedbackForm):
    class Meta:
        model = Feedback
        fields = ["satisfaction", "comment", "submitter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["satisfaction"].label = ""
        self.fields["satisfaction"].required = True
        self.fields["satisfaction"].widget = RadioSelect()
        self.fields["satisfaction"].choices = SatisfactionOptions.choices
        self.fields["comment"].label = ""

        self.helper.layout.remove(SUBMIT_BUTTON)
        self.helper.layout.append(
            Fieldset(
                Field.radios(
                    "satisfaction",
                    template="django_feedback_govuk/widgets/star_rating/star_rating.html",
                ),
                legend=dfg_settings.COPY_FIELD_SATISFACTION_LEGEND,
                legend_size=Size.MEDIUM,
            )
        )
        self.helper.layout.append(
            Fieldset(
                HTML(
                    f"<p class='govuk-hint'>{dfg_settings.COPY_FIELD_COMMENT_HINT}</p>"
                ),
                Field("comment"),
                legend=dfg_settings.COPY_FIELD_COMMENT_LEGEND,
                legend_size=Size.MEDIUM,
            )
        )
        self.helper.layout.append(SUBMIT_BUTTON)
