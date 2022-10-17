from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class LoginTestCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'golf',
            'password': 'TeamGolf2022'
        }
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

    def test_login_available_by_name(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
