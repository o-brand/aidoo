from django.test import RequestFactory, TestCase
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from .middlewares import LoginRequiredMiddleware, ENABLED_URLS
from django.contrib.auth import get_user_model

User = get_user_model() # Get user model

def dummy_middleware(request):
    response = HttpResponse()
    response.status_code = 200
    return response

class LoginRequiredMiddlewareTestCase(TestCase):

    def setUp(self):
        self.middleware = LoginRequiredMiddleware(dummy_middleware)

    def test_user_not_logged_id(self):
        request = RequestFactory()
        request.user = AnonymousUser()
        request.path_info = '/jobs/post'

        response = self.middleware(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/jobs/post")

    def test_user_logged_id(self):
        request = RequestFactory()
        request.user = User()
        request.path_info = '/jobs/post'

        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)

    def test_enabled_urls(self):
        request = RequestFactory()
        request.user = AnonymousUser()

        for enabled_url in ENABLED_URLS:

            request.path_info = enabled_url

            response = self.middleware(request)
            self.assertEqual(response.status_code, 200)
