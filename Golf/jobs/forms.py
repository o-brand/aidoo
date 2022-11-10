from dataclasses import Field
from time import time
from django import forms
from django.forms import ModelForm
from .models import JobPosting
from django.forms.widgets import NumberInput
import datetime
from django.core.validators import RegexValidator

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
            attrs={'class': 'form-control', 'placeholder': 'MM/DD/YYYY', 'style': 'width: auto; display: initial;'},
        ),
        label="Deadline",
        required=False
    )

    class Meta:
        model = JobPosting
        fields = ['job_title','job_short_description','job_description','location','points','deadline','poster_id']
