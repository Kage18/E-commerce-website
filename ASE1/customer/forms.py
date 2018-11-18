from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from customer.models import CustomerProfile


class Contact_Form(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ('phone_number', 'address')


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class CustomerCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password Here ...'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password ...'}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password mismatch')
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.get(email=email)
        if user:
            raise forms.ValidationError('Email Already Exists')
        return user
