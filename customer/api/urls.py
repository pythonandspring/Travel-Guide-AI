from django.apps import AppConfig
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import ProfileViewSet


class GuideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guide'
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('', include(router.urls)),  # Include all the generated routes for the viewsets.
]