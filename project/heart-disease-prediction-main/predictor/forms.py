from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "first_name": "First name",
            "last_name": "Last name",
            "username": "Choose a username",
            "email": "you@example.com",
            "password1": "Create a password",
            "password2": "Confirm your password",
        }
        icons = {
            "first_name": "fa-user",
            "last_name": "fa-user",
            "username": "fa-at",
            "email": "fa-envelope",
            "password1": "fa-lock",
            "password2": "fa-shield-halved",
        }
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control auth-input",
                "placeholder": placeholders.get(field_name, ""),
                "autocomplete": "new-password" if "password" in field_name else "off",
                "data-icon": icons.get(field_name, ""),
            })

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control auth-input",
            "placeholder": "Username",
            "autocomplete": "username",
        })
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control auth-input",
            "placeholder": "Password",
            "autocomplete": "current-password",
        }),
    )
