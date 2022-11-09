from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model() # Get user model

# This class extends the UserCreationForm to have extra fields.
# We can customize the error messages later, if we want.

class DateInput(forms.DateInput):
    input_type = 'date'

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

    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "min":str(datetime.now().year - 100)+"-01-01",
                "max":str(datetime.now().year - 13)+"-"+str("{:02d}".format(datetime.now().month))+"-"+str("{:02d}".format(datetime.now().day))
            }
        ),
    )
 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'date_of_birth']


    
