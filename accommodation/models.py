from django.db import models

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


 


