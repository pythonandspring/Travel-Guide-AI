from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from accommodation.models import Hotel, HotelRoom, HotelImage
from .serializers import HotelSerializer, HotelRoomSerializer, HotelImageSerializer

class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]

class HotelRoomViewSet(ModelViewSet):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer
    permission_classes = [IsAuthenticated]
    

class HotelImageViewSet(ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [IsAuthenticated]
