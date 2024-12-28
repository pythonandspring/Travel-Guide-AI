from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from pyexpat.errors import messages
from guide.models import Place, Guide, Image
from accommodation.models import Hotel, HotelImage
from django.core.cache import cache
from django.contrib.auth.decorators import login_required



def home(request):
    if request.session.get('super_guide_id') or request.session.get('guide_id'):
        try:
            guide_id = request.session.get('super_guide_id')
            guide = Guide.objects.get(id=guide_id)
        except Guide.DoesNotExist:
            guide_id = request.session.get('guide_id')
            guide = Guide.objects.get(id=guide_id)
        finally:
            return render(request, 'home.html', {'guide': guide})
    elif request.session.get('hotel_owner_id'):
        hotel_owner = Hotel.objects.get(id=request.session['hotel_owner_id'])
        return render(request, 'home.html', {'hotel_owner': hotel_owner})
    else: 
        return render(request, 'home.html')



def agentRegistration(request):
    if request.method == 'POST':
        form = request.POST.get('agentRegistration')
        messages.success(request, 'Agent Registration request has been sent!')
        return redirect('agentRegistration')
    
    return render(request, 'agentRegistration.html')


def gallery(request):
    places = Place.objects.all()
    return render(request, 'gallery.html', {'places': places, 'MEDIA_URL': settings.MEDIA_URL})
def gallery_view(request):
    places = Place.objects.all()
    cities = places.values_list('city', flat=True).distinct()
    states = places.values_list('state', flat=True).distinct()
    countries = places.values_list('country', flat=True).distinct()

    context = {
        'places': places,
        'cities': cities,
        'states': states,
        'countries': countries,
    }
    return render(request, 'gallery.html', context)

def get_place(request, place_id):
    place = Place.objects.get(id=place_id)
    images = Image.objects.filter(place=place.id)
    hotels = Hotel.objects.filter(place=place.name)
    guides = Guide.objects.filter(place=place.name)
    print(place.name)
    if place:
        request.session['place_exist'] = True
        return render(request, 'place.html', {'place_exist': True, 'place': place, 'MEDIA_URL': settings.MEDIA_URL, 'images': images, 'hotels': hotels, 'guides': guides})
    else:
        request.session['place_exist'] = False
        messages.error(request, f"doesn't exist in database now.")
        return render(request, 'place.html', {'place_exist': False, 'MEDIA_URL': settings.MEDIA_URL, 'images': images, 'hotels': hotels, 'guides': guides})


def get_hotel_details(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    images = HotelImage.objects.filter(hotel_id=hotel.id)
    print(images)
    return render(request, 'hotel_details.html', {'hotel':hotel, 'images':images})


def contact(request):    
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'contact.html',context)


def feedback(request):
    cache.clear()
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        messages.success(request, 'Thank you for your feedback!')
        return redirect('gen_feedback')

    return render(request, 'feedback.html')


def gen_contact(request):    
    return render(request, 'gen_contact.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_conditions(request):
    return render(request,'travel/terms_conditions.html')


def get_states(request):
    country = request.GET.get('country')
    states = Place.objects.filter(country=country).values_list(
        'state', flat=True).distinct()
    states = list(states)
    return JsonResponse({'states': states})


def get_cities(request):
    state = request.GET.get('state')
    cities = Place.objects.filter(state=state).values_list(
        'city', flat=True).distinct()
    cities = list(cities)
    return JsonResponse({'cities': cities})


def get_places(request):
    city = request.GET.get('city')
    places = Place.objects.filter(city=city).values_list('name', flat=True).distinct()
    places = list(places)
    return JsonResponse({'places': places})

