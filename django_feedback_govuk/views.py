from typing import Any, Dict

from django import http
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.module_loading import import_string
from django.views.generic import FormView, ListView

from django_feedback_govuk import notify
from django_feedback_govuk.models import BaseFeedback, Feedback
from django_feedback_govuk.settings import DEFAULT_FEEDBACK_ID, dfg_settings


class FeedbackView(FormView):
    template_name = "django_feedback_govuk/templates/submit.html"
    success_url = reverse_lazy("feedback-confirm")

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        self.form_id = kwargs.get("form_id", DEFAULT_FEEDBACK_ID)

        try:
            self.feedback_config = dfg_settings.FEEDBACK_FORMS[self.form_id]
        except KeyError:
            raise ValueError(f"Unknown feedback form ID: {self.form_id}")
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return import_string(self.feedback_config["form"])

    def get_initial(self):
        initial = super().get_initial()
        initial["submitter"] = self.request.user
        return initial

    def form_valid(self, form):
        form.save()
        # Send an email to inform the team of the feedback
        notify.email(
            personalisation={
                "feedback_url": self.request.build_absolute_uri(
                    reverse("feedback-listing")
                ),
            },
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form_id"] = self.form_id
        return context


def get_feedback_view(request, *args, **kwargs):
    form_id = kwargs.get("form_id", DEFAULT_FEEDBACK_ID)
    feedback_config = dfg_settings.FEEDBACK_FORMS[form_id]
    feedback_view: FormView = import_string(feedback_config["view"])
    return feedback_view.as_view()(request, *args, **kwargs)


def feedback_confirm(request):
    return render(request, "django_feedback_govuk/templates/confirm.html")


class UserCanViewFeedback(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("django_feedback_govuk.view_feedback")


class FeedbackListingView(UserCanViewFeedback, ListView):
    template_name = "django_feedback_govuk/templates/listing.html"
    model = BaseFeedback
    paginate_by = 5

    def get_queryset(self):
        return BaseFeedback.objects.all().order_by("-submitted_at")


# #
# # AJAX supporting views - e.g. using HTMX to render without pageloads
# #

# class AjaxFeedbackView(FeedbackView):
#     template_name = "django_feedback_govuk/partials/submit.html"
#     success_url = reverse_lazy("feedback-confirm-ajax")


# def feedback_confirm_ajax(request):
#     return render(request, "django_feedback_govuk/partials/confirm.html")
