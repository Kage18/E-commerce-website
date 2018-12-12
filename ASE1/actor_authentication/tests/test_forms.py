from django.test import TestCase
from actor_authentication.forms import UserCreationForm, UserLoginForm


class SignUpFormTest(TestCase):

    def test_login_details(self):
        form = UserLoginForm(data={'username': 'jitesh@!@#123', 'password': 'hsdfkaew8r480234@#'})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['password'].label == 'Password')
