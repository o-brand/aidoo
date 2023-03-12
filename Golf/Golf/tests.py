from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from .middlewares import ENABLED_URLS, LoginRequiredMiddleware
from .validators import validate_profanity


# Get actual user model.
User = get_user_model()


def dummy_middleware(_):
    """Returns an HTTPS response with status code 200. Use ONLY for tests!"""
    response = HttpResponse()
    response.status_code = 200
    return response


class LoginRequiredMiddlewareTestCase(TestCase):
    """Tests for LoginRequiredMiddleware."""

    def setUp(self):
        """Saves the Middleware before every tests."""
        self.middleware = LoginRequiredMiddleware(dummy_middleware)

    def test_user_not_logged_id(self):
        """Tests what happens if the user is NOT authenticated."""
        request = RequestFactory()
        request.user = AnonymousUser()
        request.path_info = "/jobs/post"

        # Get the response using the Middleware
        response = self.middleware(request)

        # Assert the redirection
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login?next=/jobs/post")

    def test_user_logged_id(self):
        """Tests what happens if the user is authenticated."""
        request = RequestFactory()
        request.user = User()
        request.path_info = "/jobs/post"

        # Get the response using the Middleware
        response = self.middleware(request)

        # Assert no redirection
        self.assertEqual(response.status_code, 200)

    def test_enabled_urls(self):
        """Tests every url in the ENABLED_URLS list against the Middleware."""
        request = RequestFactory()
        request.user = AnonymousUser()

        for enabled_url in ENABLED_URLS:
            # Change the URL of the request
            request.path_info = enabled_url

            # Get the response using the Middleware
            response = self.middleware(request)

            # Assert no redirection
            self.assertEqual(response.status_code, 200)

    def test_admin_url(self):
        """Tests an admin url against the Middleware."""
        request = RequestFactory()
        request.user = AnonymousUser()

        # Change the URL of the request
        request.path_info = "admin"

        # Get the response using the Middleware
        response = self.middleware(request)

        # Assert no redirection
        self.assertEqual(response.status_code, 200)

    def test_url_ending_with_slash(self):
        """Tests an url ending with a slash against the Middleware."""
        request = RequestFactory()
        request.user = AnonymousUser()

        # Change the URL of the request
        request.path_info = "chat/"

        # Get the response using the Middleware
        response = self.middleware(request)

        # Assert no redirection
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login?next=/chat/")

    def test_wrong_url(self):
        """Tests a wrong url against the Middleware."""
        request = RequestFactory()
        request.user = AnonymousUser()

        # Change the URL of the request
        request.path_info = "sad/"

        # Get the response using the Middleware
        response = self.middleware(request)

        # Assert no redirection
        self.assertEqual(response.status_code, 200)


class ProfanityValidatorTestCase(TestCase):
    """Tests for validate_profanity validator."""

    def test_empty_string(self):
        """Tests if the string is empty."""

        # Just call the validator
        validate_profanity("")

    def test_a_string(self):
        """Tests if the string is "a"."""

        # Just call the validator
        validate_profanity("a")

    def test_string_ends_with_a(self):
        """Tests if the string ends with "a"."""

        # Just call the validator
        validate_profanity("Walk a")

    def test_normal(self):
        """Tests a normal string."""

        # Just call the validator
        validate_profanity("Walk my dog")
