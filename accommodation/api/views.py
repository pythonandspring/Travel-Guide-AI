from rest_framework.viewsets import ModelViewSet
from accommodation.models import Hotel, HotelRoom, HotelImage
from .serializers import HotelSerializer, HotelRoomSerializer, HotelImageSerializer

class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelRoomViewSet(ModelViewSet):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer

class HotelImageViewSet(ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer

# update

