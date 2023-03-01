from django import forms
from django.forms import ModelForm
from .models import Transfer
from .validators import validate_recipient
from Golf.validators import validate_profanity


class TransferForm(ModelForm):
    """Form to transfer coins"""
    recipient = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "width: auto; display: initial;",
            }
        ),
        max_length=100,
        validators=[validate_recipient],
    )

    amount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "style":"width: auto; display: initial;",
            },
        ),
        label = "Amount",
        min_value=1,
    )

    note = forms.CharField(
    max_length=250,
    widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "rows": 3,
        }
    ),
    label="Message for recipient",
    validators=[validate_profanity],
    )

    class Meta:
        model = Transfer
        fields = [
            "amount",
            "note",
        ]
