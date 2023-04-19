from django.urls import include, path

from django_feedback_govuk import urls as feedback_urls


urlpatterns = [
    path("", include(feedback_urls)),
]
