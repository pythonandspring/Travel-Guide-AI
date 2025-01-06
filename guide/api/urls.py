from django.apps import AppConfig
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, ImageViewSet, GuideViewSet, DoctorViewSet

# update
class GuideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guide'

router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'placeimages', ImageViewSet)
router.register(r'guides', GuideViewSet)
router.register(r'doctors', DoctorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]