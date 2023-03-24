import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from Aidoo.utils import create_date_string
from .forms import RegisterForm
from .validators import validate_dob, validate_username
from .views import activateAccount


# Get actual user model.
User = get_user_model()


class WelcomeTestCase(TestCase):
    """Tests for Welcome page."""

    def test_welcome(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="welcome.html")

    def test_welcome_available_by_name(self):
        response = self.client.get(reverse("welcome"))
        self.assertEqual(response.status_code, 200)

    def test_redirect(self):
        credentials = {
            "username": "asd",
            "password": "asd123",
            "date_of_birth": datetime.datetime.now(),
            "profile_id": "media/profilepics/default",
        }
        user = User.objects.create_user(**credentials)
        self.client.post("/login", credentials, follow=True)

        response = self.client.get(reverse("welcome"))
        self.assertEqual(response.status_code, 302)


class LoginTestCase(TestCase):
    """Tests for the login and the logout page"""

    def test_login(self):
        credentials = {
            "username": "asd",
            "password": "asd123",
            "date_of_birth": datetime.datetime.now(),
            "profile_id": "media/profilepics/default",
        }
        User.objects.create_user(**credentials)

        response = self.client.post("/login", credentials, follow=True)
        self.assertTrue(response.context["user"].is_active)

    def test_login_available_by_name(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="login/login.html")

    def test_logout(self):
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_logout_available_by_name(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


class SignupTestCase(TestCase):
    """Tests for the signup page."""

    # test if the signup page is reachable and uses the right template
    def test_signup(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, 200)

    def test_signup_available_by_name(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="login/signup.html")

    # test if signing up works if not correct data given
    def test_signup_flow_not_correct(self):
        upload_file = open('../fortest.jpeg', 'rb')
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "",
            "username": "madeupuser",
            "biography": "hey",
            "password1": "madeuppassword",
            "password2": "madeuppassword",
            "date_of_birth": datetime.date(2000, 1, 1),
            "profile_id": SimpleUploadedFile(upload_file.name, upload_file.read())
        }
        response = self.client.post(reverse("signup"), data=new_user)
        self.assertEqual(response.status_code, 200)

        # Test that no message has been sent.
        self.assertEqual(len(mail.outbox), 0)

    # test if signing up works if correct data given and user is redirected after
    def test_signup_flow(self):
        upload_file = open('../fortest.jpeg', 'rb')
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "madeupuser@madeupuser.com",
            "username": "madeupuser",
            "biography": "hey",
            "password1": "madeuppassword",
            "password2": "madeuppassword",
            "date_of_birth": datetime.date(2000, 1, 1),
            "profile_id": SimpleUploadedFile(upload_file.name, upload_file.read())
        }
        response = self.client.post(reverse("signup"), data=new_user)

        # After the user registered, the activation template should be used
        self.assertTemplateUsed(
            response, template_name="login/activation_link_sent.html"
        )
        self.assertEqual(response.status_code, 200)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)


class PasswordResetTestCase(TestCase):
    """Tests for resetting a password."""

    def test_password_reset_page(self):
        response = self.client.get("/password_reset")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_page_available_by_name(self):
        response = self.client.get(reverse("password_reset_form"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="login/password_reset_form.html"
        )

    def test_password_reset_sent_page(self):
        response = self.client.get("/password_reset/sent")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_sent_page_available_by_name(self):
        response = self.client.get(reverse("password_reset_done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="login/password_reset_sent.html"
        )

    def test_password_reset_complete_page(self):
        response = self.client.get("/password_reset/complete")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_page_available_by_name(self):
        response = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="login/password_reset_complete.html"
        )

    def test_password_reset_confirm_page_available_by_name(self):
        # The default Django view is used, so there is no need for more tests.
        response = self.client.get("/password_reset/<uidb64>/<token>")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="login/password_reset_confirm.html"
        )


class ActivationTestCase(TestCase):
    """Tests for account activation pages."""

    def setUp(self):
        # Create a user.
        credentials = {
            "username": "asd",
            "password": "asd123",
            "date_of_birth": datetime.datetime.now(),
            "profile_id": "media/profilepics/default",
        }
        self.user = User.objects.create_user(**credentials)

        tokengenerator = PasswordResetTokenGenerator()

        # Create a valid token
        self.token = tokengenerator.make_token(self.user)

    def test_activation_success_page(self):
        response = self.client.get("/activation/success")
        self.assertEqual(response.status_code, 200)

    def test_activation_success_page_available_by_name(self):
        response = self.client.get(reverse("activation_success"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            template_name="login/activation_success.html")

    def test_activation_failure_page(self):
        response = self.client.get("/activation/failure")
        self.assertEqual(response.status_code, 200)

    def test_activation_failure_page_available_by_name(self):
        response = self.client.get(reverse("activation_failure"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            template_name="login/activation_failure.html")

    def test_activation_successful(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        request = HttpRequest()

        response = activateAccount(request, uid, self.token)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/activation/success")

    def test_activiation_failure(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        request = HttpRequest()

        response = activateAccount(request, uid, "self.token")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/activation/failure")

    def test_activiation_failure_uid(self):
        uid = urlsafe_base64_encode(force_bytes('2'))

        request = HttpRequest()

        response = activateAccount(request, uid, self.token)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/activation/failure")


class RegisterFormTestCase(TestCase):
    """Tests for RegisterForm."""
    # PasswordInput is already tested well, so we do not test it here.

    def setUp(self):
        self.upload_file = open('../fortest.jpeg', 'rb')
        self.file_dict = {
            "profile_id": SimpleUploadedFile(self.upload_file.name, self.upload_file.read(), content_type='image/jpeg')
        }

    def test_nothing_entered(self):
        # behaviour if form is empty
        form = RegisterForm(data={})

        self.assertEqual(9, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required.", form.errors[key][0])

    def test_name_entered(self):
        # behaviour if full name is entered and valid
        # there should be less errors thrown
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
        }
        form = RegisterForm(new_user, self.file_dict)

        # Name must be ok
        self.assertEqual(6, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required.", form.errors[key][0])

    def test_name_username_entered_username_too_long(self):
        # behaviour if the username entered is too long and name is correct
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "username": "a" * 101,
        }
        form = RegisterForm(new_user, self.file_dict)

        # Name must be ok
        self.assertEqual(6, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == "username":
                self.assertIn(
                    "Ensure this value has at most 100 characters (it has 101).",
                    form.errors[key][0],
                )
            else:
                self.assertIn("This field is required.", form.errors[key][0])

    def test_name_username_entered(self):
        # behaviour if username and name are valid, rest invalid
        # num of errors must match the num of required fields not filled
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "username": "madeupuser",
        }
        form = RegisterForm(new_user, self.file_dict)

        # Name, username must be ok
        self.assertEqual(5, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required.", form.errors[key][0])

    def test_name_username_email_entered_email_not_valid(self):
        # behaviour if entered email is not valid
        # other entered fields are valid
        # the expected error message should be the response
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "madeupusermadeupuser.com",
            "username": "madeupuser",
        }
        form = RegisterForm(new_user, self.file_dict)

        # Name, username must be ok
        self.assertEqual(5, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == "email":
                self.assertIn(
                    "Enter a valid email address.",
                    form.errors[key][0],
                )
            else:
                self.assertIn("This field is required.", form.errors[key][0])

    def test_name_username_email_entered(self):
        # behaviour if the email is valid
        # the number of errors should be the number of empty required fields
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "madeupuser@madeupuser.com",
            "username": "madeupuser",
        }
        form = RegisterForm(new_user, self.file_dict)

        # Name, email, username must be ok
        self.assertEqual(4, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required.", form.errors[key][0])

    def test_name_username_email_passwords_entered_passwords_not_match(self):
        # behaviour repeated passphrase does not match original one
        # should give the expected error message
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "madeupuser@madeupuser.com",
            "username": "madeupuser",
            "biography": "hey",
            "password1": "madeuppassword",
            "password2": "madeuppassword2",
        }
        form = RegisterForm(new_user, self.file_dict)

        # Name, email, username must be ok
        self.assertEqual(2, len(form.errors))

        self.assertIn(
            "The two password fields didn’t match.",
            form.errors["password2"][0],
        )

    def test_name_username_email_passwords_entered_(self):
        #test if all fields are entered and valid
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "madeupuser@madeupuser.com",
            "username": "madeupuser",
            "biography": "hey",
            "password1": "madeuppassword",
            "password2": "madeuppassword",
            "date_of_birth": datetime.date(2000, 1, 1),
        }
        form = RegisterForm(new_user, self.file_dict)
        self.assertEqual(0, len(form.errors))

    def test_DoB_out_of_range_too_young(self):
        #behaviour if user is too young
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "madeupuser@madeupuser.com",
            "username": "madeupuser",
            "biography": "hey",
            "password1": "madeuppassword",
            "password2": "madeuppassword",
            "date_of_birth": create_date_string(0),
        }
        form = RegisterForm(new_user, self.file_dict)
        self.assertEqual(1, len(form.errors))

    def test_DoB_out_of_range_too_old(self):
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "madeupuser@madeupuser.com",
            "username": "madeupuser",
            "biography": "hey",
            "password1": "madeuppassword",
            "password2": "madeuppassword",
            "date_of_birth": create_date_string(123),
        }
        form = RegisterForm(new_user, self.file_dict)
        self.assertEqual(1, len(form.errors))

    def test_profane_first_name(self):
        new_user = {
            "first_name": "kondums",
            "last_name": "MadeUp",
            "email": "madeupuser@madeupuser.com",
            "username": "madeupuser",
            "biography": "hey",
            "password1": "madeuppassword",
            "password2": "madeuppassword",
            "date_of_birth": datetime.date(2000, 1, 1),
        }
        form = RegisterForm(new_user, self.file_dict)
        self.assertEqual(1, len(form.errors))

    def test_profane_last_name(self):
        new_user = {
            "first_name": "User",
            "last_name": "kondums",
            "email": "madeupuser@madeupuser.com",
            "username": "madeupuser",
            "biography": "hey",
            "password1": "madeuppassword",
            "password2": "madeuppassword",
            "date_of_birth": datetime.date(2000, 1, 1),
        }
        form = RegisterForm(new_user, self.file_dict)
        self.assertEqual(1, len(form.errors))

    def test_profane_username(self):
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "madeupuser@madeupuser.com",
            "username": "kondums",
            "biography": "hey",
            "password1": "madeuppassword",
            "password2": "madeuppassword",
            "date_of_birth": datetime.date(2000, 1, 1),
        }
        form = RegisterForm(new_user, self.file_dict)
        self.assertEqual(1, len(form.errors))

    def test_image(self):
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "madeupuser@madeupuser.com",
            "username": "madeupuser",
            "biography": "hey",
            "password1": "madeuppassword",
            "password2": "madeuppassword",
            "date_of_birth": datetime.date(2000, 1, 1),
        }
        form = RegisterForm(new_user)
        self.assertEqual(1, len(form.errors))

    def test_biography(self):
        new_user = {
            "first_name": "User",
            "last_name": "MadeUp",
            "email": "madeupuser@madeupuser.com",
            "username": "madeupuser",
            "password1": "madeuppassword",
            "password2": "madeuppassword",
            "date_of_birth": datetime.date(2000, 1, 1),
        }
        form = RegisterForm(new_user, self.file_dict)
        self.assertEqual(1, len(form.errors))


class ValidatorsTestCase(TestCase):

    def test_validate_dob(self):
        """Test the validate_dob function."""
        # Test invalid dates.
        with self.assertRaises(ValidationError):
            validate_dob(datetime.datetime.strptime("2022-02-19",
                "%Y-%m-%d").date())  # Too young.
        with self.assertRaises(ValidationError):
            validate_dob(datetime.datetime.strptime("1910-02-19",
                "%Y-%m-%d").date())  # Too old.

        # Test valid dates.
        self.assertIsNone(validate_dob(datetime.datetime.strptime("1990-02-19",
            "%Y-%m-%d").date()))
        self.assertIsNone(validate_dob(datetime.datetime.strptime("2005-02-19",
            "%Y-%m-%d").date()))

    def test_validate_username(self):
        """Test the validate_username function."""
        # Test the invalid username.
        with self.assertRaises(ValidationError):
            validate_username("default")

        # Test a valid username.
        self.assertIsNone(validate_username("asdasd"))
