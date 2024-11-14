from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import Profile


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'email', 
        ]

    location = forms.CharField(max_length=100, required=False)
    birth_date = forms.DateField(required=False)
    travel_preferences = forms.JSONField(required=False)
    favorite_destinations = forms.CharField(widget=forms.Textarea, required=False)
    languages_spoken = forms.CharField(max_length=255, required=False)
    budget_range = forms.CharField(max_length=50, required=False)
    interests = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
    
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

