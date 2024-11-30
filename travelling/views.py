from django.conf import settings
from django.shortcuts import render, redirect
from .json_to_choice_fields import extract_cities, extract_place
from django.http import JsonResponse
from pyexpat.errors import messages
from travelling.json_to_choice_fields import extract_cities, extract_place
from django.http import JsonResponse
from django.core.cache import cache


def home(request):
    return render(request, 'home.html')


def agentRegistration(request):
    if request.method == 'POST':
        form = request.POST.get('agentRegistration')
        messages.success(request, "Agent Registration request has been sent!")
        return redirect('agentRegistration')
    
    return render(request, 'agentRegistration.html')





def gallery(request):
    places = [
        {"name": "Paris", "location": "France", "description": "Known for the Eiffel Tower, art, and its romantic ambiance.", "image": f"{settings.MEDIA_URL}images/paris.jpg"},
        {"name": "Kyoto", "location": "Japan", "description": "Famous for its temples, traditional tea houses, and cherry blossoms.", "image": f"{settings.MEDIA_URL}images/kyoto.jpg"},
        {"name": "Rome", "location": "Italy", "description": "Known for the Colosseum, rich history, and Italian cuisine.", "image": f"{settings.MEDIA_URL}images/rome.jpg"},
        {"name": "Cape Town", "location": "South Africa", "description": "Famous for Table Mountain, beaches, and stunning landscapes.", "image": f"{settings.MEDIA_URL}images/cape_town.jpg"},
        {"name": "Sydney", "location": "Australia", "description": "Home to the iconic Opera House and beautiful harbor views.", "image": f"{settings.MEDIA_URL}images/sydney.jpg"},
        {"name": "New York City", "location": "USA", "description": "Famous for the Statue of Liberty, Times Square, and Central Park.", "image": f"{settings.MEDIA_URL}images/new_york.jpg"},
        {"name": "Dubai", "location": "UAE", "description": "Known for luxury shopping, ultramodern architecture, and lively nightlife.", "image": f"{settings.MEDIA_URL}images/dubai.jpg"},
        {"name": "Venice", "location": "Italy", "description": "Unique for its canals, gondolas, and beautiful architecture.", "image": f"{settings.MEDIA_URL}images/venice.jpg"},
        {"name": "London", "location": "United Kingdom", "description": "Known for the Big Ben, Buckingham Palace, and the River Thames.", "image": f"{settings.MEDIA_URL}images/london.jpg"},
        {"name": "Bangkok", "location": "Thailand", "description": "Famous for vibrant street life, cultural landmarks, and grand palaces.", "image": f"{settings.MEDIA_URL}images/bangkok.jpg"},
        {"name": "Barcelona", "location": "Spain", "description": "Known for the architecture of Antoni Gaudí, including the Sagrada Familia.", "image": f"{settings.MEDIA_URL}images/barcelona.jpg"},
        {"name": "Machu Picchu", "location": "Peru", "description": "Ancient Inca city set high in the Andes Mountains, known for its stunning views.", "image": f"{settings.MEDIA_URL}images/machu_picchu.jpg"},
        {"name": "Istanbul", "location": "Turkey", "description": "Known for its historic sites such as the Hagia Sophia and Blue Mosque.", "image": f"{settings.MEDIA_URL}images/istanbul.jpg"},
        {"name": "Santorini", "location": "Greece", "description": "Famous for its whitewashed buildings, crystal-clear waters, and sunsets.", "image": f"{settings.MEDIA_URL}images/santorini.jpg"},
        {"name": "Berlin", "location": "Germany", "description": "Known for its historical landmarks such as the Berlin Wall and Brandenburg Gate.", "image": f"{settings.MEDIA_URL}images/berlin.jpg"},
        {"name": "Athens", "location": "Greece", "description": "Famous for ancient monuments like the Acropolis and Parthenon.", "image": f"{settings.MEDIA_URL}images/athens.jpg"}
    ]

    # messages.warning(request,"Loading assets, please hold on")
    return render(request, 'gallery.html')


def feedback(request):
    cache.clear()
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        messages.success(request, "Thank you for your feedback!")
        return redirect('gen_feedback')

    return render(request, 'feedback.html')

def gen_contact(request):    
    return render(request, 'gen_contact.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_conditions(request):
    return render(request,'travel/terms_conditions.html')


def get_cities(request):
    state = request.GET.get("state")
    cities = extract_cities(state)
    return JsonResponse({"cities": cities})


def get_places(request):
    city = request.GET.get("city")
    places = extract_place(city)
    return JsonResponse({"places": places})