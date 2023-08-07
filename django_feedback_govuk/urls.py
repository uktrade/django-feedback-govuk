from django.urls import path

from . import views


urlpatterns = [
    path("stars/<str:project>/", views.StarsView.as_view(), name="get-stars"),
    path("stars/", views.StarsView.as_view(), name="feedback-stars"),
    path("extra/", views.FeedbackView.as_view(), name="feedback-submit"),
    path("confirm/", views.feedback_confirm, name="feedback-confirm"),
    path("listing/", views.FeedbackListingView.as_view(), name="feedback-listing"),
    # path("submit-ajax", views.AjaxFeedbackView.as_view(), name="feedback-submit-ajax"),
    # path("confirm-ajax/", views.feedback_confirm_ajax, name="feedback-confirm-ajax"),
]
