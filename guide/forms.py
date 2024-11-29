from django import forms
from .models import Guide
from travelling.json_to_choice_fields import extract_state, extract_cities, extract_place


print(extract_state())


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
        fields = ['name', 'email', 'password', 'phone', 'is_super_guide', 'state', 'city', 'place']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
    def _init_(self, *args, **kwargs):
        state = kwargs.pop('state', None)
        city = kwargs.pop('city', None)
        super()._init_(*args, **kwargs)

        self.fields['state'].choices = [(state_option, state_option) for state_option in extract_state()]
        self.fields['state'].initial = state
    
        if state:
            self.fields['city'].choices = [(city_option, city_option) for city_option in extract_cities(state)]
        else:
            self.fields['city'].choices = []

        if state and city:
            self.fields['place'].choices = [(place_option, place_option) for place_option in extract_place(city)]
        else:
            self.fields['place'].choices = []

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

    def _init_(self, *args, **kwargs):
        state = kwargs.pop('state', None)
        city = kwargs.pop('city', None)
        super()._init_(*args, **kwargs)

        self.fields['state'].choices = [(state_option, state_option) for state_option in extract_state()]
        self.fields['state'].initial = state
    
        if state:
            self.fields['city'].choices = [(city_option, city_option) for city_option in extract_cities(state)]
        else:
            self.fields['city'].choices = []

        if state and city:
            self.fields['place'].choices = [(place_option, place_option) for place_option in extract_place(city)]
        else:
            self.fields['place'].choices = []