import datetime
from django.test import TestCase
from vendor.models import Product, Category, Review, VendorProfile, VendorQty
from django.contrib.auth.models import User


class CategoryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(cat_name='Groceries')

    def test_category_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('cat_name').verbose_name
        self.assertEqual(field_label, 'cat name')

    def test_category_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('cat_name').max_length
        self.assertEqual(max_length, 150)

    def test_category_object_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = f'{category.cat_name}'
        self.assertEqual(expected_object_name, str(category))

    def test_get_absolute_url(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.get_absolute_url(), '/vendor/home/')


class ProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(cat_name='Groceries')
        Product.objects.create(category=category, prod_name='test_prod1', cost=50)

    def test_prod_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('prod_name').verbose_name
        self.assertEqual(field_label, 'prod name')

    def test_prod_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('prod_name').max_length
        self.assertEqual(max_length, 150)

    def test_prod_object_name(self):
        product = Product.objects.get(id=1)
        expected_object_name = f'{product.prod_name}'
        self.assertEqual(expected_object_name, str(product))

    def test_get_prod_date(self):
        product = Product.objects.get(id=1)
        product.prod_name = 'changed the name'
        self.assertTrue(product.updated_at, datetime.datetime.now)

    def test_get_absolute_url(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.get_absolute_url(), '/vendor/home/1/')


class TestVendorProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        vendor = User.objects.create(username='jitesh')
        VendorProfile.objects.create(Vendor=vendor)

    def test_prod_object_name(self):
        vendor_profile = VendorProfile.objects.get(id=1)
        expected_object_name = f'{vendor_profile.Vendor.username}'
        self.assertEquals(expected_object_name, str(vendor_profile))


class TestVendorQty(TestCase):
    @classmethod
    def setUpTestData(cls):
        vendor = User.objects.create(username='jitesh')
        category = Category.objects.create(cat_name='Groceries')
        product = Product.objects.create(category=category, prod_name='test_prod1', cost=50)
        VendorQty.objects.create(Vendor=vendor, product=product, qty=100)

    def test_prod_object_name(self):
        vendor_qty = VendorQty.objects.get(id=1)
        expected_object_name = f'{vendor_qty.Vendor.username}--{vendor_qty.product.prod_name}'
        self.assertEquals(expected_object_name, str(vendor_qty))


class ReviewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(cat_name='Groceries')
        product = Product.objects.create(category=category, prod_name='test_prod1', cost=50)
        customer = User.objects.create(username='jitesh')
        Review.objects.create(category=category, product=product, customer=customer, content='Test Review')

    def test_prod_object_name(self):
        review = Review.objects.get(id=1)
        expected_object_name = f'{review.content}'
        self.assertEquals(expected_object_name, str(review))
