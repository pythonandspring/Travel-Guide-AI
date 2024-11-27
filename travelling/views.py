from django.conf import settings
from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html', {'MEDIA_URL': settings.MEDIA_URL})