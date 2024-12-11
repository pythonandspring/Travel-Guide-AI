from django.contrib.auth.models import User
from rest_framework import serializers
from travelling.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nest the UserSerializer

    class Meta:
        model = Profile
        fields = ['id', 'user', 'location', 'birth_date', 'travel_preferences', 
                  'favorite_destinations', 'languages_spoken', 'budget_range', 'interests']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)  # Extract nested user data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        instance.save()
        return instance