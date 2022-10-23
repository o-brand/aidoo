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
            'username': 'asd',
            'password': 'asd123'
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


class SignupTestCase(TestCase):
    
    def test_signuppage(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_view_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login/signup.html')

    def test_signup(self):
        response = self.client.post(reverse('signup'), data={
            'username': 'madeupuser',
            'password1': 'madeuppassword',
            'password2': 'madeuppassword'
        })

        self.assertEqual(response.status_code, 302)

