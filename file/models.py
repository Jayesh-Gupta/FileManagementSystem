from django.db import models

# Create your models here.
class Register(models.Model):
    email=models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
