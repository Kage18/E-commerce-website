from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserCreationForm(forms.ModelForm):
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

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email):
    #         raise forms.ValidationError('Email Already Exists')
    #     return email

# class UserEditForm(forms.ModelForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
#     email = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'first_name',
#             'last_name',
#             'email',
#         )
#
# class ProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         exclude = ('user',)
