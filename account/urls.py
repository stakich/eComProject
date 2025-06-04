from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),

    path('email-verification/<str:uidb64>/<str:token>/', views.EmailVerificationView.as_view(), name='email_verification'),
    path('email-verification-sent/', views.EmailVerificationSentView.as_view(), name='email_verification_sent'),
    path('email-verification-success/', views.EmailVerificationSuccessView.as_view(), name='email_verification_success'),
    path('email-verification-failed/', views.EmailVerificationFailedView.as_view(), name='email_verification_failed'),

    path('login/', views.LoginFormView.as_view(), name='my-login'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('user-logout/', views.LogoutUserView.as_view(), name='user-logout'),

    path('profile-management/', views.ProfileManagementView.as_view(), name='profile-management'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete-account'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="account/password/password-reset.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="account/password/password-reset-sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password/password-reset-form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password/password-reset-complete.html"), name='password_reset_complete')
]
