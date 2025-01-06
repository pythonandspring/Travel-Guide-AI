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
# update
    def create(self, validated_data):
        # Use create_user for proper password hashing
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    # User field is read-only and inferred from the URL
    user = serializers.PrimaryKeyRelatedField(read_only=True)

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
        # The user instance is passed explicitly from the view
        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError(
                {"user": "User instance is required."})

        # Check if a profile already exists for this user
        if Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError("User already has a profile.")

        # Create the profile
        return Profile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
