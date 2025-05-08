from django.urls import path, include  # type: ignore
from . import views

urlpatterns = [
    path('', views.store, name='store'),
]