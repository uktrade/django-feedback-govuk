from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Fieldset, Hidden, Layout, Size, Submit
from django.forms import HiddenInput, Form, ModelForm, RadioSelect, CheckboxSelectMultiple, CheckboxInput, CharField, ChoiceField, IntegerField, Textarea, TextInput

from .models import Feedback, SatisfactionOptions
from .settings import dfg_settings

print("Now running", __file__)

class FeedbackForm(Form):
    issues = ChoiceField(label="", required=True, widget=CheckboxSelectMultiple(attrs={"class": "corblimey"}), choices=dfg_settings.ISSUE_CHOICES)
    issue_comment = CharField()
    activities = ChoiceField(label="", required=True, widget=CheckboxSelectMultiple(), choices=dfg_settings.ACTIVITY_CHOICES)
    activity_comment = CharField()
    comment = CharField()

    def __init__(self,
                 satisfaction_legend = dfg_settings.COPY_FIELD_SATISFACTION_LEGEND,
                 comment_hint=dfg_settings.COPY_FIELD_COMMENT_HINT,
                 issues_legend=dfg_settings.ISSUES_LEGEND,
                 comment_legend=dfg_settings.COPY_FIELD_COMMENT_LEGEND,
                 activities_legend=dfg_settings.ACTIVITIES_LEGEND,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        submitter = self.initial["submitter"]
        submitter_id = str(submitter.id) if submitter.id else None

        layouts = [
            Hidden("submitter", submitter_id),
        ]
        if dfg_settings.ISSUE_CHOICES:
            layouts.append(
                Fieldset(
                    Field.checkboxes("issues"),
                    Field("issue_comment"),
                    legend=issues_legend,
                    legend_size=Size.MEDIUM,
                )
            )
        if dfg_settings.ACTIVITY_CHOICES:
            layouts.append(Fieldset(
                    Field.checkboxes("activities"),
                    Field.textarea("activity_comment", rows=4),
                    legend=activities_legend,
                    legend_size=Size.MEDIUM,
                )
            )


        layouts += [
            Fieldset(
                HTML(f"<p class='govuk-hint'>{comment_hint}</p>"),
                Field.textarea("comment", rows=4),
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


