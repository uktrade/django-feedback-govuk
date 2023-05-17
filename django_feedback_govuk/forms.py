from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Fieldset, Hidden, Layout, Size, Submit
from django.forms import HiddenInput, ModelForm, RadioSelect, CheckboxSelectMultiple, CheckboxInput

from .models import Feedback, SatisfactionOptions
from .settings import dfg_settings


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["satisfaction", "issues", "activities", "comment", "submitter"]

    def __init__(self,
                 issue_choices=dfg_settings.ISSUE_CHOICES,
                 satisfaction_legend = dfg_settings.COPY_FIELD_SATISFACTION_LEGEND,
                 comment_hint=dfg_settings.COPY_FIELD_COMMENT_HINT,
                 issues_legend=dfg_settings.ISSUES_LEGEND,
                 comment_legend=dfg_settings.COPY_FIELD_COMMENT_LEGEND,
                 activity_choices=dfg_settings.ACTIVITY_CHOICES,
                 activities_legend=dfg_settings.ACTIVITIES_LEGEND,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        submitter = self.initial["submitter"]
        submitter_id = str(submitter.id) if submitter.id else "anonymous user"

        self.fields["satisfaction"].label = ""
        self.fields["satisfaction"].required = True
        self.fields["satisfaction"].widget = RadioSelect()
        self.fields["satisfaction"].choices = SatisfactionOptions.choices
        self.fields["issues"].label = ""
        self.fields["issues"].required = False
        self.fields["issues"].widget = CheckboxSelectMultiple()
        self.fields["issues"].choices = issue_choices
        if activity_choices:
            self.fields["activities"].label=""
            self.fields["activities"].required = True
            self.fields["activities"].widget = CheckboxSelectMultiple()
            self.fields["activities"].choices = activity_choices
        self.fields["comment"].label = ""
        self.fields["submitter"].required = False

        layouts = [
            Hidden("submitter", submitter_id),
            Fieldset(
                Field.radios(
                    "satisfaction",
                    template="django_feedback_govuk/widgets/star_rating/star_rating.html",
                ),
                legend=satisfaction_legend,
                legend_size=Size.MEDIUM,
            ),
            Fieldset(
                Field.checkboxes("issues"),
                legend=issues_legend,
                legend_size=Size.MEDIUM,
            )
        ]
        if activity_choices:
            layouts += [
                Fieldset(
                    Field.checkboxes("activities"),
                    legend=activities_legend,
                    legend_size=Size.MEDIUM,
                )
            ]
        layouts += [
            Fieldset(
                HTML(f"<p class='govuk-hint'>{comment_hint}</p>"),
                Field("comment"),
                legend=comment_legend,
                legend_size=Size.MEDIUM,
            ),
            Submit("submit", "Send feedback"),
        ]

        self.helper = FormHelper()
        self.helper.layout = Layout(*layouts)

