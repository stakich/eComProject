from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
# Create your models here.

class ShippingAdress(models.Model):

    full_name = models.CharField(max_length=200)

    email = models.EmailField(max_length=256)

    address1 = models.CharField(max_length=256)

    address2 = models.CharField(max_length=256, null=True, blank=True)

    city = models.CharField(max_length=256)

    # OPTIONAl

    state = models.CharField(max_length=256, null=True, blank=True)

    zipcode = models.CharField(max_length=256, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Shipping Address'

    
    def __str__(self):
        return f"Shipping Address - {self.id}"