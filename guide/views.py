from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import GuideRegistrationForm, GuideLoginForm
from .models import Guide


def guide_registration(request):
    if request.method == 'POST':
        form = GuideRegistrationForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
            else:
                hotel_owner = form.save(commit=False)
                hotel_owner.password = make_password(password)  
                hotel_owner.save()
                messages.success(request, "Registration successful!")
                return redirect('guide_login')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GuideRegistrationForm()

    return render(request, 'guide_register.html', {'form': form})


def guide_login(request):
    if request.method == "POST":
        form = GuideLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                guide = Guide.objects.get(email=email)  
                if check_password(password, guide.password):
                    if guide.is_super_guide:
                        request.session['super_guide_id'] = guide.id 
                    else:
                        request.session['guide_id'] = guide.id  
                    request.session['is_logged_in'] = True
                    messages.success(request, "Login successful!")
                    return redirect('guide_dashboard')  
                else:
                    messages.error(request, "Invalid password.")
            except Guide.DoesNotExist:
                messages.error(request, "Guide profile doesn't exist.")
        else:
            messages.error(request, "Errors in the form.")
    else:
        form = GuideLoginForm()

    return render(request, 'guide_login.html', {'form': form})


def guide_logout(request):
    if request.session['guide_id']:
        del request.session['guide_id']
        messages.success(request, "You have been logged out successfully.")  
    elif request.session['super_guide_id']:
        del request.session['super_guide_id']
        messages.success(request, "You have been logged out successfully.")
    request.session['is_logged_in'] = False
    return redirect('guide_login')


def contact_support(request):    
    return render(request, 'contact.html')


def guide_dashboard(request):
    return render(request, 'guide_dashboard.html')


def guide_edit_profile(request):
    return render(request, 'guide_edit_profile.html')


def guide_edit_doctor_profile(request):
    return render(request, 'guide_edit_doctor_profile.html')

