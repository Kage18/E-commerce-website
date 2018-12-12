from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='mypassword')
        test_user.save()

    def test_logged_in(self):
        login = self.client.login(username='testuser', password='mypassword')
        response = self.client.get(reverse('customer:home'))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/index.html', 'customer/base.html')

