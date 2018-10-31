from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomerCreationForm(UserCreationForm):
    contact_number = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'contact_number']
