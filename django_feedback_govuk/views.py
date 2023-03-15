from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView

from . import notify
from .forms import FeedbackForm
from .models import Feedback


class FeedbackView(FormView):
    template_name = "django_feedback_govuk/templates/submit.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("feedback-confirm")

    def get_initial(self):
        initial = super().get_initial()
        initial["submitter"] = self.request.user
        return initial

    def form_valid(self, form):
        form.save()
        # Send an email to inform the team of the feedback
        notify.email(
            personalisation={
                "feedback_url": self.request.build_absolute_uri(reverse("feedback-listing")),
            },
        )
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
