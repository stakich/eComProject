from django.shortcuts import render, get_object_or_404 # type: ignore
from .models import Category, Product # type: ignore
from django.views.generic import ListView, DetailView # type: ignore
from django.http import HttpResponse # type: ignore


def store(request):

    all_products = Product.objects.all()

    
    return render(request, 'store/store.html', context={'all_products': all_products})

def category_list(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

def product_info(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_info.html', context={'product': product}) 

def list_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/list-category.html', context={'category': category, 'products': products})