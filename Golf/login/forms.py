from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from Golf.utils import create_date_string
from .validators import validate_dob
from profanity.validators import validate_is_profane


# Get actual user model.
User = get_user_model()


class RegisterForm(UserCreationForm):
    """It is used to register a user."""

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control",
            }
        ),
        validators=[validate_is_profane],
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control",
            }
        ),
        validators=[validate_is_profane],
    )

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
            }
        ),
        validators=[validate_is_profane],
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
            }
        ),
    )

    password1 = forms.CharField(
        max_length=50,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
            }
        ),
    )

    password2 = forms.CharField(
        max_length=50,
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control",
            }
        ),
    )

    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "min": create_date_string(100),
                "max": create_date_string(13),
            }
        ),
        validators=[validate_dob],
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "date_of_birth",
        ]
