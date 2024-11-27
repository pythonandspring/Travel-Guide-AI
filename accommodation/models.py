from django.db import models

from django.db import models

class HotelOwner(models.Model):

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    address = models.TextField(blank=True, null=True)

    hotel_name = models.CharField(max_length=255)
    hotel_address = models.TextField()
    description = models.TextField(blank=True, null=True)  

    total_ac_rooms = models.PositiveIntegerField(default=0)  
    total_non_ac_rooms = models.PositiveIntegerField(default=0)  
    available_ac_rooms = models.PositiveIntegerField(default=0)  
    available_non_ac_rooms = models.PositiveIntegerField(default=0)  
    price_per_ac_room = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    price_per_non_ac_room = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hotel_name} - Owned by {self.name}"