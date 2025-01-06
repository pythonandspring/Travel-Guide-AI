from django.db import models
import os
from travelling.filter_data.get_data import get_countries, get_cities, get_place, get_states 
from django.contrib.auth.models import User
import uuid


def place_image_upload_to(instance, filename):
    """
    Constructs the upload path for place images.
    Images are stored in a folder named after the Place name within the 'place_images' directory.
    """
    return os.path.join('place_images', instance.place.name.lower().replace(' ', '_'), filename)


def place_front_image_upload(instance, filename):

    return os.path.join('front_images', instance.name.lower().replace(' ', '_'), filename)


class Place(models.Model):

    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    # name
    name = models.CharField(max_length=255)

    # Location
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    address = models.TextField()
    location_on_map = models.URLField(max_length=1000)

    # Information about history, speciality, appealing_text, size
    area_size = models.CharField(
        max_length=255,
        help_text="Enter the size of the area (e.g., in square meters)",
        null=True,
        blank=True
    )

    history = models.TextField(
        help_text="Provide a detailed history or background information related to the entity."
    )

    speciality = models.TextField(
        help_text="Describe the main specialties or unique features of the entity."
    )

    best_months_to_visit = models.CharField(
        max_length=255,
        help_text="Enter the best months to visit, separated by commas (e.g., 'January, February, March')."
    )

    appealing_text = models.TextField(
        null=True, 
        blank=True, 
        help_text="Add a brief, engaging description to attract and retain users."
    )

    front_image = models.ImageField(upload_to=place_front_image_upload, default="no picture")

    # nearest travelling options
    nearest_cities = models.TextField(
        help_text="List nearby cities, separated by commas."
    )

    airports = models.TextField(
        help_text="List nearby airports, separated by commas."
    )

    railway_stations = models.TextField(
        help_text="List nearby railway stations, separated by commas."
    )

    by_road_distances_from_railway_stations = models.TextField(
        help_text="Enter road distances to nearby railway stations.(railway_station, distance)"
    )

    by_road_distances_from_airports = models.TextField(
        help_text="Enter road distances to nearby airports.(airports, distance)"
    )

    by_road_distances_from_nearest_cities = models.TextField(
        help_text="Enter road distances to nearby cities.(nearest_cities, distance)"
    )

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
        return self.name


class Image(models.Model):
    place = models.ForeignKey(
        Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='place_images/')

    def __str__(self):
        return f"Image for {self.place.name}"


class Guide(models.Model):
    
    country_choice = [(country_option, country_option) for country_option in get_countries()]
    state_choice = [(state_option, state_option) for state_option in get_states()]
    city_choice = [(city_option, city_option) for city_option in get_cities()]
    place_choice = [(place_option, place_option) for place_option in get_place()]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    is_occupied = models.BooleanField(default=False)
    is_super_guide = models.BooleanField(default=False)

    
    country = models.CharField(max_length=50, choices=country_choice, null=False)
    state = models.CharField(max_length=50, choices=state_choice, null=False)
    city = models.CharField(max_length=50, choices=city_choice, null=False)
    place = models.CharField(max_length=50, choices=place_choice, null=False)
    
    def __str__(self):
        return f"{self.name}:{self.place}- {'Super Guide' if self.is_super_guide else 'Guide'}"



class Doctor(models.Model):

    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name="doctors")
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)

    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    
    weekly_closed_on = models.CharField(
        max_length=20,
        choices=DAYS_OF_WEEK,
        null=True,
        blank=True,
        help_text="Day of the week when the tour place is regularly closed."
    )

    open_time = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.speciality}"


class PasswordResetToken(models.Model):
    guide = models.OneToOneField(Guide, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    sender = models.ForeignKey(
        User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='received_requests', on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username} ({self.status})"
