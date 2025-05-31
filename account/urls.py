from django.urls import path, include  # type: ignore
from . import views


urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('email-verification/<str:uidb64>/<str:token>/', views.EmailVerificationView.as_view(), name='email_verification'),
    path('email-verification-sent', views.EmailVerificationSentView.as_view(), name='email_verification_sent'),
    path('email-verification-success', views.EmailVerificationSuccessView.as_view(), name='email_verification_success'),
    path('email-verification-failed', views.EmailVerificationFailedView.as_view(), name='email_verification_failed'),
    path('login', views.LoginFormView.as_view(), name='login'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('user-logout', views.LogoutUserView.as_view(), name='user-logout')
]
