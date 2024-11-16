from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']

class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)
