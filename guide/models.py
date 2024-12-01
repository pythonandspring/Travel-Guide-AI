from django.db import models
import os

def place_image_upload_to(instance, filename):
    """
    Constructs the upload path for place images.
    Images are stored in a folder named after the Place name within the 'place_images' directory.
    """
    return os.path.join('place_images', instance.place.name.replace(' ', '_'), filename)


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
    location_on_map = models.URLField()

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
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=place_image_upload_to)

    def __str__(self):
        return f"Image for {self.place.name}"


class Guide(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    is_super_guide = models.BooleanField(default=False)

    country = models.CharField(max_length=255)
    state = models.CharField(max_length=50, choices=[])
    city = models.CharField(max_length=50, choices=[])
    place = models.CharField(max_length=50, choices=[])
    
    def __str__(self):
        return f"{self.name} - {'Super Guide' if self.is_super_guide else 'Guide'}"
    

class Doctor(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name="doctors")
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)

    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    
    available_dates = models.CharField(max_length=100, help_text="E.g., Mon-Fri")
    available_time = models.CharField(max_length=100, help_text="E.g., 9 AM - 5 PM")

    def __str__(self):
        return f"{self.name} - {self.specialty}"