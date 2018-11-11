from django.contrib import admin
from cart.models import order, orderitem, Transaction
# Register your models here.
admin.site.register((order, orderitem, Transaction))