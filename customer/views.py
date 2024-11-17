from django.shortcuts import render,redirect

#to view response on browser
from django.http import HttpResponse

# To use Django's messaging system
from django.contrib import messages  

# Create your views here.
#REVERSE - AVOID HARDCODING THE URLS 
from django.urls import reverse

#for image!
from django.conf import settings

def test(request):
    return HttpResponse("ok.")

def guide(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'travel/home.html',context)

def admin_login(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    if request.user.is_authenticated:
        return redirect('admin_dashboard')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if both fields have a minimum of 4 characters
        if len(username) >= 4 and len(password) >= 4:
            if username == 'admin' and password == 'admin':
                request.session['is_admin'] = True
                return redirect(reverse('admin_dashboard'))  # Redirect to dashboard on success
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Both username and password must be at least 4 characters long.')

    return render(request, 'travel/adminPage.html',context)


def admin_dashboard(request):

    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    # Check if the user is logged in and is an admin
    if not request.session.get('is_admin'):
        # Redirect to login if not authenticated as an admin
        messages.error(request, 'You need to log in as an admin first.')
        return redirect('admin_login')  # Redirect to the login page if not logged in as admin

    # Here you can render the actual admin dashboard page
    return render(request, 'travel/adminDashboard.html',context)

def admin_logout(request):
    # Clear the session to log out the admin
    if 'is_admin' in request.session:
        del request.session['is_admin']
        messages.success(request, 'You have logged out successfully.')
    else:
        messages.error(request, 'You are not logged in.')
    
    # Redirect to the login page after logging out
    return redirect('admin_login')  # Adjust to your actual login page URL


def gallery(request):
    places = [
        {"name": "Paris", "location": "France", "description": "Known for the Eiffel Tower, art, and its romantic ambiance.", "image": "images/paris.jpg"},
        {"name": "Kyoto", "location": "Japan", "description": "Famous for its temples, traditional tea houses, and cherry blossoms.", "image": "images/kyoto.jpg"},
        {"name": "Rome", "location": "Italy", "description": "Known for the Colosseum, rich history, and Italian cuisine.", "image": "images/rome.jpg"},
        {"name": "Cape Town", "location": "South Africa", "description": "Famous for Table Mountain, beaches, and stunning landscapes.", "image": "images/cape_town.jpg"},
        {"name": "Sydney", "location": "Australia", "description": "Home to the iconic Opera House and beautiful harbor views.", "image": "images/sydney.jpg"},
        {"name": "New York City", "location": "USA", "description": "Famous for the Statue of Liberty, Times Square, and Central Park.", "image": "images/new_york.jpg"},
        {"name": "Dubai", "location": "UAE", "description": "Known for luxury shopping, ultramodern architecture, and lively nightlife.", "image": "images/dubai.jpg"},
        {"name": "Venice", "location": "Italy", "description": "Unique for its canals, gondolas, and beautiful architecture.", "image": "images/venice.jpg"},

        {"name": "London", "location": "United Kingdom", "description": "Known for the Big Ben, Buckingham Palace, and the River Thames.", "image": "images/london.jpg"},
        {"name": "Bangkok", "location": "Thailand", "description": "Famous for vibrant street life, cultural landmarks, and grand palaces.", "image": "images/bangkok.jpg"},
        {"name": "Barcelona", "location": "Spain", "description": "Known for the architecture of Antoni Gaudí, including the Sagrada Familia.", "image": "images/barcelona.jpg"},
        {"name": "Machu Picchu", "location": "Peru", "description": "Ancient Inca city set high in the Andes Mountains, known for its stunning views.", "image": "images/machu_picchu.jpg"},
        {"name": "Istanbul", "location": "Turkey", "description": "Known for its historic sites such as the Hagia Sophia and Blue Mosque.", "image": "images/istanbul.jpg"},
        {"name": "Santorini", "location": "Greece", "description": "Famous for its whitewashed buildings, crystal-clear waters, and sunsets.", "image": "images/santorini.jpg"},
        {"name": "Berlin", "location": "Germany", "description": "Known for its historical landmarks such as the Berlin Wall and Brandenburg Gate.", "image": "images/berlin.jpg"},
        {"name": "Athens", "location": "Greece", "description": "Famous for ancient monuments like the Acropolis and Parthenon.", "image": "images/athens.jpg"}
    ]
    context = {"places": places, 'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'travel/gallery.html', context)

def feedback(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/feedback.html',context)

def accomodations(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/accomodations.html',context)

def agentRegistration(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/agentRegistration.html',context)

def contact(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/contact.html',context)

def customer(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/customer.html',context)

def privacy_policy(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/privacy_policy.html',context)

def terms_conditions(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/terms_conditions.html',context)

def mainPage(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/mainPage.html',context)