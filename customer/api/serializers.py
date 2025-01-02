# customer/api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from customer.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Use create_user for proper password hashing
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested User serializer

    class Meta:
        model = Profile
        fields = [
            "user",
            "location",
            "birth_date",
            "travel_preferences",
            "favorite_destinations",
            "languages_spoken",
            "budget_range",
            "interests",
        ]

    def create(self, validated_data):
        # Extract nested user data
        user_data = validated_data.pop("user")

        # Create or get the user instance (if already exists)
        user_id = user_data.get("id")
        if user_id:
            user = User.objects.get(id=user_id)
        else:
            user = UserSerializer().create(user_data)

        # Check if profile already exists for this user, if so raise an error
        if Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError("User already has a profile.")

        # Create the Profile instance
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        # Handle nested update for User
        user_data = validated_data.pop("user", None)
        if user_data:
            user_serializer = UserSerializer(
                instance=instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        # Update Profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
