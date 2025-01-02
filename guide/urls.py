from django.urls import path
from travelling.urls import views as travel_views
from . import views
from django.contrib.auth import views as auth_views
from .views import request_password_reset, reset_password


urlpatterns = [
    path("", travel_views.home),

    path('registration/', views.guide_registration, name='guide_registration'),
    path('login/', views.guide_login, name='guide_login'),
    path('dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('edit-profile/', views.guide_edit_profile, name='guide_edit_profile'),
    path('logout/', views.guide_logout, name='guide_logout'),
    path('guide-gallery/', views.gallery, name='guide_gallery'),
    path('get-doctor/', views.get_doctors , name='get_doctors'),
    path('add-doctor/', views.add_doctor, name="add_doctor"),
    path('edit-doctor/<int:doctor_id>', views.update_doctor_details, name='guide_edit_doctor'),
    path('delete-doctor/<int:doctor_id>', views.delete_doctor, name='delete_doctor'),

    path('get-place-info/', views.get_place_info, name='get_place_info'),
    path('update-place-info/', views.update_place_info, name='update_place_info'),
    path('add-image/', views.add_place_image, name='add_place_image'),
    path('get-images/<int:place_id>/', views.get_images, name='get_images'),
    path('delete-image/<int:place_id>/<int:image_id>/', views.delete_place_image, name='delete_place_image'),
    path('image-popup/<int:place_id>/<int:image_id>/', views.place_image_popup, name="place_image_popup"),

    path("contact_support/", views.contact_support, name='contact_support'),

    path('request-password-reset/', request_password_reset, name='guide_request_password_reset'),
    path('reset-password/<uuid:token>/', reset_password, name='guide_reset_password'),
]
