from django.test import TestCase
from django.urls import reverse
from vendor.models import Category
from cart.models import *


class AddTOCartTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        category = Category.objects.create(cat_name='Groceries')
        Product.objects.create(category=category, prod_name='test_product', cost=100, stock=100)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('cart:add_to_cart', kwargs={'prod_id': 1}))
        self.assertRedirects(response, '/customer/authentication/login/?next=/cart/add-to-cart/1/')

    # def test_logged_in_uses_correct_template(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse('cart:add_to_cart', kwargs={'prod_id': 1}),data={'vendorid':})
    #     self.assertEqual(response.status_code, 200)


class DeleteFromCart(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='mypassword')
        test_user.save()
        category = Category.objects.create(cat_name='Groceries')
        product = Product.objects.create(category=category, prod_name='test_product', cost=100, stock=100)
        order_item = OrderItem.objects.create(product=product, ref_code='abcd1234')
        order_item.vendor.add(test_user)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('cart:delete_from_cart', kwargs={'item_id': 1}))
        self.assertRedirects(response, '/customer/authentication/login/?next=/cart/delete-from-cart/1/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='mypassword')
        response = self.client.get(reverse('cart:delete_from_cart', kwargs={'item_id': 1}))
        self.assertRedirects(response, reverse('cart:order_summary'))


class OrderDetailsTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='mypassword')
        test_user.save()
        category = Category.objects.create(cat_name='Groceries')
        product = Product.objects.create(category=category, prod_name='test_product', cost=100, stock=100)
        order_item = OrderItem.objects.create(product=product, ref_code='abcd1234')
        order_item.vendor.add(test_user)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('cart:order_summary'))
        self.assertRedirects(response, '/customer/authentication/login/?next=/cart/order-summary/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='mypassword')
        response = self.client.get(reverse('cart:order_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/order_summary.html')


class CheckoutTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='mypassword')
        test_user.save()
        category = Category.objects.create(cat_name='Groceries')
        product = Product.objects.create(category=category, prod_name='test_product', cost=100, stock=100)
        order_item = OrderItem.objects.create(product=product, ref_code='abcd1234')
        order_item.vendor.add(test_user)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('cart:checkout'))
        self.assertRedirects(response, '/customer/authentication/login/?next=/cart/checkout/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='mypassword')
        response = self.client.get(reverse('cart:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/checkout.html')


class UpdateTransactionsTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='mypassword')
        test_user.save()
        category = Category.objects.create(cat_name='Groceries')
        product = Product.objects.create(category=category, prod_name='test_product', cost=100, stock=100)
        order_item = OrderItem.objects.create(product=product, ref_code='abcd1234')
        order_item.vendor.add(test_user)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('cart:update'))
        self.assertRedirects(response, '/customer/authentication/login/?next=/cart/update_transaction_records/')

    # def test_logged_in_uses_correct_template(self):
    #     login = self.client.login(username='testuser', password='mypassword')
    #     order_item = OrderItem.objects.get(id=1)
    #     order_item.is_ordered = True
    #     response = self.client.get(reverse('cart:update'))
    #     self.assertRedirects(response, reverse('customer:profile')
