# guide/forms.py
class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'city', 'state', 'country', 'description', 'location_url', 'image']


