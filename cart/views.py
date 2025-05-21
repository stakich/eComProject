from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart':    cart})


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, qty=product_qty)

        cart_quantity = cart.__len__()

        response = JsonResponse({"qty": cart_quantity})

        return response

def cart_delete(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        return  JsonResponse({
                "qty":   cart_quantity,                
                "total":   str(cart_total),  
                "deleted_id": product_id
            })

    

    return JsonResponse({"error": "invalid request"}, status=400)


def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('qty'))

        cart.update(product=product_id, qty=product_qty)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        return  JsonResponse({
                "qty":   cart_quantity,                
                "total":   str(cart_total),  
                "updated_id": product_id
            })