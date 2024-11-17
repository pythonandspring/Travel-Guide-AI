from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.models import User

from .forms import EditProfileForm, UserRegistrationForm
from .models import Profile


from .forms import EditProfileForm, UserRegistrationForm

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

    # Debugging session expiry
    print(f"Session expiry before login: {request.session.get_expiry_date()}")

    # If the user is already logged in as admin, redirect to dashboard
    if request.user.is_authenticated or request.session.get('is_admin'):
        print("Admin is already logged in.")
        return redirect('admin_dashboard')  # Redirect to dashboard if logged in as admin

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if both fields have a minimum of 4 characters
        if len(username) >= 4 and len(password) >= 4:
            if username == 'admin' and password == 'admin':
                    request.session['is_admin'] = True
                    print(f"Session data after setting is_admin: {request.session.items()}")
                    print(f"Session expiry after login: {request.session.get_expiry_date()}")
                    return redirect('admin_dashboard')  # Redirect to dashboard
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Both username and password must be at least 4 characters long.')

    return render(request, 'travel/adminPage.html', context)




def admin_dashboard(request):
    # Print session data on every request
    print(f"Session data on dashboard page: {request.session.items()}")

    # Check if the user is logged in as admin
    if not request.session.get('is_admin'):
        messages.error(request, 'You need to log in as an admin first.')
        return redirect('admin_login')  # Redirect to login page if not an admin
    
    users = User.objects.all()
    profiles = Profile.objects.all()

    # Render the admin dashboard
    return render(
        request, 
        'travel/adminDashboard.html', 
        {'users': users, 'profiles': profiles,'MEDIA_URL': settings.MEDIA_URL},
    )


def admin_logout(request):
    # If using Django's User model for authentication

    print(f"Session before logout: {request.session.items()}")

    logout(request)  # This will clear the session data
    
    # Clear the admin-specific session if manually set
    if 'is_admin' in request.session:
        del request.session['is_admin']
        print("Admin session deleted.")


    print(f"Session after logout: {request.session.items()}")  
    
    messages.success(request, 'You have logged out successfully.')
    return redirect('admin_login')






def is_admin_user(user):
    return user.is_authenticated and user.is_staff

def edit_user(request, user_id):
    print(f"[DEBUG] Current user: {request.user.username}, is_staff: {request.user.is_staff}")
    print(f"[DEBUG] Accessing edit_user with user: {request.user}, is_staff: {request.user.is_staff}")
    print(f"[DEBUG] Session data: {request.session.items()}")
    print(f"[DEBUG] Request method: {request.method}")

    user = get_object_or_404(User, id=user_id)

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        print("[DEBUG] Handling POST request for edit_user.")
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            profile.location = form.cleaned_data.get('location')
            profile.birth_date = form.cleaned_data.get('birth_date')
            profile.travel_preferences = form.cleaned_data.get('travel_preferences')
            profile.favorite_destinations = form.cleaned_data.get('favorite_destinations')
            profile.languages_spoken = form.cleaned_data.get('languages_spoken')
            profile.budget_range = form.cleaned_data.get('budget_range')
            profile.interests = form.cleaned_data.get('interests')
            profile.save()
            print("[DEBUG] User profile updated successfully.")
            return redirect('admin_dashboard')
    else:
        print("[DEBUG] Rendering edit form for GET request.")
        form = EditProfileForm(instance=user)
        form.fields['location'].initial = profile.location
        form.fields['birth_date'].initial = profile.birth_date
        form.fields['travel_preferences'].initial = profile.travel_preferences
        form.fields['favorite_destinations'].initial = profile.favorite_destinations
        form.fields['languages_spoken'].initial = profile.languages_spoken
        form.fields['budget_range'].initial = profile.budget_range
        form.fields['interests'].initial = profile.interests
        print("[DEBUG] Rendering edit form.")

    return render(request, 'travel/edit_user.html', {'form': form, 'user': user,'MEDIA_URL': settings.MEDIA_URL})







def delete_user(request, user_id):
    if request.user.is_staff:  # Ensure only staff can delete users
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('admin_dashboard')  # Adjust to the correct URL name for your admin dashboard
    else:
        return redirect('login')  # Redirect non-staff users to login or another page














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




#login, register (only for customer...)
# def customer(request):
#     context = {
#         'MEDIA_URL': settings.MEDIA_URL,
#     }
#     return render(request,'travel/customer.html',context)



# #after login,
# def mainPage(request):
#     context = {
#         'MEDIA_URL': settings.MEDIA_URL,
#     }
#     return render(request,'travel/mainPage.html',context)




#login
def user_login(request):
    if request.user.is_authenticated: 
        return redirect('profile') 
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("DEBUG: Login form is valid")

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            print("DEBUG: Username and password extracted") 

            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("DEBUG: Authentication successful for user:", user.username)

                login(request, user)
                return redirect('profile')  
            else:
                print("DEBUG: Authentication failed")
                messages.error(request, "user doesn't exists.")
                return redirect('register')
        else:
            print("DEBUG: Login form is invalid")  
            print("DEBUG: Errors -", form.errors) 
            messages.error(request, "Invalid login credentials.")
    else:
        print("DEBUG: GET request received for login")
        form = AuthenticationForm()  

    return render(request, 'travel/login.html', {'form': form,'MEDIA_URL': settings.MEDIA_URL})

#register
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("DEBUG: Form is valid")
            print("DEBUG: Form data -", form.cleaned_data)
            # form.save()  .

            user = form.save()
            Profile.objects.create(user=user)

            messages.success(request, "Your account has been created. You can now log in.")
            print("DEBUG: User registration successful")  
            return redirect('login')  
        else:
            print("DEBUG: Form is invalid")
            print("DEBUG: Errors -", form.errors)
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

    user = request.user
    return render(
        request,
        'travel/profile.html',
        {
            'profile': profile,
            'MEDIA_URL': settings.MEDIA_URL,
            'user': request.user,  # Pass the user directly
        }
    )
    # profile = Profile.objects.get(user=request.user)
    

