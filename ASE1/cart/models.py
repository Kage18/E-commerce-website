from django.db import models
from vendor.models import Product
from customer.models import CustomerProfile


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_ordered = models.DateTimeField(null=True)
    qty = models.IntegerField(null=True,default=1)
    ref_code = models.CharField(max_length=20)

    def __str__(self):
        return self.product.prod_name


class Order(models.Model):
    owner = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True, related_name='o')
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(null=True)

    def get_cart_item(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.cost*item.qty for item in self.items.all()])

    def __str__(self):
        return '{0} -- {1}'.format(self.owner, self.ref_code)


class Transaction(models.Model):
    profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']
