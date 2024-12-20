from .models import Hotel
from django import forms
from .models import Hotel, HotelImage, HotelRoom
from django.core.exceptions import ValidationError


class HotelOwnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password"}),
        label="Password",
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm your password"}),
        label="Confirm Password",
        required=False
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
            "password",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Hotel description"}),
            "hotel_address": forms.Textarea(attrs={"rows": 3, "placeholder": "Hotel address"}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Set all fields to required=False
    #     for field_name, field in self.fields.items():
    #         field.required = False

    def clean(self):
        cleaned_data = super().clean()

        # Extract cleaned data
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        week_days_opening_time = cleaned_data.get("week_days_opening_time")
        week_days_closing_time = cleaned_data.get("week_days_closing_time")
        weekends_opening_time = cleaned_data.get("weekends_opening_time")
        weekends_closing_time = cleaned_data.get("weekends_closing_time")

        # Validate passwords
        if password and confirm_password:
            if password != confirm_password:
                self.add_error("confirm_password", "Passwords do not match.")

        # Validate weekday opening and closing times
        if week_days_opening_time and week_days_closing_time:
            if week_days_opening_time >= week_days_closing_time:
                self.add_error(
                    "week_days_closing_time", "Weekday opening time must be earlier than closing time.")

        # Validate weekend opening and closing times
        if weekends_opening_time and weekends_closing_time:
            if weekends_opening_time >= weekends_closing_time:
                self.add_error(
                    "weekends_closing_time", "Weekend opening time must be earlier than closing time.")

        return cleaned_data



class HotelLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        label="Email",
        max_length=255,
        required=True,
        help_text="please enter HOTEL EMAIL ID not owner's email Id."
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 
        'form-control'}),
        required=True,
        label="Password"
    )


class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.hotel_id = kwargs.pop('hotel_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.hotel_id:
            raise forms.ValidationError("A valid Hotel ID must be provided.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        try:
            instance.hotel = Hotel.objects.get(id=self.hotel_id)
        except Hotel.DoesNotExist:
            raise ValueError("The specified Hotel does not exist.")

        if commit:
            instance.save()
        return instance


class HotelRoomForm(forms.ModelForm):
    class Meta:
        model = HotelRoom
        fields = [
            'room_category',
            'room_type',
            'total_rooms',
            'available_rooms',
            'price_per_6hrs',
        ]
        widgets = {
            'room_category': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'total_rooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'available_rooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'price_per_6hrs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, * args, **kwargs):
        self.hotel_id = kwargs.pop('hotel_id', None)
        super().__init__(*args, **kwargs)

        if not self.hotel_id:
            raise ValueError("Hotel ID must be provided through the session.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Assign the hotel instance
        try:
            instance.hotel = Hotel.objects.get(id=self.hotel_id)
        except Hotel.DoesNotExist:
            raise ValidationError("The provided Hotel ID does not exist.")

        # Save the instance if commit is True
        if commit:
            instance.save()
        return instance
    

class HotelRoomUpdateForm(forms.ModelForm):
    class Meta:
        model = HotelRoom
        fields = [
            'total_rooms',
            'available_rooms',
            'price_per_6hrs',
        ]


class HotelDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            "hotel_name",
            "hotel_phone_number",
            "hotel_email",
            "hotel_address",
            "location_on_map",
            "description",
            "weekly_closed_on",
            "special_closed_dates",
            "week_days_opening_time",
            "week_days_closing_time",
            "weekends_opening_time",
            "weekends_closing_time",
        ]
    def clean(self):
        cleaned_data = super().clean()

        # Weekday time fields
        week_days_opening_time = cleaned_data.get("week_days_opening_time")
        week_days_closing_time = cleaned_data.get("week_days_closing_time")

        # Weekend time fields
        weekends_opening_time = cleaned_data.get("weekends_opening_time")
        weekends_closing_time = cleaned_data.get("weekends_closing_time")

        # Validate weekday times
        if week_days_opening_time and week_days_closing_time:
            if week_days_opening_time >= week_days_closing_time:
                raise ValidationError(
                    "Weekday opening time must be earlier than weekday closing time."
                )

        # Validate weekend times
        if weekends_opening_time and weekends_closing_time:
            if weekends_opening_time >= weekends_closing_time:
                raise ValidationError(
                    "Weekend opening time must be earlier than weekend closing time."
                )

        return cleaned_data



