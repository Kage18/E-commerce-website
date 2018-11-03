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
    qty = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    brand = models.CharField(max_length=150, blank=True)
    # photo = models.ImageField(upload_to='documents/', blank=True)

    def __str__(self):
        return self.prod_name

class VendorProfile(models.Model):
    Vendor = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        return self.Vendor.username