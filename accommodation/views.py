from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from .models import Hotel
from .forms import HotelOwnerRegistrationForm, HotelLoginForm

def hotel_owner_registration(request):
    country = None
    state = None
    city = None

    if request.method == 'POST':
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')

        form = HotelOwnerRegistrationForm(request.POST, country=country, state=state, city=city)

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
        form = HotelOwnerRegistrationForm(country=country, state=state, city=city)

    print(f"Country: {country}, State: {state}, City: {city}")

    return render(request, 'hotel_owner_register.html', {'form': form})


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
                    messages.success(request, "Login successful!")
                    return redirect('hotel_dashboard')
                else:
                    messages.error(request, "Invalid Password.")
            except hotel_owner.DoesNotExist:
                messages.error(request, "profile doesn't exists.")
        else:
            messages.error(request, "Errors in the form.")
    else:     
        form = HotelOwnerLoginForm()
    return render(request, 'hotel_owner_login.html', {'form':form})


def contact_support(request):    
    return render(request, 'contact.html')

def get_dashboard(request):
    return render(request, 'hotel_dashboard.html')

