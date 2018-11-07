from django import forms
from vendor.models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProductsAdd(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

def email_check(user):
    return user.is_vendor

class VendorCreationForm(UserCreationForm):
    contact_number = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'contact_number']
