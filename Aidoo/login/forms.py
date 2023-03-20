from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from Aidoo.utils import create_date_string
from Aidoo.validators import validate_profanity
from .validators import validate_dob, validate_username



# Get actual user model.
User = get_user_model()


class RegisterForm(UserCreationForm):
    """It is used to register a user."""

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control",
            }
        ),
        validators=[validate_profanity],
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control",
            }
        ),
        validators=[validate_profanity],
    )

    biography = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Biography",
                "class": "form-control",
            }
        ),
        validators=[validate_profanity],
    )

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
            }
        ),
        validators=[validate_profanity, validate_username],
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

    profile_id = forms.ImageField(
        label="Please upload an image of an ID",
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "biography",
            "username",
            "email",
            "password1",
            "password2",
            "date_of_birth",
            "profile_id",
        ]
