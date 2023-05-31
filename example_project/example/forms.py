from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Fieldset, Hidden, Layout, Size, Submit
from django.forms import HiddenInput, Form, ModelForm, RadioSelect, CheckboxSelectMultiple, CheckboxInput, CharField, ChoiceField, IntegerField, Textarea, TextInput
from django_feedback_govuk.settings import dfg_settings

PROJECT_CHOICES = [
    (p, p) for p in ("DMAS", "TWUK", "LITE", "ICMS")
]

class ProjectSelectForm(Form):

    project = ChoiceField(choices=PROJECT_CHOICES, required=True)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        print("SELECT FORM. Args:", args, "Kwarg:", kw)
        submitter_id = "Anonymous Coward"
        layouts = [
            Hidden("submitter", submitter_id),
            "project",
            Submit("submit", "Select Project"),
        ]
        self.helper = FormHelper()
        self.helper.layout = Layout(*layouts)


class ResponseSelectionForm(Form):

    heading = CharField(max_length=50, required=True, label="What heading would you like above your selected response options?")
    responses = ChoiceField()  # placeholder
    submit = Submit("submit", "Submit feedback")

    def __init__(
        self,
        project=None,
        username=None,
        issues_legend="Select the questions for your form",
        *args,
        **kwargs):
        super().__init__(*args, **kwargs)
        print("RESPONSE FORM. Args:", args, "Kwarg:", kwargs, "")
        self.project = project
        self.fields["responses"] = ChoiceField(
            choices=self.choices,
            label="Select the responses you'd like as options on the questionnaire",
            widget=CheckboxSelectMultiple,
        )
        print("RESPONSE FORM. Args:", *args, "project:", project, "kwargs:", kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "heading",
                Field.checkboxes("responses"),
                 legend=issues_legend,
                legend_size=Size.MEDIUM,
            ),
            Submit("submit", "Submit feedback")
        )

    def choices(self):
        """
        Return the choices for the project selected in the
        """
        return [(f"{self.project}_{i+1}", f"{self.project} Question {i+1}") for i in range(10)]


    def post(self):
        print("Debug me!")
        print()