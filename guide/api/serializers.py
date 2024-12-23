from rest_framework import serializers
from guide.models import Place, Image, Guide, Doctor


class PlaceSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Doctor
        fields = [
            'id', 'guide', 'name', 'speciality', 'phone', 'email', 'address', 'weekly_closed_on', 'open_time', 'service_time',
]