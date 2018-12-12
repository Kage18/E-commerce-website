from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    cat_name = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse('vendor:home')

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

    def get_absolute_url(self):
        return reverse('vendor:items', args=[str(self.id)])

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
        return self.Vendor.username+'--'+self.product.prod_name


class VendorProfile(models.Model):
    Vendor = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        return self.Vendor.username


class Review(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    rating = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.content