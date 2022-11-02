from tkinter import Widget
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from jobs.models import UserExtended
from datetime import datetime
from datetime import timedelta
from django.forms import ModelForm

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

class RegisterFormExtended(forms.ModelForm):
    

    #variables used for dynamic date time
    date_range = 100    
    this_year = datetime.now().year

    date_of_birth = forms.DateField(
        required=True,
        label="Date of Birth",
        initial=(datetime.now() - timedelta(days=365)),
        widget=forms.SelectDateWidget(
            years=range(this_year - date_range, this_year),
            ),
        
    )


    class Meta:
        model = UserExtended
        fields = ['date_of_birth']
