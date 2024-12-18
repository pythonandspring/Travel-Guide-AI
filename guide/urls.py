from django.urls import path
from travelling.urls import views as travel_views
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", travel_views.home),

    path('registration/', views.guide_registration, name='guide_registration'),
    path('login/', views.guide_login, name='guide_login'),
    path('dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('edit-profile/', views.guide_edit_profile, name='guide_edit_profile'),
    path('logout/', views.guide_logout, name='guide_logout'),

    path('get-doctor/', views.get_doctors , name='get_doctors'),
    path('add-doctor/', views.add_doctor, name="add_doctor"),
    path('edit-doctor/<int:doctor_id>', views.update_doctor_details, name='guide_edit_doctor'),
    path('delete-doctor/<int:doctor_id>', views.delete_doctor, name='delete_doctor'),

    path('get-place-info/', views.get_place_info, name='get_place_info'),
    path('update-place-info/<int:place_id>', views.update_place_info, name='update_place_info'),
    path('add-image/', views.add_place_image, name='add_place_image'),
    path('get-images/<int:place_id>/', views.get_images, name='get_images'),
    path('delete-image/<int:place_id>/<int:image_id>/', views.delete_place_image, name='delete_place_image'),


    path("contact_support/", views.contact_support, name='contact_support'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
