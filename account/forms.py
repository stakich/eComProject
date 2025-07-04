from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django.core.validators import (
    EmailValidator, MaxLengthValidator, MinLengthValidator
)
from django.core.exceptions import ValidationError




DISPOSABLE_DOMAINS = {
    "tempmail.com", "mailinator.com", "dispostable.com",
}

def no_whitespace(value):
    if any(c.isspace() for c in value):
        raise ValidationError("Email must not contain spaces.")

def domain_blocklist(value):
    domain = value.rsplit("@", 1)[-1].lower()
    if domain in DISPOSABLE_DOMAINS:
        raise ValidationError("Disposable email addresses are not allowed.")

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        max_length=254,
        validators=[
            EmailValidator(message="Enter a valid email address."),
            no_whitespace,
            MaxLengthValidator(254, message="Email is too long (max 254 characters)."),
            domain_blocklist,
        ],
        error_messages={
            "required": "Email is required.",
            "invalid":  "Enter a valid email address.",
        }
    )

    class Meta:
        model  = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        local_part = email.split("@", 1)[0]
        if len(local_part) > 64:
            raise forms.ValidationError(
                "The part before the @ is too long (max 64 characters)."
            )

        # case-insensitive uniqueness
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already taken. Please use another one."
            )
        return email
    

class LoginUserForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

    class Meta:
        model = User


class UpdateUserForm(UserChangeForm):
    
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

        email_field = self.fields['email']

        email_field.validators.append(domain_blocklist)
        email_field.validators.append(no_whitespace)

    class Meta(UserChangeForm.Meta):
        model = User

        fields = ['username', 'email']  


    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        local_part = email.split("@", 1)[0]
        if len(local_part) > 64:
            raise forms.ValidationError(
                "The part before the @ is too long (max 64 characters)."
            )
        
        if len(email) > 254:
            raise forms.ValidationError(
                "Email is too long (max 254 characters)."
            )

        # case-insensitive uniqueness
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "This email is already taken. Please use another one."
            )
        return email
