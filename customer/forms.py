from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_username(self):
        return self.cleaned_data.get('username')  


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'email', 
        ]

    location = forms.CharField(max_length=100, required=False, label='Location')
    birth_date = forms.DateField(required=False, label='Birth Date', widget=forms.SelectDateWidget(years=range(1900, 2025)))
    travel_preferences = forms.CharField(max_length=350,required=False, label='Travel Preferences', widget=forms.Textarea)
    favorite_destinations = forms.CharField(widget=forms.Textarea, required=False, label='Favorite Destinations')
    languages_spoken = forms.CharField(max_length=255, required=False, label='Languages Spoken')
    budget_range = forms.CharField(max_length=50, required=False, label='Budget Range')
    interests = forms.CharField(max_length=255, required=False, label='Interests')

    def _init_(self, *args, **kwargs):
        super(EditProfileForm, self)._init_(*args, **kwargs)
    
        if self.instance.pk:  
            profile = self.instance.profile
            self.fields['location'].initial = profile.location
            self.fields['birth_date'].initial = profile.birth_date
            self.fields['travel_preferences'].initial = profile.travel_preferences
            self.fields['favorite_destinations'].initial = profile.favorite_destinations
            self.fields['languages_spoken'].initial = profile.languages_spoken
            self.fields['budget_range'].initial = profile.budget_range
            self.fields['interests'].initial = profile.interests

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        
        if commit:
            user.save()
            profile = user.profile 
            profile.location = self.cleaned_data.get('location')
            profile.birth_date = self.cleaned_data.get('birth_date')
            profile.travel_preferences = self.cleaned_data.get('travel_preferences')
            profile.favorite_destinations = self.cleaned_data.get('favorite_destinations')
            profile.languages_spoken = self.cleaned_data.get('languages_spoken')
            profile.budget_range = self.cleaned_data.get('budget_range')
            profile.interests = self.cleaned_data.get('interests')
            profile.save()

        return user
