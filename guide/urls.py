from django.urls import path
from travelling.urls import views as travel_views
from . import views

urlpatterns = [
    path('registration/', views.guide_registration, name='guide_registration'),
    path('login/', views.guide_login, name='guide_login'),
    path('logout/', views.guide_logout, name='guide_logout'),
    
    path('dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('edit-profile/', views.guide_edit_profile, name='guide_edit_profile'),
    path('edit-doctor/', views.guide_edit_doctor_profile, name='guide_edit_doctor_profile'),

    path("contact_support/", views.contact_support, name='contact_support'),
    path("", travel_views.home),
]
