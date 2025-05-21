from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import RegisterUserForm


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = "account/registration/register.html"
    success_url = reverse_lazy("login")

    # optional: add extra context
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Create an account"
        return ctx