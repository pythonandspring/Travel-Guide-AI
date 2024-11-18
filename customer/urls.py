from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.guide,name="home"),
    path('gallery/', views.gallery, name='gallery'),
    path('feedback/', views.feedback, name='feedback'),
    path('accomodations/', views.accomodations, name='accomodations'),
    path('agentRegistration/', views.agentRegistration, name='agentRegistration'),
    path('contact/', views.contact, name='contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),

    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('search_voice/', views.search_voice, name='search_voice'),

    # for admin use
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]