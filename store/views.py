from django.shortcuts import render # type: ignore
from .models import Category, Product # type: ignore
from django.views.generic import ListView, DetailView # type: ignore
from django.http import HttpResponse # type: ignore

def store(request):
    return render(request, 'store/store.html')

def category_list(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}