from django.urls import path

from . import views

urlpatterns = [
    path("",views.guide,name="home"),
    path('gallery/', views.gallery, name='gallery'),
    path('feedback/', views.feedback, name='feedback'),
    path('accomodations/', views.accomodations, name='accomodations'),
    path('agentRegistration/', views.agentRegistration, name='agentRegistration'),
    path('contact/', views.contact, name='contact'),
    path('customer/', views.customer, name='customer'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),


    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]
