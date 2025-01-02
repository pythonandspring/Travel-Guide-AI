from django.apps import AppConfig
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet


class GuideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guide'
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Include all the generated routes for the viewsets.
]