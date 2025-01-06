from django.db import transaction
from accommodation.models import Hotel, HotelRoom, HotelImage  
from rest_framework import serializers
from accommodation.models import Hotel, HotelRoom, HotelImage

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


# update

class HotelSerializer(serializers.ModelSerializer):
    rooms = HotelRoomSerializer(many=True)
    images = HotelImageSerializer(many=True)

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
