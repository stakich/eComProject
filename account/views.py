from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import RegisterUserForm
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = "account/registration/register.html"
    success_url = reverse_lazy("store")


    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()


        # Generate token and send email
        current_site = get_current_site(self.request)
        subject = "Activate your account"
        
        message = render_to_string('account/registration/email-verification.html', {

            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': user_tokenizer_generate.make_token(user),

        })

        user.email_user(subject=subject, message=message)




        return redirect('email_verification_sent')

def email_verification(request):
    return render(request, "account/registration/email_verification.html")

def email_verification_sent(request):
    return render(request, "account/registration/email_verification_sent.html")

def email_verification_success(request):
    return render(request, "account/registration/email_verification_success.html")

def email_verification_failed(request):
    return render(request, "account/registration/email_verification_failed.html")

