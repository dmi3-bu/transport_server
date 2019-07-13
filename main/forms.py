from django import forms
from .models import User


class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    passport = forms.CharField(max_length=10)
    middle_name = forms.CharField(max_length=50)
    date_of_birth = forms.DateField()
    phone = forms.CharField(max_length=10)
    password = forms.CharField(max_length=30)


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=30)
