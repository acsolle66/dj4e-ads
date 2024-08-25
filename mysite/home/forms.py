from django.forms import ModelForm
from django.forms import Form
from django import forms
from django.contrib.auth import get_user_model


class LoginForm(Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
