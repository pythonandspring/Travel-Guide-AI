from django.shortcuts import get_object_or_404, render
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from pyexpat.errors import messages
from guide.models import Place, Guide, Image, Doctor
from accommodation.models import Hotel, HotelImage
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
# from channels.layers import get_channel_layer


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
    if (request.session.get('super_guide_id') or request.session.get('guide_id')) and request.session.get('is_login'):
        return redirect('guide_dashboard')
    elif (request.session.get('is_logged_in')):
        return redirect('hotel_dashboard')
    elif (request.user.is_authenticated):
        return redirect('profile')
    else:
        if request.method == 'POST':
            form = request.POST.get('agentRegistration')
            messages.success(request, 'Agent Registration request has been sent!')
            return redirect('agentRegistration')
        
        return render(request, 'agentRegistration.html')


def gallery(request):
    places = Place.objects.all()

    # Extract distinct city, state, and country values
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
    try:
        # Attempt to fetch the place object
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        # Handle case where place does not exist
        messages.error(request, "The requested place does not exist.")
        return render(request, 'place.html', {
            'place_exist': False,
            'MEDIA_URL': settings.MEDIA_URL,
            'images': [],
            'hotels': [],
            'guides': [],
            'user': request.user,
            'has_pending_request': False
        })

    # Fetch related data
    images = Image.objects.filter(place=place.id)
    hotels = Hotel.objects.filter(place=place.name)
    guides = Guide.objects.filter(place=place.name)

    if place:
        request.session['place_exist'] = True
        return render(request, 'place.html', {'place_exist': True, 'place': place, 'MEDIA_URL': settings.MEDIA_URL, 'images': images, 'hotels': hotels, 'guides': guides, 'user':request.user})
    else:
        request.session['place_exist'] = False
        messages.error(request, f"doesn't exist in database now.")
        return render(request, 'place.html', {'place_exist': False, 'MEDIA_URL': settings.MEDIA_URL, 'images': images, 'hotels': hotels, 'guides': guides, 'user': request.user})


@login_required
def get_hotel_details(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    images = HotelImage.objects.filter(hotel_id=hotel.id)
    return render(request, 'hotel_details.html', {'hotel':hotel, 'images':images})


@login_required
def hotel_list(request):
    country = request.GET.get('country')
    state = request.GET.get('state')
    city = request.GET.get('city')
    place = request.GET.get('place')

    hotels = Hotel.objects.all()

    if country:
        hotels = hotels.filter(country=country)
    if state:
        hotels = hotels.filter(state=state)
    if city:
        hotels = hotels.filter(city=city)
    if place:
        hotels = hotels.filter(place=place)

    context = {
        'hotels': hotels,
        'countries': Hotel.objects.values_list('country', flat=True).distinct(),
        # Replace with your function to fetch states
        'states': Hotel.objects.values_list('state', flat=True).distinct(),
        # Replace with your function to fetch cities
        'cities': Hotel.objects.values_list('city', flat=True).distinct(),
        # Replace with your function to fetch places
        'places': Hotel.objects.values_list('place', flat=True).distinct(),
    }

    return render(request, 'hotels.html', context)


@login_required
def guide_list(request):
    # Get all guides from the database
    guides = Guide.objects.all()

    # Get distinct values for countries, states, cities, and places
    countries = Guide.objects.values_list('country', flat=True).distinct()
    states = Guide.objects.values_list('state', flat=True).distinct()
    cities = Guide.objects.values_list('city', flat=True).distinct()
    places = Guide.objects.values_list(
        'place', flat=True).distinct()  # Added place filter

    # Apply filters based on GET parameters if they exist
    search_query = request.GET.get('search', '')
    country_filter = request.GET.get('country', '')
    state_filter = request.GET.get('state', '')
    city_filter = request.GET.get('city', '')
    place_filter = request.GET.get('place', '')

    if search_query:
        guides = guides.filter(name__icontains=search_query)

    if country_filter:
        guides = guides.filter(country__icontains=country_filter)

    if state_filter:
        guides = guides.filter(state__icontains=state_filter)

    if city_filter:
        guides = guides.filter(city__icontains=city_filter)

    if place_filter:
        guides = guides.filter(place__icontains=place_filter)

    # Render the page with all necessary context data
    return render(request, 'guides.html', {
        'guides': guides,
        'countries': countries,
        'states': states,
        'cities': cities,
        'places': places,  # Pass places to the template
    })


@login_required
def get_guide_details(request, id):
    try:
        guide = Guide.objects.get(id=id)
        guide_data = {
            'id': guide.id,
            'name': guide.name,
            'email': guide.email,
            'phone': guide.phone,
            'is_super_guide': guide.is_super_guide,
            'country': guide.country,
            'state': guide.state,
            'city': guide.city,
            'place': guide.place,
        }
        doctors = Doctor.objects.filter(guide_id=id)
        return render(request, 'guide_details.html', {'guide':guide_data, 'doctors':doctors})
    except Guide.DoesNotExist:
        return redirect('get_guides')


def update_guide_status(request, guide_id):
    guide = Guide.objects.get(id=guide_id)

    # Toggle the status for example
    guide.is_occupied = not guide.is_occupied
    guide.save()

    # Get the channel layer and send a message to the WebSocket consumer
    # channel_layer = get_channel_layer()
    channel_layer.group_send(
        'guide_updates_group',
        {
            'type': 'guide_status_update',
            'guide_id': guide.id,
            'is_occupied': guide.is_occupied
        }
    )

    return JsonResponse({'status': 'success'})

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

