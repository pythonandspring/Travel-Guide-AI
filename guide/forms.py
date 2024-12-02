from django import forms
from .models import Guide
from travelling.json_to_choice_fields import extract_states, extract_cities, extract_places, extract_countries

class GuideRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}),
        label="Password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'form-control'}),
        label="Confirm Password",
    )

    class Meta:
        model = Guide
        fields = ['name', 'email', 'password', 'phone', 'is_super_guide', 'country', 'state', 'city', 'place']
    
    def __init__(self, *args, **kwargs):
        # Extract specific data from kwargs
        self.country = kwargs.pop('country', None)
        self.state = kwargs.pop('state', None)
        self.city = kwargs.pop('city', None)

        # Call the parent constructor
        super().__init__(*args, **kwargs)

        # Ensure fields exist before accessing them
        if 'country' in self.fields:
            self.fields['country'].choices = [
                (country_option, country_option) for country_option in extract_countries()
            ]

        if 'state' in self.fields and self.country:
            self.fields['state'].choices = [
                (state_option, state_option) for state_option in extract_states(self.country)
            ]
        else:
            self.fields['state'].choices = []

        if 'city' in self.fields and self.state:
            self.fields['city'].choices = [
                (city_option, city_option) for city_option in extract_cities(self.state)
            ]
        else:
            self.fields['city'].choices = []

        if 'place' in self.fields and self.city:
            self.fields['place'].choices = [
                (place_option, place_option) for place_option in extract_places(self.city)
            ]
        else:
            self.fields['place'].choices = []

        # Debugging output for troubleshooting
        print(f"Country provided: {self.country}, State provided: {self.state}, City provided: {self.city}")
        print(f"Fetching states for country: {self.country}")
        print(f"Fetching cities for state: {self.state}")
        print(f"Fetching places for city: {self.city}")
        

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