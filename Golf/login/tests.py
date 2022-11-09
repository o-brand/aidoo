from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegisterForm
import datetime

class WelcomeTestCase(TestCase):

    def test_welcome(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='welcome.html')

    def test_welcome_available_by_name(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)


class LoginTestCase(TestCase):

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
        self.assertTemplateUsed(response, template_name='login/login.html')

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
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'email': "madeupuser@madeupuser.com",
            'username': 'madeupuser',
            'password1': 'madeuppassword',
            'password2': 'madeuppassword',
            'date_of_birth':datetime.date(2000,1,1)
        }
        response = self.client.post(reverse('signup'), data=new_user)

        self.assertEqual(response.status_code, 302)


class RegisterFormTestCase(TestCase):
    # I think PasswordInput is already tested well, so I do not test it here.

    def test_nothing_entered(self):
        form = RegisterForm(data={})

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_name_entered(self):
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(4, len(form.errors)) # Name must be ok

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_name_username_entered_username_too_long(self):
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'username': 'a' * 101,
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(4, len(form.errors)) # Name must be ok

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == 'username':
                self.assertIn('Ensure this value has at most 100 characters (it has 101).', form.errors[key][0])

            else:
                self.assertIn('This field is required.', form.errors[key][0])

    def test_name_username_entered(self):
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'username': 'madeupuser',
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(3, len(form.errors)) # Name, username must be ok

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_name_username_email_entered_email_not_valid(self):
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'email': "madeupusermadeupuser.com",
            'username': 'madeupuser',
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(3, len(form.errors)) # Name, username must be ok

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == 'email':
                self.assertIn('Enter a valid email address.', form.errors[key][0])
            else:
                self.assertIn('This field is required.', form.errors[key][0])

    def test_name_username_email_entered(self):
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'email': "madeupuser@madeupuser.com",
            'username': 'madeupuser',
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(2, len(form.errors)) # Name, email, username must be ok

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_name_username_email_passwords_entered_passwords_not_match(self):
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'email': "madeupuser@madeupuser.com",
            'username': 'madeupuser',
            'password1': 'madeuppassword',
            'password2': 'madeuppassword2'
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(1, len(form.errors)) # Name, email, username must be ok
        self.assertIn('The two password fields didn’t match.', form.errors['password2'][0])

    def test_name_username_email_passwords_entered_(self):
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'email': "madeupuser@madeupuser.com",
            'username': 'madeupuser',
            'password1': 'madeuppassword',
            'password2': 'madeuppassword'
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(0, len(form.errors))


class PasswordResetTestCase(TestCase):

    def test_password_reset_page(self):
        response = self.client.get('/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_page_view_name(self):
        response = self.client.get(reverse('password_reset_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login/password_reset_form.html')

    def test_password_reset_done_page(self):
        response = self.client.get('/password_reset/done')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_page_view_name(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login/password_reset_done.html')

    def test_password_reset_complete_page(self):
        response = self.client.get('/password_reset/complete')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_page_view_name(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login/password_reset_complete.html')

    def test_password_reset_confirm_page(self):
        response = self.client.get('/password_reset/<uidb64>/<token>')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login/password_reset_confirm.html')
