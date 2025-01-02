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

    def update(self, instance, validated_data):
        rooms_data = validated_data.pop('rooms', None)

        # Update the Hotel instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle rooms updates or creations
        if rooms_data:
            room_ids = {
                room['id']: room for room in rooms_data if room.get('id')}
            existing_rooms = {room.id: room for room in instance.rooms.all()}

            # Update existing rooms
            for room_id, room_data in room_ids.items():
                if room_id in existing_rooms:
                    room_instance = existing_rooms[room_id]
                    for attr, value in room_data.items():
                        setattr(room_instance, attr, value)
                    room_instance.save()
                else:  # Create new room if it doesn't exist
                    HotelRoom.objects.create(hotel=instance, **room_data)

            # # Handle rooms that should be removed (if needed, adjust based on your business logic)
            # for room_instance in existing_rooms.values():
            #     if room_instance.id not in room_ids:
            #         room_instance.delete()

        return instance

    def to_internal_value(self, data):
        print("Incoming Data to Serializer:", data)
        return super().to_internal_value(data)
