from django.db import models
from vendor.models import Product, VendorProfile
from customer.models import CustomerProfile
from django.contrib.auth.models import User


class OrderItem(models.Model):
    vendor = models.ManyToManyField(User)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_ordered = models.DateTimeField(null=True)
    qty = models.IntegerField(null=True, default=1)
    ref_code = models.CharField(max_length=20)

    def __str__(self):
        return self.product.prod_name

    def __unicode__(self):
        return '%s' % self.product.prod_name


class Order(models.Model):
    vendor = models.ManyToManyField(User)
    owner = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True, related_name='o')
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem, related_name='item')
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(null=True)

    def get_cart_item(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.cost * item.qty for item in self.items.all()])

    def get_qr_code(self):
        string = ""
        string += "Order Id :  " + str(self) + "\n"
        string += "For Mr/Mrs " + str(self.owner) + "\n"
        string += "Date Ordered :  " + str(self.date_ordered) + "\n\n"
        string += "Item : Quantity\n"
        for item in self.items.all():
            string += str(item.product.prod_name) + " : " + str(item.qty) + "\n"
        string += "Total is  :  ₹" + str(self.get_cart_total()) + "\n"
        string += "\nThank You"
        # print(string)
        return string

    def __str__(self):
        return '{0} -- {1}'.format(self.owner, self.ref_code)


class Transaction(models.Model):
    profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']
