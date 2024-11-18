from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    travel_preferences = models.JSONField(blank=True, null=True)  # JSONField for travel preferences
    favorite_destinations = models.TextField(blank=True, null=True)
    languages_spoken = models.CharField(max_length=255, blank=True, null=True)
    budget_range = models.CharField(max_length=255, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
