from django.urls import path
from . import views
from travelling.urls import views as travel_views
from travelling import settings

urlpatterns = [
    path("", travel_views.home),    

    path('registration/', views.hotel_owner_registration, name='hotel_registration'),
    path('login/', views.hotel_login, name='hotel_login'),
    path('logout/', views.hotel_logout, name='hotel_logout'),

    path('images/', views.hotel_images, name="hotel_images"),
    path('image-upload/', views.add_hotel_images, name="add_image_hotel"),
    path('image-delet/<int:image_id>', views.delete_hotel_image, name="delete_image_hotel"),

    path('dashboard/', views.hotel_dashboard, name='hotel_dashboard'),

    # path('hotel_images/', views.hotel_images, name='hotel_images'),

    path('images/',views.hotel_images,name='hotel_images'),
    path("contact_support", views.contact_support, name='contact_support')
]
