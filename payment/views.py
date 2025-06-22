from django.shortcuts import render # type: ignore
from django.views.generic import TemplateView, UpdateView # type: ignore
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import ShippingAddress 
from store.models import Product
from cart.cart import Cart
from payment.models import Order, OrderItem

# Create your views here.
class PaymentSuccessView(TemplateView):
    def get(self, request, *args, **kwargs):

        for key in list(request.session.keys()):

            if key == "session_cart":

                del request.session[key]
        
        return super().get(request, *args, **kwargs)
        

    template_name = 'payment/payment-success.html'


class PaymentFailedView(TemplateView):
    template_name = 'payment/payment-failed.html'

class CheckoutView(UpdateView):
    template_name = 'payment/checkout.html'
    model = ShippingAddress
    fields = ['full_name', 'email', 'address1', 'address2', 'city', 'state', 'zipcode']
    success_url = reverse_lazy('payment-success')

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            return None
        return ShippingAddress.objects.get(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        return form
    
def complete_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        the_email = request.POST.get('the_email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        shipping_address = "\n".join([address1, address2, city, state, zipcode])

        cart = Cart(request)
        total_cost = cart.get_total()

        order_data = {
            'full_name': name,
            'email': the_email,
            'shipping_address': shipping_address,
            'amount_paid': total_cost,
        }

        if request.user.is_authenticated:
            order_data['user'] = request.user

        order = Order.objects.create(**order_data)

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['qty'],
                price=item['price'],
                user=request.user if request.user.is_authenticated else None
            )
        order_success = True

        response = JsonResponse({'success': order_success, 'order_id': order.id})

        return response
