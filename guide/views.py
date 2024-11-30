from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import GuideRegistrationForm, GuideLoginForm
from .models import Guide
from django.conf import settings

def guide_registration(request):
    if request.method == 'POST':
        form = GuideRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
            else:
                guide = form.save(commit=False)
                guide.password = make_password(password)  
                guide.save()
                messages.success(request, "Registration successful!")
                return redirect('guide_login')  # Redirect to login page after successful registration
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GuideRegistrationForm()

    return render(request, 'guide_register.html', {'form': form,'MEDIA_URL': settings.MEDIA_URL})

def guide_login(request):
    if request.method == "POST":
        form = GuideLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                guide = Guide.objects.get(email=email)  
                if check_password(password, guide.password):
                    request.session['guide_id'] = guide.id  # Store guide ID in session for tracking
                    messages.success(request, "Login successful!")
                    return redirect('guide_dashboard')  # Redirect to guide dashboard after successful login
                else:
                    messages.error(request, "Invalid password.")
            except Guide.DoesNotExist:
                messages.error(request, "Guide profile doesn't exist.")
        else:
            messages.error(request, "Errors in the form.")
    else:
        form = GuideLoginForm()

    return render(request, 'guide_login.html', {'form': form,'MEDIA_URL': settings.MEDIA_URL})



def contact_support(request):    
    return render(request, 'contact.html', {'MEDIA_URL': settings.MEDIA_URL})


def guide_dashboard(request):
    return render(request, 'guide_dashboard.html', {'MEDIA_URL': settings.MEDIA_URL})

def guide_edit_profile(request):
    return render(request, 'guide_edit_profile.html',  {'MEDIA_URL': settings.MEDIA_URL})

def guide_edit_doctor_profile(request):
    return render(request, 'guide_edit_doctor_profile.html', {'MEDIA_URL': settings.MEDIA_URL})

