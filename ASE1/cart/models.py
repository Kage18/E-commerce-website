from django.db import models
from vendor.models import Product
from customer.models import CustomerProfile


# Create your models here.


class orderitem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    q = models.IntegerField(null=True)

    def __str__(self):
        return self.product.prod_name


class order(models.Model):
    owner = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True, related_name='o')
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(orderitem)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(null=True)

    def get_cart_item(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.cost * item.qty for item in self.items.all()])

    def __str__(self):
        return '{0} -- {1}'.format(self.owner, self.ref_code)
