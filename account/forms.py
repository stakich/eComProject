from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

DISPOSABLE_DOMAINS = {
    "tempmail.com", "mailinator.com", "dispostable.com",  # add more as needed
}

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        
        # 1) Validate basic email format
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address.")
        
        # 2) No whitespace anywhere
        if ' ' in email:
            raise forms.ValidationError("Email must not contain spaces.")

        # 3) Length checks
        if len(email) > 254:
            raise forms.ValidationError("Email is too long (max 254 characters).")
        local_part, domain = email.rsplit('@', 1)
        if len(local_part) > 64:
            raise forms.ValidationError("The part before the @ is too long (max 64 characters).")

        # 4) Disposable domain block
        if domain.lower() in DISPOSABLE_DOMAINS:
            raise forms.ValidationError("Disposable email addresses are not allowed.")

        # 5) Case-insensitive uniqueness
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already taken. Please use another one.")
        
        # Return the normalized email
        return email.lower()
