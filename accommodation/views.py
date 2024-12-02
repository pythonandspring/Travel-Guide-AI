from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from .models import Hotel
from .forms import HotelOwnerRegistrationForm, HotelLoginForm

def hotel_owner_registration(request):
    if request.method == 'POST':
        form = HotelOwnerRegistrationForm(request.POST)

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
                return redirect('hotel_login')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = HotelOwnerRegistrationForm()

    return render(request, 'hotel_register.html', {'form': form})


def hotel_login(request):
    if request.method == "POST":
        form = HotelLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                hotel_owner = Hotel.objects.get(hotel_email=email)   
                if check_password(password, hotel_owner.password):
                    request.session['hotel_owner_id'] = hotel_owner.id 
                    request.session['is_logged_in'] = True
                    messages.success(request, "Login successful!")
                    return redirect('hotel_dashboard')
                else:
                    messages.error(request, "Invalid Password.")
            except hotel_owner.DoesNotExist:
                messages.error(request, "profile doesn't exists.")
        else:
            messages.error(request, "Errors in the form.")
    else:     
        form = HotelLoginForm()
    return render(request, 'hotel_login.html', {'form':form})

def contact_support(request):    
    return render(request, 'contact_support.html')


def hotel_dashboard(request):
    if request.session['hotel_owner_id']:
        hotel_owner = Hotel.objects.get(id = request.session['hotel_owner_id'])
        return render(request, 'hotel_dashboard.html', {'hotel_owner': hotel_owner})
    else:
        return render(request, 'hotel_login')


def hotel_logout(request):
    if request.session['hotel_owner_id']:
        del request.session['hotel_owner_id']
        request.session['is_logged_in'] = False
        messages.success(request, "You have been logged out successfully.")  
    return redirect('hotel_login')

def hotel_images(request):
    # images = HotelImage.objects.all()
    return render(request, 'hotel_images.html')