from rest_framework import serializers, viewsets, permissions
from .models import Hotel, HotelRoom, HotelImage, Profile, Place, Image, Guide, Doctor

# Serializers
class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'hotel', 'name', 'image']


class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = [
            'id', 'hotel', 'room_category', 'room_type', 'total_rooms', 'available_rooms', 'price_per_6hrs'
        ]


class HotelSerializer(serializers.ModelSerializer):
    rooms = HotelRoomSerializer(many=True, read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id', 'hotel_owner_name', 'owner_phone_number', 'owner_email', 'password',
            'hotel_name', 'hotel_phone_number', 'hotel_email', 'hotel_address',
            'ratings', 'location_on_map', 'description', 'country', 'state', 'city',
            'place', 'weekly_closed_on', 'special_closed_dates',
            'week_days_opening_time', 'week_days_closing_time',
            'weekends_opening_time', 'weekends_closing_time', 'rooms', 'images'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'location', 'birth_date', 'travel_preferences', 'favorite_destinations',
            'languages_spoken', 'budget_range', 'interests'
        ]


class PlaceSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Place
        fields = [
            'id', 'name', 'country', 'state', 'city', 'address', 'location_on_map',
            'area_size', 'history', 'speciality', 'best_months_to_visit', 'appealing_text',
            'front_image', 'nearest_cities', 'airports', 'railway_stations',
            'by_road_distances_from_railway_stations', 'by_road_distances_from_airports',
            'by_road_distances_from_nearest_cities', 'weekly_closed_on', 'special_closed_dates',
            'week_days_opening_time', 'week_days_closing_time', 'weekends_opening_time',
            'weekends_closing_time', 'images'
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'place', 'image']


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = [
            'id', 'name', 'profile_image', 'email', 'phone', 'password', 'address',
            'is_occupied', 'is_super_guide', 'country', 'state', 'city', 'place'
        ]


class DoctorSerializer(serializers.ModelSerializer):
    guide = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'guide', 'name', 'speciality', 'phone', 'email', 'address', 'weekly_closed_on', 'open_time'
        ]


# ViewSets
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HotelRoomViewSet(viewsets.ModelViewSet):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HotelImageViewSet(viewsets.ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# URLs (Add this to urls.py)
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'hotel-rooms', HotelRoomViewSet)
router.register(r'hotel-images', HotelImageViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'place-images', ImageViewSet)
router.register(r'guides', GuideViewSet)
router.register(r'doctors', DoctorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
