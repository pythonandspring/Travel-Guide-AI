from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from guide.models import Place, Image, Guide, Doctor
from .serializers import PlaceSerializer, ImageSerializer, GuideSerializer, DoctorSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class GuideViewSet(ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
