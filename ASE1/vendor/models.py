from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    cat_name = models.CharField(max_length=150)

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    prod_name = models.CharField(max_length=150)
    ingredients = models.TextField(max_length=264, blank=True)
    stock = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    brand = models.CharField(max_length=150, blank=True)
    prod_pic = models.FileField(upload_to='documents/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # qty = models.ManyToManyField(VendorQty)

    def __str__(self):
        return self.prod_name

    def get_qty(self):
        # p = VendorQty.objects.get(Vendor=request.user,product=self)
        # print(p)
        print('12')
        return self.stock


class VendorQty(models.Model):
    Vendor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(default=0)

    def __str__(self):
        return self.Vendor.username




class VendorProfile(models.Model):
    Vendor = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        return self.Vendor.username
