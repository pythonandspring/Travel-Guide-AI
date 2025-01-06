from django.shortcuts import get_object_or_404
from rest_framework import viewsets, serializers
from rest_framework.exceptions import NotFound
from customer.models import Profile
from customer.api.serializers import ProfileSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Fetch all users and their profiles
    @action(detail=False, methods=['get'])
    def all_profiles(self, request):
        users = User.objects.all()
        profiles = Profile.objects.filter(user__in=users)

        # Serialize all profiles
        serialized_profiles = ProfileSerializer(profiles, many=True).data
        return Response(serialized_profiles)

# update

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Restricts the queryset to the profile for the user specified in the nested URL.
        """
        user_id = self.kwargs.get("user_pk")
        user = get_object_or_404(User, id=user_id)
        return Profile.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Associates the profile with the user from the nested URL during creation.
        """
        user_id = self.kwargs.get("user_pk")
        user = get_object_or_404(User, id=user_id)

        if Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                {"detail": "User already has a profile."})

        serializer.save(user=user)

    def perform_update(self, serializer):
        """
        Ensures the profile is correctly updated with the user from the nested URL.
        """
        user_id = self.kwargs.get("user_pk")
        user = get_object_or_404(User, id=user_id)
        serializer.save(user=user)
