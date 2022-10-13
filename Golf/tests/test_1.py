from django.test import TestCase
from django.contrib.auth.models import User


class LoginTestCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'golf',
            'password': 'TeamGolf2022'
        }
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

class DatabaseTestCase(TestCase):
    pass

class WebsiteReachableCase(TestCase):
    pass
