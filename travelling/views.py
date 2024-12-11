from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from pyexpat.errors import messages
from travelling.json_to_choice_fields import extract_states, extract_cities, extract_places
from guide.models import Place, Guide
from accommodation.models import Hotel
from django.core.cache import cache


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
    places = [
        {'name': 'Paris', 'location': 'France', 'description': 'Known for the Eiffel Tower, art, and its romantic ambiance.', 'image': f'images/paris.jpg'},
        {'name': 'Kyoto', 'location': 'Japan', 'description': 'Famous for its temples, traditional tea houses, and cherry blossoms.', 'image': f'images/kyoto.jpg'},
        {'name': 'Rome', 'location': 'Italy', 'description': 'Known for the Colosseum, rich history, and Italian cuisine.', 'image': f'images/rome.jpg'},
        {'name': 'Cape Town', 'location': 'South Africa', 'description': 'Famous for Table Mountain, beaches, and stunning landscapes.', 'image': f'images/cape_town.jpg'},
        {'name': 'Sydney', 'location': 'Australia', 'description': 'Home to the iconic Opera House and beautiful harbor views.', 'image': f'images/sydney.jpg'},
        {'name': 'New York City', 'location': 'USA', 'description': 'Famous for the Statue of Liberty, Times Square, and Central Park.', 'image': f'images/new_york.jpg'},
        {'name': 'Dubai', 'location': 'UAE', 'description': 'Known for luxury shopping, ultramodern architecture, and lively nightlife.', 'image': f'images/dubai.jpg'},
        {'name': 'Venice', 'location': 'Italy', 'description': 'Unique for its canals, gondolas, and beautiful architecture.', 'image': f'images/venice.jpg'},
        {'name': 'London', 'location': 'United Kingdom', 'description': 'Known for the Big Ben, Buckingham Palace, and the River Thames.', 'image': f'images/london.jpg'},
        {'name': 'Bangkok', 'location': 'Thailand', 'description': 'Famous for vibrant street life, cultural landmarks, and grand palaces.', 'image': f'images/bangkok.jpg'},
        {'name': 'Barcelona', 'location': 'Spain', 'description': 'Known for the architecture of Antoni Gaudí, including the Sagrada Familia.', 'image': f'images/barcelona.jpg'},
        {'name': 'Machu Picchu', 'location': 'Peru', 'description': 'Ancient Inca city set high in the Andes Mountains, known for its stunning views.', 'image': f'images/machu_picchu.jpg'},
        {'name': 'Istanbul', 'location': 'Turkey', 'description': 'Known for its historic sites such as the Hagia Sophia and Blue Mosque.', 'image': f'images/istanbul.jpg'},
        {'name': 'Santorini', 'location': 'Greece', 'description': 'Famous for its whitewashed buildings, crystal-clear waters, and sunsets.', 'image': f'images/santorini.jpg'},
        {'name': 'Berlin', 'location': 'Germany', 'description': 'Known for its historical landmarks such as the Berlin Wall and Brandenburg Gate.', 'image': f'images/berlin.jpg'},
        {'name': 'Athens', 'location': 'Greece', 'description': 'Famous for ancient monuments like the Acropolis and Parthenon.', 'image': f'images/athens.jpg'}
    ]
    if request.session.get('super_guide_id') or request.session.get('guide_id'):
        try:
            guide_id = request.session.get('super_guide_id')
            guide = Guide.objects.get(id=guide_id)
        except Guide.DoesNotExist:
            guide_id = request.session.get('guide_id')
            guide = Guide.objects.get(id=guide_id)
        finally:
            return render(request, 'gallery.html', {'places': places, 'guide': guide})
    elif request.session.get('hotel_owner_id'):
        hotel_owner = Hotel.objects.get(id=request.session['hotel_owner_id'])
        return render(request, 'gallery.html', {'places': places, 'hotel_owner': hotel_owner})
    else:
        return render(request, 'gallery.html', {'places': places})




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
    states = extract_states(country)
    return JsonResponse({'states': states})


def get_cities(request):
    state = request.GET.get('state')
    cities = extract_cities(state)
    return JsonResponse({'cities': cities})


def get_places(request):
    city = request.GET.get('city')
    places = extract_places(city)
    return JsonResponse({'places': places})