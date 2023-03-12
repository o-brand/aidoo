from django import forms
from django.forms import ModelForm, Form
from .models import Transfer, Sale
from .validators import validate_recipient
from Golf.validators import validate_profanity


class BuyForm(Form):
    """Form to buy an item"""

    def __init__(self, choices, *args, **kwargs):
        super(BuyForm, self).__init__(*args, **kwargs)
        self.fields["quantity"].choices = [(f"{x}", f"{x}") for x in choices]

    quantity = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "style": "width: auto; display: initial;",
            }
        ),
        required=True,
        label="Quantity",
    )


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
                "style": "width: auto; display: initial;",
            },
        ),
        label="Amount",
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
        label="Message for recipient (optional)",
        validators=[validate_profanity],
        required=False,
    )

    class Meta:
        model = Transfer
        fields = [
            "amount",
            "note",
        ]
