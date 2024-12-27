from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    location = models.CharField(max_length=100, blank=True, null=True, default="")
    birth_date = models.DateField(blank=True, null=True)
    travel_preferences = models.CharField(max_length=350,blank=True, null=True, default="")  
    favorite_destinations = models.TextField(blank=True, null=True, default="")  
    languages_spoken = models.CharField(max_length=255, blank=True, null=True, default="")  
    budget_range = models.CharField(max_length=350, blank=True, null=True, default="")
    interests = models.CharField(max_length=255, blank=True, null=True, default="")  
    about = models.CharField(max_length=250, null=True, default="")

    def _str_(self):
        return f"{self.user.username}'s profile"
