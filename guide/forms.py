from django import forms
from .models import Guide

class GuideRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password"}),
        label="Confirm Password"
    )

    class Meta:
        model = Guide
        fields = [
            "name",
            "email",
            "phone",
            "password",
            "is_super_guide",
            "assigned_place",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone Number"}),
            "assigned_place": forms.Select(attrs={"placeholder": "Select Place"}),
        }

class GuideLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        label="Email",
        max_length=255
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        label="Password"
    )