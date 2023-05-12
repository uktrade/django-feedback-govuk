from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Fieldset, Layout, Size, Submit
from django.conf import settings
from django.forms import HiddenInput, ModelForm, RadioSelect

from .models import Feedback, SatisfactionOptions
from .settings import dfg_settings


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["satisfaction", "comment", "submitter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["submitter"].widget = HiddenInput()
        self.fields["satisfaction"].label = ""
        self.fields["satisfaction"].required = True
        self.fields["satisfaction"].widget = RadioSelect()
        self.fields["satisfaction"].choices = SatisfactionOptions.choices
        self.fields["comment"].label = ""

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field("submitter"),
            Fieldset(
                Field.radios(
                    "satisfaction",
                    template="django_feedback_govuk/widgets/star_rating/star_rating.html",
                ),
                legend=dfg_settings.COPY_FIELD_SATISFACTION_LEGEND,
                legend_size=Size.MEDIUM,
            ),
            Fieldset(
                HTML(f"<p class='govuk-hint'>{dfg_settings.COPY_FIELD_COMMENT_HINT}</p>"),
                Field("comment"),
                legend=dfg_settings.COPY_FIELD_COMMENT_LEGEND,
                legend_size=Size.MEDIUM,
            ),
            Submit("submit", "Send feedback"),
        )
