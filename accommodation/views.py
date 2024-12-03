from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .models import Hotel, HotelImage, HotelRoom
from .forms import HotelOwnerRegistrationForm, HotelLoginForm, HotelImageForm
from time import sleep

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
                hotel_owner = get_object_or_404(Hotel, hotel_email=email)  
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


def hotel_images(request):
    if request.session['hotel_owner_id']:
        try:
            hotel_images = HotelImage.objects.get(hotel_id = request.session['hotel_owner_id'])
            return (request, "hotel_images.html", {'hotel_images': hotel_images})
        except:
            return redirect('add_hotel_image')

def add_hotel_images(request):
    if request.session['hotel_owner_id']:
        hotel_id = request.session.get('hotel_owner_id')
        if request.method == "POST":
            form = HotelImageForm(request.POST, request.FILES, hotel_id=hotel_id)
            if form.is_valid:
                form.save()
                messages.success(request, "You have added new image")
                return redirect('hotel_image.html')
            else:
                messages.success(request, "Please enter correct input.")
        else:
            form = HotelImageForm(hotel_id=hotel_id)
        return render(request, 'hotel_image_upload.html', {form:form})
    else:
        return redirect('hotel_login')
    



def delete_hotel_image(request, image_id):
    if 'hotel_owner_id' not in request.session:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('hotel_login')

    hotel_id = request.session['hotel_owner_id']
    image = get_object_or_404(HotelImage, id=image_id, hotel_id=hotel_id)

    try:
        image.delete()
        messages.success(request, "Image deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the image: {e}")

    return redirect('hotel_login')


def hotel_logout(request):
    if request.session['hotel_owner_id']:
        del request.session['hotel_owner_id']
        request.session['is_logged_in'] = False
        messages.success(request, "You have been logged out successfully.")  
    return redirect('hotel_login')