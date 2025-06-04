from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, TemplateView, UpdateView, DeleteView
from django.contrib.auth.models import User, auth

from account.mixins import RedirectAuthenticatedUserMixin
from .forms import RegisterUserForm, LoginUserForm, UpdateUserForm
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin




# Create your views here.
class RegisterView(RedirectAuthenticatedUserMixin, CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = "account/registration/register.html"
    success_url = reverse_lazy("store")
    redirect_authenticated_user_to = reverse_lazy('dashboard')


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

class EmailVerificationView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and user_tokenizer_generate.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("email_verification_success")

        return redirect("email_verification_failed")
    
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect(self.redirect_authenticated_user_to)



class EmailVerificationSentView(TemplateView):
    template_name = "account/registration/email-verification-sent.html"

class EmailVerificationSuccessView(TemplateView):
    template_name = "account/registration/email-verification-success.html"


class EmailVerificationFailedView(TemplateView):
    template_name = "account/registration/email-verification-failed.html"

class LoginFormView(RedirectAuthenticatedUserMixin, LoginView):
    authentication_form = LoginUserForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('dashboard')
    redirect_authenticated_user_to = reverse_lazy('dashboard')


# def my_login(request):
#     form = LoginUserForm
#     if request.method == 'POST':
#         form = LoginUserForm(request, data=request.POST)

#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 auth.login(request, user)

#                 return redirect('store')

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "account/dashboard.html"
    login_url = reverse_lazy('login')


class LogoutUserView(LoginRequiredMixin,LogoutView):
    next_page = reverse_lazy('store')
    login_url = reverse_lazy('login')


class ProfileManagementView(LoginRequiredMixin,UpdateView):
    model = User
    template_name = "account/profile-management.html"
    form_class = UpdateUserForm
    success_url   = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return self.request.user



class DeleteAccountView(LoginRequiredMixin, DeleteView):
    template_name = "account/delete-account.html"
    model = User
    success_url = reverse_lazy('store')

    def get_object(self, queryset=None):
        return self.request.user
