from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import HotelViewSet, HotelRoomViewSet, HotelImageViewSet


router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'hotel-rooms', HotelRoomViewSet)
router.register(r'hotel-images', HotelImageViewSet)
urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs.
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]
