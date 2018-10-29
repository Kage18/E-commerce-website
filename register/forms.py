from django import forms
from django.contrib.auth.models import User
from register.models import Registermodel

class LoginForm(forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')

class RegisterForm(forms.ModelForm):
    class Meta():
        model = Registermodel
        fields = ('first_name','last_name','date_of_birth')
