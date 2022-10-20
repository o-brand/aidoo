from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class LoginTestCase(TestCase):

    def test_welcome(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_welcome_available_by_name(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        credentials = {
            'username': 'golf',
            'password': 'TeamGolf2022'
        }
        User.objects.create_user(**credentials)

        response = self.client.post('/login/', credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_login_available_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_logout_available_by_name(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
