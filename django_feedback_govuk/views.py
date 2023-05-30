from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView

from . import notify
from .forms import FeedbackForm, StarsForm
from .models import Feedback

class StarsView(FormView):
    template_name = "django_feedback_govuk/templates/stars.html"
    form_class = StarsForm
    success_url = reverse_lazy("feedback-submit")

    def get_form_kwargs(self):
        """
        Inject user_id and project name to pass as hidden fields.

        Started out as an exact copy of FeedbackView.get_form_kwargs ...
        """
        kw = super().get_form_kwargs()
        kw['project'] = self.request.session.pop('project')
        kw['user_id'] = None
        if self.request.user.is_authenticated:
            kw['user_id'] = self.request.user.id
        return kw

    def form_valid(self):
        record = dict(
            user_id=self.user_id,
            project=self.project,
            satisfaction=self.satisfaction,
        )


class FeedbackView(FormView):
    template_name = "django_feedback_govuk/templates/submit.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("feedback-confirm")

    def get_form_kwargs(self):
        """
        Inject project ID stored in session to form creation arguments.
        """
        kw = super().get_form_kwargs()
        kw['user_id'] = None
        if self.request.user.is_authenticated:
            kw['user_id'] = self.request.user.id
        return kw


    def form_valid(self, form):
        form.update()  # Update the star rating with other feedback
        return super().form_valid(form)


def feedback_confirm(request):
    return render(request, "django_feedback_govuk/templates/confirm.html")


class UserCanViewFeedback(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("feedback.view_feedback")


class FeedbackListingView(UserCanViewFeedback, ListView):
    template_name = "django_feedback_govuk/templates/listing.html"
    model = Feedback
    paginate_by = 5

    def get_queryset(self):
        return Feedback.objects.all().order_by("-submitted_at")

# #
# # AJAX supporting views - e.g. using HTMX to render without pageloads
# #

# class AjaxFeedbackView(FeedbackView):
#     template_name = "django_feedback_govuk/partials/submit.html"
#     success_url = reverse_lazy("feedback-confirm-ajax")


# def feedback_confirm_ajax(request):
#     return render(request, "django_feedback_govuk/partials/confirm.html")
