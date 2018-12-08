from django.contrib import admin
from vendor.models import *

admin.site.register((Category, Product, VendorProfile, VendorQty))
