from django import forms
from .models import Guide, Doctor, Place, Image


class GuideRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}),
        label='Password',
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'form-control'}),
        label='Confirm Password',
    )

    class Meta:
        model = Guide
        fields = ['name', 'email', 'password', 'phone', 'is_super_guide', 'country', 'state', 'city', 'place']
        

class GuideLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        label='Email',
        max_length=255
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        label='Password'
    )


class GuideDetailsUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Guide
        fields = ['name', 'email', 'phone', 'country', 'state', 'city', 'place']


class DoctorDetailsUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Doctor
        fields = [
            'name',
            'speciality',
            'phone',
            'email',
            'address',
            'weekly_closed_on',
            'service_time',
        ]



class PlaceDetailsUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Place
        fields = [
            'address',
            'area_size',
            'history',
            'speciality',
            'best_months_to_visit',
            'appealing_text',
            'nearest_cities',
            'airports',
            'railway_stations',
            'by_road_distances_from_railway_stations',
            'by_road_distances_from_airports',
            'by_road_distances_from_nearest_cities',
            'weekly_closed_on',
            'special_closed_dates',
            'week_days_opening_time',
            'week_days_closing_time',
            'weekends_opening_time',
            'weekends_closing_time',
        ]


class PlaceImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.place_id = kwargs.pop('place_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.place_id:
            raise forms.ValidationError("A valid Hotel ID must be provided.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        try:
            instance.hotel = Place.objects.get(id=self.place_id)
        except Place.DoesNotExist:
            raise ValueError("The specified Hotel does not exist.")

        if commit:
            instance.save()
        return instance
