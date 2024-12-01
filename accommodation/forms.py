from django import forms
from .models import Hotel
from travelling.json_to_choice_fields import extract_states, extract_cities, extract_places, extract_countries


class HotelOwnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password"}),
        label="Confirm Password"
    )

    class Meta:
        model = Hotel
        fields = [
            "hotel_owner_name",
            "owner_phone_number",
            "owner_email",
            "hotel_name",
            "hotel_phone_number",
            "hotel_email",
            "hotel_address",
            "location_on_map",
            "description",
            "country",
            "state",
            "city",
            "place",
            "weekly_closed_on",
            "special_closed_dates",
            "week_days_opening_time",
            "week_days_closing_time",
            "weekends_opening_time",
            "weekends_closing_time",
            "password"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Hotel description"}),
            "hotel_address": forms.Textarea(attrs={"rows": 3, "placeholder": "Hotel address"}),
        }

    def __init__(self, *args, **kwargs):
        country = kwargs.pop('country', None)
        state = kwargs.pop('state', None)
        city = kwargs.pop('city', None)
        super().__init__(*args, **kwargs)

        self.fields['country'].choices = [(country_option, country_option) for country_option in extract_countries()]
        self.fields['country'].initial = country

        if country:
            self.fields['state'].choices = [(state_option, state_option) for state_option in extract_states(country)]
        else:
            self.fields['state'].choices = []

        if state:
            self.fields['city'].choices = [(city_option, city_option) for city_option in extract_cities(state)]
        else:
            self.fields['city'].choices = []

        if state and city:
            self.fields['place'].choices = [(place_option, place_option) for place_option in extract_places(city)]
        else:
            self.fields['place'].choices = []




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