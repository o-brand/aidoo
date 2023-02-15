from django import forms
from django.forms import ModelForm
from Golf.utils import create_date_string
from .models import Report
"""Report form"""

class ReportForm(ModelForm):
    """Form to report a job post"""

    #WRITE CONSTRAINTS


    complaint = forms.CharField(
    max_length=1000,
    min_length=50,
    widget=forms.Textarea(
            attrs={
            "placeholder": "Explain the reason for reporting",
            "class": "form-control",
            "rows": 5,
        }
    ),
    label="Describe your issue."
    )
    
    class Meta:
        model = Report
        fields = [
            "reported_job",
            "reported_user",
            "reporting_user",
            "complaint",
            "type"
        ]