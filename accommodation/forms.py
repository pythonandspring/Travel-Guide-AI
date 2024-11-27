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
            "address",
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
            "address": forms.Textarea(attrs={"rows": 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data