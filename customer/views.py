from django.shortcuts import render,redirect

#to view response on browser
from django.http import HttpResponse

# To use Django's messaging system
from django.contrib import messages  

# Create your views here.
#REVERSE - AVOID HARDCODING THE URLS 
from django.urls import reverse

#for image!
from django.conf import settings

def test(request):
    return HttpResponse("ok.")

def guide(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'travel/index.html',context)

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')  # Use the correct URL name

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin':
            # Successful login logic
            request.session['is_admin'] = True
            return redirect(reverse('admin_dashboard'))  # Correct way to use reverse for redirection
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'travel/adminPage.html')

def admin_dashboard(request):
    # Check if the user is logged in and is an admin
    if not request.session.get('is_admin'):
        # Redirect to login if not authenticated as an admin
        messages.error(request, 'You need to log in as an admin first.')
        return redirect('admin_login')  # Redirect to the login page if not logged in as admin

    # Here you can render the actual admin dashboard page
    return render(request, 'travel/adminDashboard.html')

def admin_logout(request):
    # Clear the session to log out the admin
    if 'is_admin' in request.session:
        del request.session['is_admin']
        messages.success(request, 'You have logged out successfully.')
    else:
        messages.error(request, 'You are not logged in.')
    
    # Redirect to the login page after logging out
    return redirect('admin_login')  # Adjust to your actual login page URL