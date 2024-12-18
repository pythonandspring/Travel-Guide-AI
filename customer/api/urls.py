from django.apps import AppConfig
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
urlpatterns = [
    path('api/token/', obtain_auth_token, name='api_token_auth'),  # Token endpoint
    path('', include(router.urls)),  # Include all the generated routes for the viewsets.
]


class GuideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guide'
