from django.contrib import admin
from vendor.models import Category, Product, VendorProfile

admin.site.register((Category, Product,VendorProfile))


# class VendorProfileAdmin(admin.ModelAdmin):
#     def username(self, obj):
#         return obj.Vendor.username
#
#     def email(self, obj):
#         return obj.Vendor.email
#
#
#     list_display = ['username', 'email', 'phone_number']



#admin.site.register(VendorProfile, VendorProfileAdmin)
