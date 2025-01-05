from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password, PBKDF2PasswordHasher
from .forms import GuideRegistrationForm, GuideLoginForm, GuideDetailsUpdateForm
from .forms import PlaceDetailsUpdateForm, PlaceImageForm
from .forms import DoctorDetailsUpdateForm, DoctorForm
from .models import Guide, Doctor, Place, Image
from functools import wraps
from django.shortcuts import redirect, render
from django.conf import settings
from travelling.send_mail import send_confirmation_email
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from .models import PasswordResetToken
from .forms import PasswordResetRequestForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import ResetPasswordForm

# <---------------------GUIDE------------------------------------->
def is_login(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        guide_id = kwargs.pop('guide_id', None)
        if guide_id:
            try:
                guide = Guide.objects.get(id=guide_id)
            except Guide.DoesNotExist:
                return redirect('guide_login')
            if guide.is_super_guide:
                return view_func(request, *args, guide_info=guide, **kwargs)
            else:
                return redirect('guide_login')
        else:
            if request.session.get('super_guide_id') or request.session.get('guide_id'):
                try:
                    guide_id = request.session.get('super_guide_id')
                    guide = Guide.objects.get(id=guide_id)
                except Guide.DoesNotExist:
                    guide_id = request.session.get('guide_id')
                    guide = Guide.objects.get(id=guide_id)
                finally:
                    return view_func(request, *args, guide_info=guide, **kwargs)
            else:
                return redirect('guide_login')
    return wrapper


def is_super_guide(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if (request.session.get('super_guide_id') or request.session.get('guide_id')) and request.session.get('is_login'):
            try:
                guide_id =request.session.get('super_guide_id')
                guide = Guide.objects.get(id=guide_id)
                if guide.is_super_guide:
                    return view_func(request, *args, guide_info=guide, **kwargs)
            except Guide.DoesNotExist:
                try:
                    guide_id = request.session.get('guide_id')
                    guide = Guide.objects.get(id=guide_id)
                    if guide.is_super_guide:
                        return view_func(request, *args, guide_info=guide, **kwargs)
                except Guide.DoesNotExist:
                    return redirect('guide_login')
        else:
            return redirect('guide_login')
    return wrapper


def guide_registration(request):
    if request.method == 'POST':
        form = GuideRegistrationForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            guide_name =  form.cleaned_data.get('name')
            place_name = form.cleaned_data.get('place')
            guide_email = form.cleaned_data.get('email')

            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
            else:
                hotel_owner = form.save(commit=False)
                hotel_owner.password = make_password(password)  
                hotel_owner.save()
                additional_info = {
                    'place_name': place_name,
                    'guide_name': guide_name,
                    'guide_email': guide_email,
                }
                send_confirmation_email(to_email=guide_email, user_type='guide', username=guide_name, additional_info=additional_info)
                messages.success(request, "Registration successful!")
                return redirect('guide_login')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GuideRegistrationForm()

    return render(request, 'guide_register.html', {'form': form})


def guide_login(request):
    
    if (request.session.get('super_guide_id') or request.session.get('guide_id')) and request.session.get('is_login'):
        return redirect('guide_dashboard')
    else:
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
                        request.session['is_login'] = True
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


@is_login
def guide_logout(request, *args, **kwargs):
    try:
        del request.session['guide_id']
        messages.success(request, "You have been logged out successfully.")
    except KeyError:
        del request.session['super_guide_id']
        messages.success(request, "You have been logged out successfully.")
        
    request.session['is_login'] = False
    return redirect('guide_login')


@is_login
def guide_dashboard(request, *args,**kwargs):
    guide_info = kwargs.pop('guide_info', None)    
    return render(request, 'guide_dashboard.html', {'guide': guide_info})


@is_login
def guide_edit_profile(request, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    try:
        guide = Guide.objects.get(id=guide_info.id)
        if request.method == "POST":
            form = GuideDetailsUpdateForm(request.POST, instance=guide)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                try:
                    guide_new = Guide.objects.get(email=email)
                    if guide_new != guide:
                        form.add_error('email', 'this email is already in use')
                    else:
                        form.save()
                        messages.success(request, 'profile updated successfully.')
                        return redirect('guide_dashboard')
                except Guide.DoesNotExist:
                    form.save()
                    messages.success(request, 'profile updated successfully.')
                    return redirect('guide_dashboard')
            else:
                messages.error(request, "profile can't update.")
                return redirect('guide_dashboard')
        else:
            form = GuideDetailsUpdateForm(instance=guide)
        return render(request, 'guide_edit_profile.html', {'form': form, 'guide':guide})
    except:
        return redirect('guide_login')
    

@is_login
def gallery(request, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    places = Place.objects.all()

    # Extract distinct city, state, and country values
    cities = places.values_list('city', flat=True).distinct()
    states = places.values_list('state', flat=True).distinct()
    countries = places.values_list('country', flat=True).distinct()

    context = {
        'places': places,
        'cities': cities,
        'states': states,
        'countries': countries,
        'guide': guide_info,
    }

    return render(request, 'gallery.html', context)


# <---------------------DOCTOR------------------------------------->


@is_super_guide
def get_doctors(request, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    try:
        doctors = Doctor.objects.filter(guide=guide_info.id)
    except Doctor.DoesNotExist:
        return render(request, 'get_doctors.html', {'doctors': None})
    return render(request, 'get_doctors.html', {'doctors': doctors, 'guide': guide_info})


@is_super_guide
def add_doctor(request, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    if guide_info:
        guide_id = guide_info.id
        if request.method == "POST":
            form = DoctorForm(request.POST, guide_id=guide_id)
            if form.is_valid():
                form.save()
                messages.success(request, 'You have added a new doctor.')
                return redirect('get_doctors')
            else:
                messages.error(request, "Please provide valid details.")
        else:
            form = DoctorForm(guide_id=guide_id)
        return render(request, 'add_doctor.html', {'doctor_form': form, 'guide': guide_info})
    else:
        messages.error(
            request, "You are not authorized to perform this action.")
        return redirect('login')


@is_super_guide
def update_doctor_details(request, doctor_id, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    doctor = Doctor.objects.filter(id=doctor_id, guide=guide_info.id).first()
    if request.method == "POST":
        form = DoctorDetailsUpdateForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Information for doctor {doctor.name} is updated.')
            return redirect('get_doctors')
        else:
            messages.error(request, 'please enter valid deatils')
    else:
        form = DoctorDetailsUpdateForm(instance=doctor)
    return render(request, 'update_doctor.html', {'form': form, 'doctor_obj': doctor, 'guide': guide_info})
    

@is_super_guide
def delete_doctor(request, doctor_id, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    doctor = Doctor.objects.filter(id=doctor_id, guide=guide_info.id).first()

    if doctor:
        doctor.delete()
        return redirect('get_doctors')
    else:
        messages.error(request, "Doctor Doesn't exist.")
        return redirect('get_doctors')



# <---------------------PLACE------------------------------------->


@is_login
def get_place_info(request, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    place = Place.objects.filter(name=guide_info.place, city=guide_info.city, state=guide_info.state, country= guide_info.country).first()
    if place:
        request.session['place_exist'] = True
        return render(request, 'get_place_info.html', {'place_exist': True, 'place': place, 'guide': guide_info, 'MEDIA_URL': settings.MEDIA_URL})
    else:
        request.session['place_exist'] = False
        messages.error(request, f"{guide_info.place} doesn't exist in database now.")
        return render(request, 'get_place_info.html', {'place_exist': False, 'guide': guide_info, 'MEDIA_URL': settings.MEDIA_URL})


@is_super_guide
def update_place_info(request, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)

    # Retrieve place based on guide_info
    place = Place.objects.filter(
        name=guide_info.place,
        city=guide_info.city,
        state=guide_info.state,
        country=guide_info.country
    ).first()

    if not place:  # If the place doesn't exist
        messages.error(
            request, "You are not authorized to see or modify this place.")
        guide_place_info = {
            'place': guide_info.place,
            'city': guide_info.city,
            'state': guide_info.state,
            'country': guide_info.country
        }
        return render(request, 'get_place_info.html', {
            'place_exist': False,
            'guide_place_info': guide_place_info,
            'guide': guide_info
        })

    # Handle form submission
    if request.method == "POST":
        form = PlaceDetailsUpdateForm(request.POST, instance=place)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Place information updated successfully.')
            return redirect('get_place_info')
        else:
            messages.error(request, "Please enter valid details.")
            return redirect('update_place_info')

    # Render the update form with the existing place data
    form = PlaceDetailsUpdateForm(instance=place)
    return render(request, 'update_place_info.html', {'form': form, 'guide': guide_info})


@is_super_guide
def get_images(request, place_id ,*args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    place = Place.objects.get(id=place_id, name=guide_info.place, city=guide_info.city,
                                 state=guide_info.state, country=guide_info.country)
    print(place.id)
    if place:
        images = Image.objects.filter(place=place.id)
        if images:
            return render(request, 'place_images.html', {'images_exist': True, 'images': images, 'place': place})
        else:
            return render(request, 'place_images.html', {'images_exist': False, 'place': place})
    else:
        request.session['place_exist'] = False
        guide_place_info = {
            'place': guide_info.place,
            'city': guide_info.city,
            'state': guide_info.state,
            'country': guide_info.country
        }
        messages.error(request, "place doesn't exist.")
        return render(request, 'get_place_info.html', {'place_exist': False, 'guide_place_info': guide_place_info, 'guide': guide_info})


@is_super_guide
def add_place_image(request, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)

    # Attempt to find the place based on guide_info
    place = Place.objects.filter(
        name=guide_info.place,
        city=guide_info.city,
        state=guide_info.state,
        country=guide_info.country
    ).first()

    # If place is found, proceed to handle image upload
    if place:
        if request.method == "POST":
            form = PlaceImageForm(
                request.POST, request.FILES, place_id=place.id)
            if form.is_valid():
                form.save()  # Save the image instance
                messages.success(request, "Image added successfully!")
                return redirect('get_images', place_id=place.id)
            else:
                messages.error(request, "Please enter valid details.")
                return redirect('get_images', place_id=place.id)
        else:
            form = PlaceImageForm(place_id=place.id)

        return render(request, 'place_image.html', {'form': form, 'guide': guide_info})

    else:
        # Handle the case where the place does not exist
        request.session['place_exist'] = False
        guide_place_info = {
            'place': guide_info.place,
            'city': guide_info.city,
            'state': guide_info.state,
            'country': guide_info.country
        }
        messages.error(request, "Place does not exist.")
        return render(request, 'place/place_info.html', {'place_exist': False, 'guide_place_info': guide_place_info, 'guide': guide_info})


@is_super_guide
def delete_place_image(request, place_id, image_id, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    place = Place.objects.filter(name=guide_info.place, city=guide_info.city,
                                 state=guide_info.state, country=guide_info.country).first()
    if place:
        try:
            image = Image.objects.get(place=place.id, id=image_id)
            image.delete()
            messages.success(request, "Image deleted successfully.")
            return redirect('get_images', place_id=place_id)
        except Image.DoesNotExist:
            messages.error(request, "Image doesn't exists.")
            return redirect('get_images', place_id=place_id)
    else:
        request.session['place_exist'] = False
        guide_place_info = {
            'place': guide_info.place,
            'city': guide_info.city,
            'state': guide_info.state,
            'country': guide_info.country
        }
        messages.error(request, "place doesn't exist.")
        return render(request, 'place/place_info', {'place_exist': False, 'guide_place_info': guide_place_info, 'guide': guide_info})


@is_super_guide
def place_image_popup(request, place_id, image_id,  *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    place = Place.objects.filter(name=guide_info.place, city=guide_info.city,
                                 state=guide_info.state, country=guide_info.country).first()

    place_id = place_id
    image = get_object_or_404(Image, id=image_id, place_id=place_id)

    return render(request, 'place_Image_add_popup.html', {'image': image})

 
# <--------------------------------- CONTACT ------------------------------------->


@is_login
def contact_support(request, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    return render(request, 'contact.html', {'guide': guide_info})


# <--------------------------- RESET PASSWORD ------------------------------>
# for password reset
def request_password_reset(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                guide = Guide.objects.get(email=email)
                token, created = PasswordResetToken.objects.get_or_create(guide=guide)
                reset_link = f"http://127.0.0.1:8000/guide/reset-password/{token.token}/"
                send_mail(
                    "Password Reset Request",
                    f"Click the link to reset your password: {reset_link}",
                    "noreply@yourdomain.com",
                    [email]
                )
                return render(request, "password_reset_sent.html")
            except Guide.DoesNotExist:
                return render(request, "password_reset_request.html", {"form": form, "error": "Email not found."})
    else:
        form = PasswordResetRequestForm()
    return render(request, "password_reset_request.html", {"form": form})


# for password view
def reset_password(request, token):
    token_obj = get_object_or_404(PasswordResetToken, token=token)
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password == confirm_password:
                guide = token_obj.guide
                guide.password = make_password(new_password)
                guide.save()
                token_obj.delete()
                return render(request, "password_reset_complete.html")
            else:
                return render(request, "reset_password.html", {"form": form, "error": "Passwords do not match."})
    else:
        form = ResetPasswordForm()
    return render(request, "reset_password.html", {"form": form})

