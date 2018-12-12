from django.test import TestCase
from django.urls import reverse
from vendor.models import Product, Category


class ProductListView(TestCase):
    def setUp(self):
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
