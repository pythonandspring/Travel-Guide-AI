from django import forms
from .models import HotelOwner

class HotelOwnerRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = HotelOwner
        fields = [
            "name",
            "phone_number",
            "email",
            "password",
            "hotel_name",
            "hotel_address",
            "description",
            "total_ac_rooms",
            "total_non_ac_rooms",
            "price_per_ac_room",
            "price_per_non_ac_room",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "hotel_address": forms.Textarea(attrs={"rows": 3}),
        }
    

class HotelOwnerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        label="Email",
        max_length=255
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        label="Password"
    )