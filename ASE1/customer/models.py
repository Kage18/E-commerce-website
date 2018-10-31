from django.db import models
from django.contrib.auth.models import User


class CustomerProfile(models.Model):
    Customer = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        return self.Customer.username



