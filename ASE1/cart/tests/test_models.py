from django.test import TestCase
from cart.models import *
from vendor.models import Category


class OrderItemTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='mypassword')
        category = Category.objects.create(cat_name='Grocery')
        product = Product.objects.create(category=category, prod_name='p1', stock=100, cost=50)
        order_item = OrderItem.objects.create(product=product, ref_code='abcd1234')
        order_item.vendor.add(test_user)

    def test_expected_object(self):
        order_item = OrderItem.objects.get(id=1)
        expected_name = f'{order_item.product.prod_name}'
        self.assertEqual(expected_name, str(order_item))

    def test_max_length(self):
        order_item = OrderItem.objects.get(id=1)
        max_length = order_item._meta.get_field('ref_code').max_length
        self.assertEqual(max_length, 20)


