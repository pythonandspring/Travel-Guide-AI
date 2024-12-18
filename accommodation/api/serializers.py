from rest_framework import serializers
from accommodation.models import Hotel, HotelRoom, HotelImage

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = '__all__' 


class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields ='__all__' 


class HotelSerializer(serializers.ModelSerializer):
    rooms = HotelRoomSerializer(many=True, read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'



