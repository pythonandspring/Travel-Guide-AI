from django.db import models
import os

def place_image_upload_to(instance, filename):
    """
    Constructs the upload path for place images.
    Images are stored in a folder named after the Place name within the 'place_images' directory.
    """
    return os.path.join('place_images', instance.place.name.replace(' ', '_'), filename)


class HotelOwner(models.Model):
    hotel_owner_name = models.CharField(max_length=255)
    owner_phone_number = models.CharField(max_length=11, unique=True)
    owner_email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  

    country = models.CharField(max_length=50, choices=[], null=False)
    state = models.CharField(max_length=50, choices=[], null=False)
    city = models.CharField(max_length=50, choices=[], null=False)
    place = models.CharField(max_length=50, choices=[], null=False)

    hotel_name = models.CharField(max_length=255)
    hotel_phone_number = models.CharField(max_length=11, unique=True)
    hotel_email = models.EmailField(unique=True)
    hotel_address = models.TextField()
    description = models.TextField(blank=True, null=True)  

    total_ac_rooms = models.PositiveIntegerField(default=0)  
    total_non_ac_rooms = models.PositiveIntegerField(default=0)  
    available_ac_rooms = models.PositiveIntegerField(default=0)  
    available_non_ac_rooms = models.PositiveIntegerField(default=0)  
    price_per_ac_room = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    price_per_non_ac_room = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
   
    def __str__(self):
        return f"{self.hotel_name} - Owned by {self.name}"



class Image(models.Model):
    place = models.ForeignKey(HotelOwner, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=place_image_upload_to)

    def __str__(self):
        return f"Image for {self.place.name}"
 


