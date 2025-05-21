from django.urls import path, include  # type: ignore
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register')
]