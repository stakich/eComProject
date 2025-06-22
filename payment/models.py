from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
# Create your models here.

class ShippingAddress(models.Model):

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
    

class Order(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=256)
    shipping_address = models.TextField(max_length=10000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True,)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Order Item - {self.id}"
