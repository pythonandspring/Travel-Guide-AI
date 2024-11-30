from django.db import models
import os

# def place_image_upload_to(instance, filename):
#     """
#     Constructs the upload path for place images.
#     Images are stored in a folder named after the Place name within the 'place_images' directory.
#     """
#     return os.path.join('place_images', instance.place.name.replace(' ', '_'), filename)

# class Place(models.Model):
#     name = models.CharField(max_length=255)
#     area = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     state = models.CharField(max_length=255)
#     address = models.TextField()
#     speciality = models.TextField()
#     attraction_info = models.TextField()
#     location_url = models.URLField()
#     nearest_cities = models.TextField()  
#     airports = models.TextField()  
#     railway_stations = models.TextField()  
#     by_road_distances = models.TextField()  
#     images = models.ImageField(upload_to='place_images/')

#     def __str__(self):
#         return self.name

# class Image(models.Model):
#     place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=place_image_upload_to)

#     def __str__(self):
#         return f"Image for {self.place.name}"


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