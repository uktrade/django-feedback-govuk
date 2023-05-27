from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Fieldset, Hidden, Layout, Size, Submit
from django.forms import HiddenInput, Form, ModelForm, RadioSelect, CheckboxSelectMultiple, CheckboxInput, CharField, ChoiceField, IntegerField, Textarea, TextInput

from .models import SatisfactionOptions
from .settings import dfg_settings

class FeedbackForm(Form):
    issues = ChoiceField(label="", required=True, widget=CheckboxSelectMultiple(attrs={"class": "corblimey"}), choices=dfg_settings.ISSUE_CHOICES)
    issue_comment = CharField(widget=Textarea(attrs={"name": "issue_comment", 'rows': 4}))
    activities = ChoiceField(label="", required=True, widget=CheckboxSelectMultiple(), choices=dfg_settings.ACTIVITY_CHOICES)
    activity_comment = CharField(widget=Textarea(attrs={"name": "activity_comment", 'rows': 4}))
    comment = CharField(widget=Textarea(attrs={"name": "comment", 'rows': 4}))

    def __init__(self,
                 *args,
                 project=None,
                 user_id=None,
                 satisfaction_legend = dfg_settings.COPY_FIELD_SATISFACTION_LEGEND,
                 comment_hint=dfg_settings.COPY_FIELD_COMMENT_HINT,
                 issues_legend=dfg_settings.ISSUES_LEGEND,
                 comment_legend=dfg_settings.COPY_FIELD_COMMENT_LEGEND,
                 activities_legend=dfg_settings.ACTIVITIES_LEGEND,
                 **kwargs):
        super().__init__(*args, **kwargs)

        layouts = [
            Hidden("user_id", user_id),
            Hidden("project", project)
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
                    Field.textarea("activity_comment"),
                    legend=activities_legend,
                    legend_size=Size.MEDIUM,
                )
            )


        layouts += [
            Fieldset(
                HTML(f"<p class='govuk-hint'>{comment_hint}</p>"),
                Field.textarea("comment"),
                legend=comment_legend,
                legend_size=Size.MEDIUM,
            ),
            Submit("submit", "Submit feedback"),
        ]

        self.helper = FormHelper()
        self.helper.layout = Layout(*layouts)

    def is_valid(self):
        return True

    def update(self):
        """
        Take the record established by the star rating and add feedback.
        """

class StarsForm(Form):
    satisfaction = ChoiceField(required=True, widget=RadioSelect, choices=SatisfactionOptions.choices)
    submit = Submit("submit", "Submit feedback")
    def __init__(self,
                 satisfaction_legend=dfg_settings.COPY_FIELD_SATISFACTION_LEGEND,
                 project=None,
                 user_id=None,
                 *args,
                 **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout=Layout(
            Hidden("user_id", user_id),
            Hidden("project", project),
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

        def save(self):

            """
            Store a new record with only the star rating in it.
            """

