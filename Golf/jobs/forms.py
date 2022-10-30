from dataclasses import Field
from pickletools import UP_TO_NEWLINE
from time import time
from unittest.util import _MAX_LENGTH
from wsgiref.handlers import format_date_time
from django import forms
from django.forms import ModelForm
from django import forms
from .models import JobPosting
from django.forms.widgets import NumberInput
import datetime


# as you create a model for the form 
    #not sure, since we have a model for the DB, but no model for the login - which is more similar)

#bot possibly add a model to you would build the form upon

#create a form
class JobForm(ModelForm):
    first_name = forms.CharField(
        max_length=50, 
        widget = forms.TextInput(attrs= {   'placeholder' : 'First Name', 
                                            'class' : 'form-control'}), 
        label = 'First Name',
        required= True)


    last_name = forms.CharField(
        max_length=50, 
        widget = forms.TextInput(attrs= { 'placeholder' : 'Last Name', 
                                          'class' : 'form-control'}), 
        label = 'Last Name',
         required= True) 
    job_title = forms.CharField(
        max_length=50, 
        widget = forms.TextInput(attrs= { 'placeholder' : 'Job title', 
                                          'class' : 'form-control'}), 
        label = 'Job title', 
        required= True)
    job_short_description = forms.CharField(
        max_length=150, 
        widget = forms.TextInput(attrs= {'placeholder' : 'Job short description', 
                                         'class' : 'form-control'}), 
        label = 'Job short description', 
        required= True)
    
    job_long_description = forms.CharField(
        max_length=400, 
        widget = forms.TextInput(attrs= {'placeholder' : 'Give a short outline of the specifics for the job', 
                                         'class' : 'form-control'}), 
        label = 'Job description', 
        required= True)
    
    location = forms.CharField(
        max_length=7, 
        widget = forms.TextInput(attrs= {'placeholder' : 'Location', 
                                         'class' : 'form-control'}), 
        label = 'ZIP code', 
        required= True)
    
    posting_time = forms.DateTimeField(
        widget = NumberInput(attrs = {'type': 'date', 
                                      'placeholder' : '', 
                                      'class' : 'form-control'}), 
        initial = datetime.date.today, 
        required= True)
    
    points = forms.CharField(
        max_length=3, 
        widget = forms.TextInput(attrs= {'placeholder' : 'Points', 
                                         'class' : 'form-control'}), 
        label = 'Points awarded', 
        required= True)
    #points = forms.DecimalField(max_digits=3, widget = forms.TextInput(), label = 'Points awarded', required= True)
    
    duration = forms.DurationField(
        widget= forms.TextInput(attrs={ 'placeholder': 'time expected', 
                                        'clas' : 'form-control'}), 
        required= True)


    class Meta:         
        model = JobPosting
        #fields = '__all__'
        fields = ['first_name', 'last_name', 'job_title', 'job_short_description', 'job_long_description', 'location', 'posting_time', 'points', 'duration']