from django.test import TestCase
from django.urls import reverse

from django_feedback_govuk.models import Feedback, SatisfactionOptions
from django_feedback_govuk.tests.factories import UserFactory


class TestFeedbackView(TestCase):
    view_name = "feedback-submit"

    def setUp(self):
        self.view_url = reverse(self.view_name)
        self.user = UserFactory()

    def test_feedback_view_get(self):
        self.client.force_login(self.user)

        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
