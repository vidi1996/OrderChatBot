from django.db import models
class OrderDetails(models.Model):
    #Choice = models.CharField(max_length=50)
    #Type = models.CharField(max_length=50)
    #Customize = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
   # Quantity = models.IntegerField()
    Mobile_no = models.IntegerField()
    Address = models.CharField(max_length=50)
# Create your models here.
