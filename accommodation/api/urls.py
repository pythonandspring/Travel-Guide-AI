from django.contrib import admin
from travelling.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accommodation.urls')), 
]