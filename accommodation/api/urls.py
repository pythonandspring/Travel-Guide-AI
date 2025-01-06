from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, HotelRoomViewSet, HotelImageViewSet

# update

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'hotel-rooms', HotelRoomViewSet)
router.register(r'hotel-images', HotelImageViewSet)
urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs.
]
