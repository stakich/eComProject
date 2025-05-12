
from .cart import Cart
from django.conf import settings


def cart(request):
    cart = Cart(request)
    return {'cart': cart}