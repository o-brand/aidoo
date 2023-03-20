from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from Aidoo.utils import create_date_string
from Aidoo.validators import validate_profanity


# Get actual user model.
User = get_user_model()


class ProfileEditForm(ModelForm):
    """It is used to edit details in a user profile."""

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
            }
        ),
    )

    biography = forms.CharField(
        max_length=250,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Biography",
                "class": "form-control",
                "rows": 5,
            }
        ),
        validators=[validate_profanity],
    )

    profile_picture = forms.ImageField(
        label = "Upload your new profile picture.",
        widget = forms.FileInput,
        required = False,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "biography",
            "profile_picture",
        ]
