from django import forms
from . models import ShippingAdress


class ShippingAdressForm(forms.ModelForm):
    class Meta:

        model = ShippingAdress
        
        exclude = ['user',]  # or specify fields to exclude like ['field1', 'field2']