from django.urls import path

from . import views


urlpatterns = [
    path("submit/", views.FeedbackView.as_view(), name="feedback-submit"),
    path("submit/<form_id>/", views.get_feedback_view, name="custom-feedback-submit"),
    path("submit/<form_id>/confirm/", views.feedback_confirm, name="feedback-confirm"),
    path(
        "submitted/",
        views.SubmittedFeedback.as_view(),
        name="submitted-feedback",
    ),
    path(
        "submitted/<form_id>/",
        views.FeedbackListingView.as_view(),
        name="feedback-listing",
    ),
    # path("submit-ajax", views.AjaxFeedbackView.as_view(), name="feedback-submit-ajax"),
    # path("confirm-ajax/", views.feedback_confirm_ajax, name="feedback-confirm-ajax"),
]
