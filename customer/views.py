from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import EditProfileForm, UserRegistrationForm
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid(): 
            Profile.objects.create(user=request.user)
            messages.success(request, "Your account has been created. You can now log in.")
            return redirect('login')  
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  
            else:
                messages.error(request, "user doesn't exists.")
                return redirect('register')
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()  

    return render(request, 'login.html', {'form': form})



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .models import Profile

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

    return render(request, 'edit_profile.html', {'form': form})



@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    user = request.user
    return render(request, 'home.html', {'profile': profile}, {'user': user})



