from dataclasses import Field
from time import time
from _datetime import datetime
from django import forms
from django.forms import ModelForm
from django.forms.widgets import NumberInput
from django.core.validators import RegexValidator
from .validators import validate_deadline
from Golf.utils import create_date_string
from .models import Job


# Form for posting a Job
class JobForm(ModelForm):
    job_title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={'placeholder': 'Job title', 'class': 'form-control'}
        ),
        label='Job title',
        required=True,
    )

    job_short_description = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={'placeholder': 'Job short description', 'class': 'form-control'}
        ),
        label='Job short description',
        required=True,
    )

    job_description = forms.CharField(
        max_length=1000,
        min_length=50,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Give a short outline of the specifics for the job',
                'class': 'form-control',
                'rows': 5,
            }
        ),
        label='Job description',
        required=True,
    )

    location = forms.CharField(
        max_length=8,
        widget=forms.TextInput(
            attrs={'placeholder': 'ZIP code', 'class': 'form-control'}
        ),
        validators=[
            RegexValidator(
                '^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$',
                message='The postcode format is not valid. You must use capital letters.',
            )
        ],
        label='ZIP code',
        required=True,
    )

    days = [(day, day) for day in range(0, 15)]
    hours = [(hour, hour) for hour in range(1, 25)]

    duration_days = forms.DecimalField(
        widget=forms.Select(
            attrs={'class': 'form-control', 'style': 'width: auto; display: initial;'},
            choices=days,
        ),
        required=True,
    )
    duration_hours = forms.DecimalField(
        widget=forms.Select(
            attrs={'class': 'form-control', 'style': 'width: auto; display: initial;'},
            choices=hours,
        ),
        required=True,
    )

    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date',
                'class': 'form-control',
                "min":create_date_string(0),
                "max":create_date_string(-1), # 1 year in the future
                'style': 'width: auto; display: initial;'},
        ),
        label="The deadline to complete the job (optional)",
        required=False,
        validators=[validate_deadline],
    )

    class Meta:
        model = Job
        fields = ['job_title', 'job_short_description', 'job_description', 'location', 'duration_days', 'duration_hours','deadline','poster_id']
