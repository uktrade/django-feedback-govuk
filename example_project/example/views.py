from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from .forms import ProjectSelectForm, ResponseSelectionForm

class ProjectSelectView(FormView):

    template_name = "project_select.html"
    form_class = ProjectSelectForm

    def form_valid(self, form):
        self.project = form.cleaned_data.get('project')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('choose-questions', args=(self.project,))

class ChooseQuestionsView(FormView):

    template_name = "project_select.html"
    form_class = ResponseSelectionForm


    def get(self, request, project):
        request.session['project'] = project
        return super().get(self, self.request)

    def post(self, request, *args, **kwargs):
        print("POST Args was", args, "kwargs was", kwargs)
        return redirect("/feedback/")

    def get_form_kwargs(self):
        """
        Inject project ID stored in session to form creation arguments.
        """
        kw = super().get_form_kwargs()
        kw['project'] = self.request.session['project']
        kw['username'] = "Anonymous User"
        if self.request.user.is_authenticated:
            kw['username'] = self.request.user.username
        return kw

