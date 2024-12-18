from django.db import models
import os
from travelling.filter_data.get_data import get_countries, get_cities, get_place, get_states
from django.core.validators import MinValueValidator, MaxValueValidator

class Hotel(models.Model):

    country_choice = [(country_option, country_option) for country_option in get_countries()]
    state_choice = [(state_option, state_option) for state_option in get_states()]
    city_choice = [(city_option, city_option) for city_option in get_cities()]
    place_choice = [(place_option, place_option) for place_option in get_place()]

    DAYS_OF_WEEK = [
            ('MON', 'Monday'),
            ('TUE', 'Tuesday'),
            ('WED', 'Wednesday'),
            ('THU', 'Thursday'),
            ('FRI', 'Friday'),
            ('SAT', 'Saturday'),
            ('SUN', 'Sunday'),
        ]

    # hotel owner details
    hotel_owner_name = models.CharField(max_length=255)
    owner_phone_number = models.CharField(max_length=11, unique=True)
    owner_email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  

    # hotel details
    hotel_name = models.CharField(max_length=255, unique=True)
    hotel_phone_number = models.CharField(max_length=11, unique=True)
    hotel_email = models.EmailField(unique=True)
    hotel_address = models.TextField()
    ratings = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],help_text="Enter a rating between 0 and 10.", null=True)
    location_on_map = models.URLField()
    description = models.TextField(blank=True, null=True) 

    # hotel's associated destination
    country = models.CharField(max_length=50, choices=country_choice, null=False)
    state = models.CharField(max_length=50, choices=state_choice, null=False)
    city = models.CharField(max_length=50, choices=city_choice, null=False)
    place = models.CharField(max_length=50, choices=place_choice, null=False)

    # opening and closing days and timings
    weekly_closed_on = models.CharField(
        max_length=20,
        choices=DAYS_OF_WEEK,
        null=True,
        blank=True,
        help_text="Day of the week when the tour place is regularly closed."
    )

    special_closed_dates = models.TextField( 
        null=True,
        blank=True,
        help_text="Special dates when the tour place is closed, formatted as a comma-separated list (e.g., '2024-12-25, 2025-01-01')."
    )

    week_days_opening_time = models.TimeField(null=True, blank=True)
    week_days_closing_time = models.TimeField(null=True, blank=True)
    
    weekends_opening_time = models.TimeField(null=True, blank=True)
    weekends_closing_time = models.TimeField(null=True, blank=True)

   
    def __str__(self):
        return f"{self.hotel_name} - Owned by {self.hotel_owner_name}"


class HotelRoom(models.Model):
    
    ROOM_CATEGORY_CHOICES = [
        ('AC', 'AC'),
        ('Non-AC', 'Non-AC'),
    ]

    ROOM_TYPE_CHOICES = [
        ('Single Bed', 'Single Bed'),
        ('Double Bed', 'Double Bed'),
        ('Suite', 'Suite'),
    ]
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')

    room_category = models.CharField(max_length=10, choices=ROOM_CATEGORY_CHOICES)
    
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    
    total_rooms = models.PositiveIntegerField(default=0)  
    available_rooms = models.PositiveIntegerField(default=0)  
    price_per_6hrs = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  


    def __str__(self):
        return f"{self.room_category} - {self.room_type} - Total: {self.total_rooms}, Available: {self.available_rooms}, Price per 6hrs: {self.price_per_6hrs} - Hotel: {self.hotel.hotel_name}"


def hotel_image_upload_to(instance, filename):
    """
    Constructs the upload path for place images.
    Images are stored in a folder named after the Place name within the 'place_images' directory.
    """
    return os.path.join('hotel_images', instance.hotel.hotel_name.replace(' ', '_'), filename)


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='images', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False,default="hotel_image")
    image = models.ImageField(upload_to=hotel_image_upload_to)

    def __str__(self):
        return f"Image for {self.hotel.hotel_name}"
 


