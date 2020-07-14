from django.db import models

# Create your models here.
class Department(models.Model):
    dept_name=models.CharField(max_length=100)


class Path(models.Model):
    dept_sequence=models.CharField(max_length=100)

