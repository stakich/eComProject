from django.shortcuts import render # type: ignore
from django.views.generic import TemplateView # type: ignore

# Create your views here.
class PaymentSuccessView(TemplateView):
    template_name = 'payment/payment-success.html'


class PaymentFailedView(TemplateView):
    template_name = 'payment/payment-failed.html'

class CheckoutView(TemplateView):
    template_name = 'payment/checkout.html'
