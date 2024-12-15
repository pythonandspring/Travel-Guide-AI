"""
URL configuration for school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("", include("customer.urls"), name="customer"),

    path('gallery/', views.gallery, name='gallery'),
    path('agentRegistration/', views.agentRegistration, name='agentRegistration'),
    path('feedback/', views.feedback, name='gen_feedback'),
    path('agentRegistration/', views.agentRegistration, name='agentRegistration'),
    path('gen_contact/', views.gen_contact, name="gen_contact"),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),
    # path('search_voice/', views.search_voice, name='search_voice'),
    
    path('admin/', include('myadmin.urls')),
    path('dj-admin/', admin.site.urls),
    path("guide/", include("guide.urls"), name='guide'),
    path("accommodation/", include("accommodation.urls"), name="accommodation"),

    path('get-states/', views.get_states, name="get_states"),
    path("get-cities/", views.get_cities, name="get_cities"),
    path("get-places/", views.get_places, name="get_places"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
