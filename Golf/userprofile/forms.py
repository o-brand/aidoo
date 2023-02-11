from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator
from .models import User

class AccountSettingsForm(ModelForm):
    """It is used to change a users account settings."""

    opt_in_emails = forms.BooleanField(
        label="Recieve emails",
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "opt_in_emails",
        ]
