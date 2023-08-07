from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

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


class TestSubmittedView(TestCase):
    view_name = "submitted-feedback"

    def setUp(self):
        self.view_url = reverse(self.view_name)
        self.user = UserFactory()

    def test_no_permission(self):
        self.client.force_login(self.user)

        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/submitted/default/")

    def test_has_permission(self):
        self.user.user_permissions.add(
            Permission.objects.get(
                name="Can view feedback",
            ),
        )
        self.client.force_login(self.user)

        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/submitted/default/")


class TestSubmittedListingView(TestCase):
    view_name = "feedback-listing"

    def setUp(self):
        self.view_url = reverse(self.view_name, kwargs={"form_id": "default"})
        self.user = UserFactory()

    def test_no_permission(self):
        self.client.force_login(self.user)

        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 403)

    def test_has_permission(self):
        self.user.user_permissions.add(
            Permission.objects.get(
                name="Can view feedback",
            ),
        )
        self.client.force_login(self.user)

        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
