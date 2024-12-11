from django.urls import path
from . import views
from travelling.urls import views as travel_views
from travelling import settings

urlpatterns = [
    path("", travel_views.home),    

    path('registration/', views.hotel_owner_registration, name='hotel_registration'),
    path('login/', views.hotel_login, name='hotel_login'),
    path('dashboard/', views.hotel_dashboard, name='hotel_dashboard'),
    path('update_dashboard', views.update_hotel_details, name='update_dashboard'),
    path('logout/', views.hotel_logout, name='hotel_logout'),
    
    path('images/', views.hotel_images, name="hotel_images"),
    path('image-upload/', views.add_hotel_images, name="add_image_hotel"),
    path('image-delete/<int:image_id>', views.delete_hotel_image, name="delete_image_hotel"),
    path('image-rename/<int:image_id>', views.rename_hotel_image, name="rename_image_hotel"),
    path('image-popup/<int:image_id>/', views.hotel_image_popup, name="hotel_image_popup"), 

    path('rooms/', views.available_rooms, name='available_rooms'),
    path('add_room_type/', views.add_room_type, name='add_room_type'),
    path('update_room_details/<int:room_id>/', views.update_room, name='update_room_details'),
    path('delete_room/<int:room_id>/', views.delete_room_type, name="delete_room"),

    # path('delete_account/<int:hotel_id>/', ),
    path("contact_support", views.contact_support, name='contact_support')
]
