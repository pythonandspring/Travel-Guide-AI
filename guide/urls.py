from django.urls import path
from travelling.urls import views as travel_views
from . import views

urlpatterns = [
    path('guide-registration/', views.guide_registration, name='guide_registration'),
    path('guide-login/', views.guide_login, name='guide_login'),
    path('guide-dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path("", travel_views.home),
]
