from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Registermodel(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    def __str__(self):
        return self.first_name

class Loginmodel(models.Model):
    user = models.OneToOneField(User, on_delete='cascade')
    def __str__(self):
        return self.user.username
