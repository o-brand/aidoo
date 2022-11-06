from tkinter import Widget
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from jobs.models import UserExtended
from datetime import datetime

# This class extends the UserCreationForm to have extra fields.
# We can customize the error messages later, if we want.

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control",
            }
        ),
    )

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
            }
        ),
    )

    password1 = forms.CharField(
        max_length=50,
        required=True,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
            }
        ),
    )

    password2 = forms.CharField(
        max_length=50,
        required=True,
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class DateInput(forms.DateInput):
    input_type = 'date'
    

#Additional form required for the date of birth field. This form is an extension of the UserExtended model
#from jobs.models
class RegisterFormExtended(forms.ModelForm):

    class Meta:
    
        model = UserExtended
        fields = ['date_of_birth']
        widgets={
            'date_of_birth': DateInput(attrs={"min":str(datetime.now().year - 100)+"-01-01",
                "max":str(datetime.now().year - 13)+"-"+str("{:02d}".format(datetime.now().month))+"-"+str("{:02d}".format(datetime.now().day))}
                ),
        }
