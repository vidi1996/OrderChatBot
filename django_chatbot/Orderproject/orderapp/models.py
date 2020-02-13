from django.db import models
#from phone_field import PhoneField
from django.core.validators import RegexValidator


class OrderDetails(models.Model):
    choice = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    customize = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_no = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    #mobile_no = models.CharField(max_length=1000)
    address = models.CharField(max_length=50)
# Create your models here.

