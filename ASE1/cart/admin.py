from django.contrib import admin
from cart.models import Order, OrderItem, Transaction

admin.site.register((Order, OrderItem, Transaction))
