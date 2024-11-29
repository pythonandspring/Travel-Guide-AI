from django.urls import path
from travelling.urls import views as travel_views
from . import views

urlpatterns = [
    path('registration/', views.guide_registration, name='guide_registration'),
    path('login/', views.guide_login, name='guide_login'),
    path("contact_support", views.contact_support, name='contact_support'),
    path("", travel_views.home),
]
