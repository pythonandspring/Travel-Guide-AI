from django.apps import AppConfig
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, ImageViewSet, GuideViewSet, DoctorViewSet
router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'placeimages', ImageViewSet)
router.register(r'guides', GuideViewSet)
router.register(r'doctors', DoctorViewSet)
urlpatterns = [
    path('api/token/', obtain_auth_token, name='api_token_auth'),  # Token endpoint
    path('', include(router.urls)),
]


class GuideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guide'
