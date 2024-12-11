from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import GuideRegistrationForm, GuideLoginForm, GuideDetailsUpdateForm
from .forms import PlaceDetailsUpdateForm, PlaceImageForm
from .forms import DoctorDetailsUpdateForm, DoctorForm
from .models import Guide, Doctor, Place, Image
from functools import wraps
from django.shortcuts import redirect, render


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
                return view_func(request, guide_info=guide, *args, **kwargs)
            else:
                print("1st I'm here")
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
                    return view_func(request, guide_info=guide, *args, **kwargs)
            else:
                print("2nd I'm here")
                return redirect('guide_login')
    return wrapper


def is_super_guide(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('super_guide_id') and request.session.get('is_login'):
            try:
                guide_id =request.session.get('super_guide_id')
                guide = Guide.objects.get(id=guide_id)
            except Guide.DoesNotExist:
                return redirect('guide_login')
            return view_func(request, guide_info=guide, *args, **kwargs)
        else:
            return redirect('guide_login')
    return wrapper


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
        return render(request, 'get_place_info.html', {'place_exist': True,'place': place, 'guide': guide_info})
    else:
        request.session['place_exist'] = False
        messages.error(request, f"{guide_info.place} doesn't exist in database now.")
        return render(request, 'get_place_info.html', {'place_exist': False, 'guide': guide_info})


@is_super_guide
def update_place_info(request, place_id, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    place = Place.objects.filter(id=place_id, name=guide_info.place, city=guide_info.city,
                                 state=guide_info.state, country=guide_info.country).first()
    if place:
        if request.method == "POST":
            form = PlaceDetailsUpdateForm(request.POST, instance=place)
            if form.is_valid():
                form.save()
                messages.success(request, 'place information updated successfully.')
                return redirect('get_place_info')
            else:
                messages.error(request, "please enter valid details")
                return redirect('get_place_info')
        else:
            form = PlaceDetailsUpdateForm(instance=place)
        return render(request, 'update_place_info.html', {'form': form})
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
def get_images(request, place_id ,*args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    place = Place.objects.filter(id=place_id, name=guide_info.place, city=guide_info.city,
                                 state=guide_info.state, country=guide_info.country).first()
    if place:
        images = Image.objects.filter(place=place.id)
        if images:
            return render(request, 'place_images.html', {'images_exist': True,'images': images})
        else:
            return render(request, 'place_images.html', {'images_exist': False})
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
def add_place_image(request, place_id, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    place = Place.objects.filter(name=guide_info.place, city=guide_info.city,
                                 state=guide_info.state, country=guide_info.country).first()
    if place:
        if request.method == "POST":
            form = PlaceImageForm(request.POST, place_id=place.id)
            if form.is_valid():
                form.save()
                return redirect('get_images')
            else:
                messages.error(request, "please enter valid details")
                return redirect('get_images')
        else:
            form = PlaceImageForm(place_id=place.id)
        return render(request, 'place_image.html', {'form': form, 'guide': guide_info})
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
def delete_place_image(request, place_id, image_id, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    place = Place.objects.filter(name=guide_info.place, city=guide_info.city,
                                 state=guide_info.state, country=guide_info.country).first()
    if place:
        try:
            image = Image.objects.get(place=place.id, id=image_id)
            image.delete()
            messages.success(request, "Image deleted successfully.")
            return redirect('get_images')
        except Image.DoesNotExist:
            messages.error(request, "Image doesn't exists.")
            return redirect('get_images')
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

    
 
# <---------------------CONTACT------------------------------------->
@is_login
def contact_support(request, *args, **kwargs):
    guide_info = kwargs.pop('guide_info', None)
    return render(request, 'contact.html', {'guide': guide_info})

