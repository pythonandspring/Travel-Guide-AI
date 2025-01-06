from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from customer.api.views import ProfileViewSet, UserViewSet

# update
# Base router for UserViewSet
router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')


# Nested router for ProfileViewSet (profiles will be nested under users)
user_router = NestedDefaultRouter(router, r'user', lookup='user')
user_router.register(r'profile', ProfileViewSet, basename='user-profile')


# Combine URLs
urlpatterns = [
    path('', include(router.urls)),  # Include user-level routes
    # Include nested profile-level routes under a specific user
    path('', include(user_router.urls)),
]
