from django.test import TestCase
from django.urls import reverse


class HelpTestCase(TestCase):
    """Tests for the Help page."""

    def test_help(self):
        response = self.client.get("/help/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="help/index.html")

    def test_help_available_by_name(self):
        response = self.client.get(reverse("help"))
        self.assertEqual(response.status_code, 200)


class PrivacyTestCase(TestCase):
    """Tests for the Privacy Policy page."""

    def test_privacy(self):
        response = self.client.get("/help/privacy")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="help/privacy.html")

    def test_privacy_available_by_name(self):
        response = self.client.get(reverse("privacy"))
        self.assertEqual(response.status_code, 200)


class GuidelinesTestCase(TestCase):
    """Tests for the Community Guidelines page."""

    def test_guidelines(self):
        response = self.client.get("/help/community-guidelines")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="help/community-guidelines.html")

    def test_guidelines_available_by_name(self):
        response = self.client.get(reverse("community-guidelines"))
        self.assertEqual(response.status_code, 200)


class ManualTestCase(TestCase):
    """Tests for the User Manual page."""

    def test_manual(self):
        response = self.client.get("/help/manual")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="help/manual.html")

    def test_guidelines_available_by_name(self):
        response = self.client.get(reverse("manual"))
        self.assertEqual(response.status_code, 200)
