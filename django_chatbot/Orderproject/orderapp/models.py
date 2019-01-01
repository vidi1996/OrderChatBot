from django.db import models


class OrderDetails(models.Model):
    choice = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    customize = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    mobile_no = models.IntegerField()
    address = models.CharField(max_length=50)
# Create your models here.

