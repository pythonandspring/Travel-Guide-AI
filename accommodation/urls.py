from django.urls import path
from . import views
from travelling.urls import views as travel_views
from travelling import settings


urlpatterns = [
    path("", travel_views.home),    

    path('hotel_owner_register/', views.hotel_owner_registration, name='hotel_owner_register'),
    path('hotel_owner_login/', views.user_login, name='hotel_owner_login'),

]
