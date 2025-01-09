from rest_framework import viewsets
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


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        # Get all profiles or filter by user if needed
        user_id = self.kwargs.get('user_pk', None)
        if user_id:
            # If a specific user ID is passed, filter profiles by that user
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise NotFound(detail="User not found", code=404)
            return Profile.objects.filter(user=user)
        else:
            # Otherwise, return all profiles
            return Profile.objects.all()

    def perform_create(self, serializer):
        user_id = self.kwargs['user_pk']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found", code=404)

        serializer.save(user=user)

    def perform_update(self, serializer):
        user_id = self.kwargs['user_pk']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found", code=404)

        serializer.save(user=user)

    def perform_destroy(self, instance):
        instance.delete()
