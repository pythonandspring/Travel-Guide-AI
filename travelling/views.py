from django.conf import settings
from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html', {'MEDIA_URL': settings.MEDIA_URL})


def get_cities(request):
    state = request.GET.get("state")
    cities = extract_cities(state)
    return JsonResponse({"cities": cities})

def get_places(request):
    state = request.GET.get("state")
    city = request.GET.get("city")
    places = extract_place(city)
    return JsonResponse({"places": places})