from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    return render(request, 'cart/cart-summary.html')


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, qty=product_qty)

        response = JsonResponse({'The product is called: ': product.title, ' and the quantity is: ': product_qty})

        return response

def cart_delete(request):
    pass


def cart_update(request):
    pass