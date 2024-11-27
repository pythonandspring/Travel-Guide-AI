from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import EditProfileForm, UserRegistrationForm
from django.contrib.auth import views as auth_views
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
import json


def user_login(request):
    if request.user.is_authenticated: 
        messages.success(request, "User is already authenticated, redirecting to profile..")
        return redirect('profile') 
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                messages.success(request, "Authentication successful for user!")
                login(request, user)
                return redirect('profile')  
            else:
                messages.error(request, "user doesn't exists.")
                return redirect('register')
        else:
            messages.error(request, form.errors)
    else:
        print("DEBUG: GET request received for login")
        form = AuthenticationForm()  

    return render(request, 'travel/login.html', {'form': form,'MEDIA_URL': settings.MEDIA_URL})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)

            messages.success(request, "Your account has been created. You can now log in.")
            return redirect('login')  
        else:
            messages.error(request, form.errors)
    else:
        print("DEBUG: GET request received for register") 
        form = UserRegistrationForm()

    return render(request, 'travel/register.html', {'form': form,'MEDIA_URL': settings.MEDIA_URL})


@login_required
def edit_profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if user_profile:
                user_profile.location = form.cleaned_data.get('location')
                user_profile.birth_date = form.cleaned_data.get('birth_date')
                user_profile.travel_preferences = form.cleaned_data.get('travel_preferences')
                user_profile.favorite_destinations = form.cleaned_data.get('favorite_destinations')
                user_profile.languages_spoken = form.cleaned_data.get('languages_spoken')
                user_profile.budget_range = form.cleaned_data.get('budget_range')
                user_profile.interests = form.cleaned_data.get('interests')
                user_profile.save()
            else:
                Profile.objects.create(
                    user=request.user,
                    location=form.cleaned_data.get('location'),
                    birth_date=form.cleaned_data.get('birth_date'),
                    travel_preferences=form.cleaned_data.get('travel_preferences'),
                    favorite_destinations=form.cleaned_data.get('favorite_destinations'),
                    languages_spoken=form.cleaned_data.get('languages_spoken'),
                    budget_range=form.cleaned_data.get('budget_range'),
                    interests=form.cleaned_data.get('interests')
                )
            messages.success(request, "Profile edited successfully!")
            return redirect('profile')  
    else:

        form = EditProfileForm(instance=request.user)
        if user_profile:
            form.fields['location'].initial = user_profile.location
            form.fields['birth_date'].initial = user_profile.birth_date
            form.fields['travel_preferences'].initial = user_profile.travel_preferences
            form.fields['favorite_destinations'].initial = user_profile.favorite_destinations
            form.fields['languages_spoken'].initial = user_profile.languages_spoken
            form.fields['budget_range'].initial = user_profile.budget_range
            form.fields['interests'].initial = user_profile.interests


    return render(request, 'travel/edit_profile.html', {'form': form,'MEDIA_URL': settings.MEDIA_URL})


@login_required
def user_profile(request):

    print(request.user)

    try:
        profile = request.user.profile  
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    return render(
        request,
        'travel/profile.html',
        {
            'profile': profile,
            'MEDIA_URL': settings.MEDIA_URL,
            'user': request.user, 
        }
    )

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)  
        messages.success(request, "You have been logged out successfully.")  
    return redirect('login')


class CustomPasswordResetView(auth_views.PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(settings.MEDIA_URL)  
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(settings.MEDIA_URL)  
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(settings.MEDIA_URL)  
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(settings.MEDIA_URL)  
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context




#  From this section till end those are upcoming modules views. we have to add multiple apps to implement this.
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

    messages.warning(request,"Loading assets, please hold on")

    context = {"places": places, 'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'travel/gallery.html', context)

def feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        messages.success(request, "Thank you for your feedback!")
        return redirect('feedback')
    
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request,'travel/feedback.html',context)

def accomodations(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('accomodations')
        messages.success(request, "Accomodations request has been sent!")
        return redirect('accomodations')
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/accomodations.html',context)

def agentRegistration(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('agentRegistration')
        messages.success(request, "Agent Registration request has been sent!")
        return redirect('agentRegistration')
    
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/agentRegistration.html',context)

def contact(request):    
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/contact.html',context)

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


    
@csrf_exempt
def search_voice(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            query = data.get('query', '')
            print(f"Voice Search Query: {query}")
            return JsonResponse({'status': 'success', 'query': query})

        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


