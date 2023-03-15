from django.urls import path

from . import views


urlpatterns = [
    path("", views.FeedbackView.as_view(), name="feedback-submit"),
    path("confirm/", views.feedback_confirm, name="feedback-confirm"),
    path("listing/", views.FeedbackListingView.as_view(), name="feedback-listing"),
    path("submit-ajax", views.FeedbackView.as_view(), name="feedback-submit-ajax"),
    path("confirm-ajax/", views.feedback_confirm, name="feedback-confirm-ajax"),
]
