from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Fieldset, Hidden, Layout, Size, Submit
from django.forms import HiddenInput, Form, ModelForm, RadioSelect, CheckboxSelectMultiple, CheckboxInput, CharField, ChoiceField

from .models import Feedback, SatisfactionOptions
from .settings import dfg_settings

print("Now running", __file__)

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
        submitter_id = str(submitter.id) if submitter.id else None

        if issue_choices:
            self.fields["issues"].label = ""
            self.fields["issues"].required = False
            self.fields["issues"].widget = CheckboxSelectMultiple(attrs={"class": "corblimey"})
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
        ]
        if issue_choices:
            layouts.append(Fieldset(
                    Field.checkboxes("issues"),
                    legend=issues_legend,
                    legend_size=Size.MEDIUM,
                )
            )
        if activity_choices:
            layouts.append(Fieldset(
                    Field.checkboxes("activities"),
                    legend=activities_legend,
                    legend_size=Size.MEDIUM,
                )
            )
        layouts += [
            Fieldset(
                HTML(f"<p class='govuk-hint'>{comment_hint}</p>"),
                Field("comment"),
                legend=comment_legend,
                legend_size=Size.MEDIUM,
            ),
            Submit("submit", "Submit feedback"),
        ]

        self.helper = FormHelper()
        self.helper.layout = Layout(*layouts)

class StarsForm(Form):
    satisfaction = ChoiceField(required=True, widget=RadioSelect, choices=SatisfactionOptions.choices)
    submit = Submit("submit", "Submit feedback")
    def __init__(self,
                 satisfaction_legend = dfg_settings.COPY_FIELD_SATISFACTION_LEGEND,
                 *args,
                 **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout=Layout(
            Hidden("submitter", "Need code here!"),
            Fieldset(
                Field.radios(
                    "satisfaction",
                    template="django_feedback_govuk/widgets/star_rating/star_rating.html",
                ),
                legend=satisfaction_legend,
                legend_size=Size.MEDIUM,
            ),
            Submit("submit", "Submit feedback")
        )


