from dataclasses import Field
from pickletools import UP_TO_NEWLINE
from time import time
from unittest.util import _MAX_LENGTH
from wsgiref.handlers import format_date_time
from django import forms
from django.forms import ModelForm
from django import forms
from .models import JobPosting


# as you create a model for the form 
    #not sure, since we have a model for the DB, but no model for the login - which is more similar)

#bot possibly add a model to you would build the form upon

#create a form
class JobForm(ModelForm):
    first_name = forms.CharField(max_length=50, widget = forms.TextInput(), label = 'First name', required= False)
    last_name = forms.CharField(max_length=50, widget = forms.TextInput(), label = 'Last Name', required= False)
    job_title = forms.CharField(max_length=50, widget = forms.TextInput(), label = 'Job title', required= False)
    job_short_desc = forms.CharField(max_length=150, widget = forms.TextInput(), label = 'List required skills', required= False)
    job_long_desc = forms.CharField(max_length=400, widget = forms.TextInput(), label = 'Give a short outline of the specifics for the job', required= False)
    location = forms.CharField(max_length=7, widget = forms.TextInput(), label = 'ZIP code', required= False)
    date = forms.DateTimeField(widget = forms.TextInput(), required= False)
    duration = forms.DurationField(widget= forms.TextInput(), required= False)


    class Meta:  #don't know why, just include, it's a Django thing
        model = JobPosting
        fields = ['first_name',]
        
        #'duration' - but add models for it