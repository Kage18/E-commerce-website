from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from vendor.models import Product, Category


class UserProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='mypassword')
        test_user.save()

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='mypassword')
        response = self.client.get(reverse('customer:profile'))
        self.assertTemplateUsed(response, 'customer/profile.html')


class ItemsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(cat_name='Groceries')
        Product.objects.create(category=category, prod_name='test_product', cost=100, stock=100)

    def test_categories_view(self):
        response = self.client.get(reverse('vendor:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/index.html', 'customer/base.html')

    def test_items_view(self):
        response = self.client.get(reverse('vendor:items', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/items.html')


class SearchResultsTest(TestCase):
    def test_search_results(self):
        response = self.client.get(reverse('customer:search_results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/search_results.html')

