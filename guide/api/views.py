from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from guide.models import Place, Image, Guide, Doctor
from .serializers import PlaceSerializer, ImageSerializer, GuideSerializer, DoctorSerializer
# update

class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class GuideViewSet(ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer


class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    