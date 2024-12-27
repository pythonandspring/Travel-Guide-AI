from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .models import Hotel, HotelImage, HotelRoom
from .forms import HotelOwnerRegistrationForm, HotelLoginForm, HotelImageForm, HotelRoomForm, HotelRoomUpdateForm, HotelDetailsUpdateForm
from django.urls import reverse
from travelling.send_mail import send_confirmation_email


def hotel_owner_registration(request):
    if request.method == 'POST':
        form = HotelOwnerRegistrationForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            hotel_name = form.cleaned_data.get('hotel_name')
            username = form.cleaned_data.get('hotel_owner_name')
            hotel_email = form.cleaned_data.get('hotel_email')
            to_mail = form.cleaned_data.get('owner_email')
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
            else:
                hotel_owner = form.save(commit=False)
                hotel_owner.password = make_password(password)
                hotel_owner.save()
                additional_info = {
                    'hotel_name': hotel_name,
                    'hotel_email': hotel_email,
                }
                send_confirmation_email(to_email=to_mail, user_type='hotel_owner',username=username, additional_info=additional_info)
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
                if check_password(password, hotel_owner.password) and hotel_owner:
                    request.session['hotel_owner_id'] = hotel_owner.id
                    request.session['is_logged_in'] = True
                    messages.success(request, "Login successful!")
                    return redirect('hotel_dashboard')
                else:
                    messages.error(request, "Invalid Password.")
                    return redirect("hotel_login")
            except Hotel.DoesNotExist:
                messages.error(request, "profile doesn't exists.")
                return redirect('hotel_login')
        else:
            messages.error(request, "Errors in the form.")
            return redirect('hotel_login')
    else:
        form = HotelLoginForm()
    return render(request, 'hotel_login.html', {'form': form})


def contact_support(request):
    return render(request, 'contact_support.html')


def hotel_dashboard(request):
    if request.session['hotel_owner_id']:
        hotel_owner = Hotel.objects.get(id=request.session['hotel_owner_id'])
        return render(request, 'hotel_dashboard.html', {'hotel_owner': hotel_owner})
    else:
        return render(request, 'hotel_login')


def hotel_images(request):
    if 'hotel_owner_id' in request.session:
        hotel_id = request.session.get('hotel_owner_id')

        hotel_images = HotelImage.objects.filter(hotel_id=hotel_id)

        if hotel_images.exists():
            return render(request, "hotel_images.html", {'hotel_images': hotel_images})
        else:
            return render(request, "hotel_images.html", {'no_image': True})
    else:
        return redirect('login')


def add_hotel_images(request):
    if request.session['hotel_owner_id']:
        hotel_id = request.session.get('hotel_owner_id')
        if request.method == "POST":
            form = HotelImageForm(request.POST, request.FILES, hotel_id=hotel_id)
            if form.is_valid:
                form.save()
                messages.success(request, "You have added new image")
                return redirect('hotel_images')
            else:
                messages.success(request, "Please enter correct input.")
        else:
            form = HotelImageForm(hotel_id=hotel_id)
        return render(request, 'hotel_image_upload.html', {'upload_form': form})
    else:
        return redirect('hotel_login')
    

def delete_hotel_image(request, image_id):
    if 'hotel_owner_id' not in request.session:
        messages.error(
            request, "You must be logged in to perform this action.")
        return redirect('hotel_login')

    hotel_id = request.session['hotel_owner_id']
    image = get_object_or_404(HotelImage, id=image_id, hotel_id=hotel_id)

    try:
        image.delete()
        messages.success(request, "Image deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the image: {e}")

    return redirect('hotel_images')


def rename_hotel_image(request, image_id):
    if 'hotel_owner_id' not in request.session:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('hotel_login')

    hotel_id = request.session.get('hotel_owner_id')
    image = get_object_or_404(HotelImage, id=image_id, hotel_id=hotel_id)

    if request.method == 'POST':
        try:
            new_name = request.POST.get('new_name')

            image.name = new_name
            image.save()

            messages.success(request, "Image renamed successfully.")

            return redirect('hotel_images')

        except Exception as e:
            messages.error(request, f"An error occurred while renaming the image: {e}")
            return redirect('hotel_images')

    return redirect('hotel_images')


def hotel_image_popup(request, image_id):
    if 'hotel_owner_id' not in request.session:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('hotel_login')

    hotel_id = request.session.get('hotel_owner_id')
    image = get_object_or_404(HotelImage, id=image_id, hotel_id=hotel_id)

    return render(request, 'hotel_image_popup.html', {'image': image})


def hotel_logout(request):
    if request.session['hotel_owner_id']:
        del request.session['hotel_owner_id']
        request.session['is_logged_in'] = False
        messages.success(request, "You have been logged out successfully.")
    return redirect('hotel_login')


def available_rooms(request):
    if request.session['hotel_owner_id']:
        hotel_id = request.session['hotel_owner_id']
        try:
            rooms = HotelRoom.objects.filter(hotel=hotel_id)
            return render(request, 'hotel_rooms.html', {'rooms': rooms})
        except HotelRoom.DoesNotExist:
            return render(request, 'hotel_rooms.html', {'no_rooms': True})
    else:
        return redirect('hotel_login')
    

def add_room_type(request):
    if 'hotel_owner_id' in request.session:
        hotel_id = request.session['hotel_owner_id']

        if request.method == "POST":
            form = HotelRoomForm(request.POST, hotel_id=hotel_id)
            if form.is_valid():
                total_rooms = form.cleaned_data.get('total_rooms')
                available_rooms = form.cleaned_data.get('available_rooms')
                room_category = form.cleaned_data.get('room_category')
                room_type = form.cleaned_data.get('room_type')

                try:
                    existing_room = HotelRoom.objects.get(
                        hotel_id=hotel_id, room_category=room_category, room_type=room_type
                    )
                    messages.success(
                        request, "Room category already present. Please update if you want to modify."
                    )
                    return redirect(reverse('update_room_details', args=[existing_room.id]))
                except HotelRoom.DoesNotExist:
                    if total_rooms >= available_rooms:
                        form.save()
                        messages.success(request, "You have added a new room category.")
                        return redirect('available_rooms')
                    else:
                        messages.error(request, 'you have added available rooms greater than total rooms.')
                        return redirect('available_rooms')
            else:
                messages.error(request, "You should enter valid details.")
                return redirect('available_rooms')
        else:
            form = HotelRoomForm(hotel_id=hotel_id)
            return render(request, 'hotel_add_room.html', {'hotel_room_form': form})

    else:
        return redirect('hotel_login')


def delete_room_type(request, room_id):
    if request.session['hotel_owner_id']:
        room = get_object_or_404(HotelRoom, id=room_id)
        room.delete()
        messages.success(request, f'you have deleted {room.room_category}, {room.room_type} room.')
        return redirect('available_rooms')


def update_room(request, room_id):
    if request.session.get('hotel_owner_id'): 
        try:
            room = HotelRoom.objects.get(id=room_id)
        except HotelRoom.DoesNotExist:
            messages.error(request, "The room does not exist.")
            return redirect('available_rooms')

        if request.method == 'POST':
            form = HotelRoomUpdateForm(request.POST, instance=room)
            if form.is_valid():
                form.save()
                messages.success(request, f"Details updated for {room.room_category}, {room.room_type}.")
                return redirect('available_rooms')
            else:
                messages.error(request, "Please correct the errors in the form.")
        else:
            form = HotelRoomUpdateForm(instance=room)

        return render(request, 'update_room_details.html', {'update_form': form, "room_obj": room})
    else:
        messages.error(request, "You need to log in first.")
        return redirect('hotel_login')
                
                
def update_hotel_details(request):
    hotel_owner_id = request.session.get('hotel_owner_id')
    if not hotel_owner_id:
        return redirect('hotel_login')

    hotel = get_object_or_404(Hotel, id=hotel_owner_id)

    if request.method == "POST":
        form = HotelDetailsUpdateForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, "Details updated successfully.")
            return redirect('hotel_dashboard')
        else:
            messages.error(request, "Please enter valid details.")
    else:
        form = HotelDetailsUpdateForm(instance=hotel)

    return render(request, 'update_hotel_details.html', {'hotel_details_form': form, 'hotel_details': hotel})
    



