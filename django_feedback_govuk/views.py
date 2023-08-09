from typing import Any, Dict

from django import http
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.module_loading import import_string
from django.views.generic import FormView, ListView, TemplateView

from django_feedback_govuk import notify
from django_feedback_govuk.models import BaseFeedback
from django_feedback_govuk.settings import DEFAULT_FEEDBACK_ID, dfg_settings


class FeedbackView(FormView):
    template_name = "django_feedback_govuk/templates/submit.html"

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        self.form_id = kwargs.get("form_id", DEFAULT_FEEDBACK_ID)

        try:
            self.feedback_config = dfg_settings.FEEDBACK_FORMS[self.form_id]
        except KeyError:
            raise ValueError(f"Unknown feedback form ID: {self.form_id}")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("feedback-confirm", kwargs={"form_id": self.form_id})

    def get_form_class(self):
        return import_string(self.feedback_config["form"])

    def get_initial(self):
        initial = super().get_initial()
        initial["submitter"] = self.request.user
        return initial

    def form_valid(self, form):
        form.save()
        feedback_listing_path = reverse(
            "feedback-listing",
            kwargs={"form_id": self.form_id},
        )
        # Send an email to inform the team of the feedback
        notify.email(
            personalisation={
                "feedback_url": self.request.build_absolute_uri(feedback_listing_path),
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


def feedback_confirm(request, *args, **kwargs):
    form_id = kwargs.get("form_id", DEFAULT_FEEDBACK_ID)
    context = {
        "form_id": form_id,
    }
    return render(request, "django_feedback_govuk/templates/confirm.html", context)


class UserCanViewFeedback(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("django_feedback_govuk.view_feedback")


class SubmittedFeedback(UserCanViewFeedback, TemplateView):
    template_name = "django_feedback_govuk/templates/submitted.html"

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        self.feedback_forms: Dict[str, str] = {}

        for feedback_form_id in dfg_settings.FEEDBACK_FORMS:
            feedback_config = dfg_settings.FEEDBACK_FORMS.get(feedback_form_id)
            feedback_model = import_string(feedback_config["model"])
            self.feedback_forms[feedback_form_id] = {
                "submission_count": feedback_model.objects.all().count()
            }

        if len(self.feedback_forms) == 1:
            form_id = list(self.feedback_forms.keys())[0]
            return redirect(
                reverse(
                    "feedback-listing",
                    kwargs={
                        "form_id": form_id,
                    },
                )
            )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["feedback_forms"] = self.feedback_forms

        return context


class FeedbackListingView(UserCanViewFeedback, ListView):
    template_name = "django_feedback_govuk/templates/listing.html"
    model = BaseFeedback
    paginate_by = 5

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        self.form_id = kwargs.get("form_id", DEFAULT_FEEDBACK_ID)

        feedback_config = dfg_settings.FEEDBACK_FORMS[self.form_id]
        self.feedback_form = import_string(feedback_config["form"])
        self.feedback_model = import_string(feedback_config["model"])

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.feedback_model.objects.all().order_by("-submitted_at")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        form = self.feedback_form(
            initial={
                "submitter": self.request.user,
            },
        )
        form_fields = list(form.fields)
        # Move 'submitter' to the end.
        form_fields.remove("submitter")
        form_fields.append("submitter")

        context.update(
            form_id=self.form_id,
            form=form,
            fields=form_fields,
            model=self.feedback_model,
            hide_back_button=len(dfg_settings.FEEDBACK_FORMS) == 1,
        )
        return context


# #
# # AJAX supporting views - e.g. using HTMX to render without pageloads
# #

# class AjaxFeedbackView(FeedbackView):
#     template_name = "django_feedback_govuk/partials/submit.html"
#     success_url = reverse_lazy("feedback-confirm-ajax")


# def feedback_confirm_ajax(request):
#     return render(request, "django_feedback_govuk/partials/confirm.html")
