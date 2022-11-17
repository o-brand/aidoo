from django.test import RequestFactory, TestCase
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from .middlewares import LoginRequiredMiddleware, ENABLED_URLS


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
        self.assertEqual(response.url, "/login/?next=/jobs/post")

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
