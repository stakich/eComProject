from django.shortcuts import redirect
from django.urls import reverse_lazy

class RedirectAuthenticatedUserMixin:

    redirect_authenticated_user_to = reverse_lazy("account_dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_authenticated_user_to)
        return super().dispatch(request, *args, **kwargs)