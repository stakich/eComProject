from django.urls import path, include # type: ignore
from . import views

urlpatterns = [
    path('payment-success/', views.PaymentSuccessView.as_view(), name='payment-success'),
    path('payment-failed/', views.PaymentFailedView.as_view(), name='payment-failed'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('complete-order/', views.complete_order, name='complete-order'),
]
