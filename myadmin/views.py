from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from customer.models import Profile
from django.contrib import messages
from customer.forms import EditProfileForm  
from django.core.exceptions import PermissionDenied


def admin_login(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    print(f"Session expiry before login: {request.session.get_expiry_date()}")

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to the custom admin dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'adminPage.html', {'form': form, 'MEDIA_URL': settings.MEDIA_URL})


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        raise PermissionDenied
    users = User.objects.all()
    profiles = Profile.objects.all()
    return render(request, 'adminDashboard.html', {'users': users, 'profiles': profiles,'MEDIA_URL': settings.MEDIA_URL})


@login_required
def delete_user(request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        print("User deleted successfully!")
        messages.success(request,"User deleted successfully!")
        return redirect('admin_dashboard') 


@login_required
def toggle_staff_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    print(f"Before toggle: User {user.username} is {'staff' if user.is_staff else 'not staff'}")

    user.is_staff = not user.is_staff
    user.save()

    print(f"After toggle: User {user.username} is {'staff' if user.is_staff else 'not staff'}")
    
    return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        print("[DEBUG] Handling POST request for edit_user.")
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            profile.location = form.cleaned_data.get('location')
            profile.birth_date = form.cleaned_data.get('birth_date')
            profile.travel_preferences = form.cleaned_data.get('travel_preferences')
            profile.favorite_destinations = form.cleaned_data.get('favorite_destinations')
            profile.languages_spoken = form.cleaned_data.get('languages_spoken')
            profile.budget_range = form.cleaned_data.get('budget_range')
            profile.interests = form.cleaned_data.get('interests')
            profile.save()
            messages.success(request,"User profile updated successfully.")

            print("[DEBUG] User profile updated successfully.")
            return redirect('admin_dashboard')
    else:
        print("[DEBUG] Rendering edit form for GET request.")
        form = EditProfileForm(instance=user)
        form.fields['location'].initial = profile.location
        form.fields['birth_date'].initial = profile.birth_date
        form.fields['travel_preferences'].initial = profile.travel_preferences
        form.fields['favorite_destinations'].initial = profile.favorite_destinations
        form.fields['languages_spoken'].initial = profile.languages_spoken
        form.fields['budget_range'].initial = profile.budget_range
        form.fields['interests'].initial = profile.interests
        messages.success(request,"Rendering edit form.")

        print("[DEBUG] Rendered edit form.")

    return render(request, 'edit_user.html', {'form': form, 'user': user,'MEDIA_URL': settings.MEDIA_URL})


def admin_logout(request):
    logout(request)
    if 'is_admin' in request.session:
        del request.session['is_admin']
        print("Admin session deleted.")


    print(f"Session after logout: {request.session.items()}")  
    
    messages.success(request, 'You have logged out successfully.')
    return redirect('admin_login')

