from django.shortcuts import render,redirect
from django.http import JsonResponse
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
from django.contrib.auth import logout
from travelling.send_mail import send_confirmation_email
from django.contrib.auth.models import User

def user_login(request):
    try:
        user = User.objects.get(username=request.session['registered_user'])
        del request.session['registered_user']
        if not user.first_name:
            messages.error(request, "your profile created with empty data you can edit it after login with your username and password.")
    finally:
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
                    login(request, user)
                    return redirect('profile')  
                else:
                    messages.error(request, "user doesn't exists.")
                    return redirect('register')
            else:
                messages.error(request, "there is some Issue check your credentials again.")
        else:
            form = AuthenticationForm()  

        return render(request, 'travel/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            request.session['registered_user'] = username
            email = form.cleaned_data.get('email')
            additional_info = {
                'email': email,
            }
            send_confirmation_email(
                to_email=email, 
                user_type='customer', 
                username=username, 
                additional_info=additional_info,
            )
            messages.success(request, "Your account has been created. You can now log in.")
            return redirect('create_profile')  
        else:
            messages.error(request, form.errors)
    else:
        form = UserRegistrationForm()

    return render(request, 'travel/register.html', {'form': form})


def create_profile(request):
    try:
        username = request.session.get('registered_user')
        user = User.objects.get(username=username)
        profile, created = Profile.objects.get_or_create(user=user)
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'you have successfully registered and created profile please login')
                return redirect('login')
        else:
            form = EditProfileForm(instance=user)
        return render(request, 'travel/create_profile.html', {'form': form, 'profile': profile, 'user': user})
    except Exception as e:
        print(f"Error: {e}")
        return redirect('login')


@login_required
def edit_profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                if user != request.user:
                    form.add_error('email', 'This email is already in use.')
                else:
                    form.save()
                    if user_profile:
                        user_profile.location = form.cleaned_data.get('location')
                        user_profile.birth_date = form.cleaned_data.get(
                            'birth_date')
                        user_profile.travel_preferences = form.cleaned_data.get(
                            'travel_preferences')
                        user_profile.favorite_destinations = form.cleaned_data.get(
                            'favorite_destinations')
                        user_profile.languages_spoken = form.cleaned_data.get(
                            'languages_spoken')
                        user_profile.budget_range = form.cleaned_data.get(
                            'budget_range')
                        user_profile.interests = form.cleaned_data.get('interests')
                        user_profile.save()
                    else:
                        Profile.objects.create(
                            user=request.user,
                            location=form.cleaned_data.get('location'),
                            birth_date=form.cleaned_data.get('birth_date'),
                            travel_preferences=form.cleaned_data.get(
                                'travel_preferences'),
                            favorite_destinations=form.cleaned_data.get(
                                'favorite_destinations'),
                            languages_spoken=form.cleaned_data.get(
                                'languages_spoken'),
                            budget_range=form.cleaned_data.get('budget_range'),
                            interests=form.cleaned_data.get('interests')
                        )
                    messages.success(request, "Profile edited successfully!")
                    return redirect('profile')
            except User.DoesNotExist:
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

    return render(request, 'travel/edit_profile.html', {'form': form, 'profile': user_profile})


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


# <<<<<<<<<<<<<<< ACCOMMODATION WE NEED TO WORK ON THIS FOR CUSTOMER >>>>>>>>>>>>>>>>>>>>>
# <<<<<<< this view is just for testing >>>>>>>


def accomodations(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('accomodations')
        messages.success(request, "Accomodations request has been sent!")
        return redirect('accomodations')

    return render(request,'travel/accomodations.html')


def feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        messages.success(request, "Thank you for your feedback!")
        return redirect('feedback')
    
    return render(request,'travel/feedback.html')


#  From this section till end those are upcoming modules views. we have to add multiple apps to implement this.


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

