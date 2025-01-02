from rest_framework import serializers
from django.contrib.auth.models import User
from customer.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Add more user fields if needed.

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nest User data inside Profile
    
    class Meta:
        model = Profile
        fields = fields = [
            "user",
            "location",
            "birth_date",
            "travel_preferences",
            "favorite_destinations",
            "languages_spoken",
            "budget_range",
            "interests",
            "about"
        ] 
