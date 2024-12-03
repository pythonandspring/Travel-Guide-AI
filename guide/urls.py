from django.urls import path
from . import views

urlpatterns = [
    path('add_place/', views.add_place, name='add_place'),
    path('gallery/', views.gallery, name='gallery'),
]
