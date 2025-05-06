from django.shortcuts import render # type: ignore

# Create your views here.
from django.http import HttpResponse # type: ignore

def home(request):
    return HttpResponse("Welcome to the Store!")