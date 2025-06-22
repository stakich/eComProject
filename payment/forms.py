from django import forms
from . models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:

        model = ShippingAddress
        
        exclude = ['user',]  # or specify fields to exclude like ['field1', 'field2']