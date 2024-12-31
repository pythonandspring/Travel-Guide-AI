from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Home page
    path("", views.home, name="home"),

    # Customer URLs
    path("customer/", include("customer.urls")),  # Updated to avoid root conflict

    # Other views
    path('gallery/', views.gallery, name='gallery'),
    path('get-guides/', views.guide_list, name='get_guides'),
    path('get-guide-details/<int:id>/', views.get_guide_details, name='guide_details'),

    path('hotels/', views.hotel_list, name='hotel_list'),
    path("get-hotel-details/<int:hotel_id>",
         views.get_hotel_details, name='get_hotel_details'),
         
    path('agentRegistration/', views.agentRegistration, name='agentRegistration'),
    path('feedback/', views.feedback, name='gen_feedback'),
    path('gen_contact/', views.gen_contact, name="gen_contact"),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),
    path("place/<int:place_id>", views.get_place, name='get_place'),
    
    path('dj-admin/', admin.site.urls),
    path("guide/", include("guide.urls"), name='guide'),
    path("accommodation/", include("accommodation.urls"), name="accommodation"),
    path('chat/', include('chat.urls')),
    
    path('get-states/', views.get_states, name="get_states"),
    path("get-cities/", views.get_cities, name="get_cities"),
    path("get-places/", views.get_places, name="get_places"),

    path('api/accommodation/', include('accommodation.api.urls')),
    path('api/customer/', include('customer.api.urls')),
    path('api/guide/', include('guide.api.urls')),


    # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] 

# Static and Media Files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
