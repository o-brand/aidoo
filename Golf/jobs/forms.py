from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator
from Golf.utils import create_date_string
from Golf.validators import validate_profanity
from .validators import validate_deadline
from .models import Job


class JobForm(ModelForm):
    """It is used to post a job."""

    job_title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Job title",
                "class": "form-control",
            }
        ),
        label="Job title",
        validators=[validate_profanity],
    )

    job_description = forms.CharField(
        max_length=1000,
        min_length=50,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Give a short outline of the specifics for the job",
                "class": "form-control",
                "rows": 5,
            }
        ),
        label="Job description",
        validators=[validate_profanity],
    )

    location = forms.CharField(
        max_length=8,
        widget=forms.TextInput(
            attrs={
                "placeholder": "ZIP code",
                "class": "form-control",
            }
        ),
        validators=[
            RegexValidator(
                "^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$",
                message="The postcode format is not valid. You must use capital letters.",
            )
        ],
        label="ZIP code",
    )

    # Fields to display a dropdown for the duration of the job
    half_hours = [(hhour, hhour) for hhour in range(0, 31, 30)]
    hours = [(hour, hour) for hour in range(1, 9)]
    duration_hours = forms.DecimalField(
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "style":"width: auto; display: initial;",
            },
            choices=hours,
        ),
    )
    duration_half_hours = forms.DecimalField(
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "style": "width: auto; display: initial;",
            },
            choices=half_hours,
        ),
    )

    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "min": create_date_string(0),
                "max": create_date_string(-1),  # 1 year in the future
                "style": "width: auto; display: initial;",
            },
        ),
        label="The deadline to complete the job (optional)",
        required=False,
        validators=[validate_deadline],
    )

    class Meta:
        model = Job
        fields = [
            "job_title",
            "job_description",
            "location",
            "duration_hours",
            "duration_half_hours",
            "deadline",
            "poster_id",
        ]
