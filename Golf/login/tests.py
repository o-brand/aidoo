from django.test import TestCase
from django.urls import reverse
from .forms import RegisterForm
import datetime
from django.contrib.auth import get_user_model

User = get_user_model() # Get user model

class WelcomeTestCase(TestCase):
    # test if the welcome page can be reached and uses the right template

    def test_welcome(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='welcome.html')

    def test_welcome_available_by_name(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)


class PrivacyTestCase(TestCase):

    def test_privacy(self):
        response = self.client.get('/privacy/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login/privacy.html')

    def test_privacy_available_by_name(self):
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)


class LoginTestCase(TestCase):
    # test for loging in and logging out
    # can the login page be reached
    # is the user redirected after logging in

    def test_login(self):
        credentials = {
            'username': 'asd',
            'password': 'asd123',
            'date_of_birth':datetime.datetime.now(),
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

    # test if the signup page is reachable and uses the right template
    def test_signuppage(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_view_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login/signup.html')

    # test if signing up works if correct data given and user is redirected after
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
        self.assertTemplateUsed(response, template_name='login/confirm_email.html')


        self.assertEqual(response.status_code, 200)


class RegisterFormTestCase(TestCase):
    # I think PasswordInput is already tested well, so I do not test it here.

    def test_nothing_entered(self):
        # behaviour if form is empty
        form = RegisterForm(data={})

        self.assertEqual(7, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_name_entered(self):
        # behaviour if full name is entered and valid
        # there should be less errors thrown
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(5, len(form.errors)) # Name must be ok

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_name_username_entered_username_too_long(self):
        # behaviour if the username entered is too long and name is correct
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'username': 'a' * 101,
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(5, len(form.errors)) # Name must be ok

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == 'username':
                self.assertIn('Ensure this value has at most 100 characters (it has 101).', form.errors[key][0])

            else:
                self.assertIn('This field is required.', form.errors[key][0])

    def test_name_username_entered(self):
        # behaviour if username and name are valid, rest invalid
        # num of errors must match the num of required fields not filled
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'username': 'madeupuser',
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(4, len(form.errors)) # Name, username must be ok

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_name_username_email_entered_email_not_valid(self):
        # behaviour if entered email is not valid
        # other entered fields are valid
        # the expected error message should be the response
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'email': "madeupusermadeupuser.com",
            'username': 'madeupuser',
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(4, len(form.errors)) # Name, username must be ok

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == 'email':
                self.assertIn('Enter a valid email address.', form.errors[key][0])
            else:
                self.assertIn('This field is required.', form.errors[key][0])

    def test_name_username_email_entered(self):
        # behaviour if the email is valid
        # the number of errors should be the number of empty required fields
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'email': "madeupuser@madeupuser.com",
            'username': 'madeupuser',
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(3, len(form.errors)) # Name, email, username must be ok

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_name_username_email_passwords_entered_passwords_not_match(self):
        # behaviour repeated passphrase does not match original one
        # should give the expected error message
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'email': "madeupuser@madeupuser.com",
            'username': 'madeupuser',
            'password1': 'madeuppassword',
            'password2': 'madeuppassword2',
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(2, len(form.errors)) # Name, email, username must be ok
        self.assertIn('The two password fields didn’t match.', form.errors['password2'][0])

    def test_name_username_email_passwords_entered_(self):
        #test if all fields are entered and valid
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'email': "madeupuser@madeupuser.com",
            'username': 'madeupuser',
            'password1': 'madeuppassword',
            'password2': 'madeuppassword',
            'date_of_birth':datetime.date(2000,1,1),
        }
        form = RegisterForm(data=new_user)

        self.assertEqual(0, len(form.errors))

    def test_DoB_out_of_range(self):
        #behaviour if user is too young
        new_user = {
            'first_name': 'User',
            'last_name': 'MadeUp',
            'email': "madeupuser@madeupuser.com",
            'username': 'madeupuser',
            'password1': 'madeuppassword',
            'password2': 'madeuppassword',
            'date_of_birth':datetime.date.today()
        }

        form = RegisterForm(data=new_user)

        self.assertEqual(1, len(form.errors))


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


class EmailConfirmationTestCase(TestCase):

    # test reachability of page
    def test_email_confirmation_page(self):
        response = self.client.get('/confirm_email/')
        self.assertEqual(response.status_code, 200)

    def test_email_confirmation_page_view_name(self):
        response = self.client.get(reverse('confirm_email'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login/confirm_email.html')

    # test if the confirmation through email is registered by the system
    # and page is displayed for success
    def test_email_confirmation_success_page(self):
        response = self.client.get('/confirm_email/success/')
        self.assertEqual(response.status_code, 200)

    def test_email_confirmation_success_page_view_name(self):
        response = self.client.get(reverse('confirm_email_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login/confirm_email_success.html')

    # test display right page when authentication fails
    # test if page reachable
    def test_email_confirmation_failure_page(self):
        response = self.client.get('/confirm_email/failure/')
        self.assertEqual(response.status_code, 200)

    def test_email_confirmation_failure_page_view_name(self):
        response = self.client.get(reverse('confirm_email_failure'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login/confirm_email_failure.html')
