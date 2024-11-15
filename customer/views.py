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
    return render(request, 'travel/home.html',context)

def admin_login(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    if request.user.is_authenticated:
        return redirect('admin_dashboard')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if both fields have a minimum of 4 characters
        if len(username) >= 4 and len(password) >= 4:
            if username == 'admin' and password == 'admin':
                request.session['is_admin'] = True
                return redirect(reverse('admin_dashboard'))  # Redirect to dashboard on success
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Both username and password must be at least 4 characters long.')

    return render(request, 'travel/adminPage.html',context)


def admin_dashboard(request):

    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    # Check if the user is logged in and is an admin
    if not request.session.get('is_admin'):
        # Redirect to login if not authenticated as an admin
        messages.error(request, 'You need to log in as an admin first.')
        return redirect('admin_login')  # Redirect to the login page if not logged in as admin

    # Here you can render the actual admin dashboard page
    return render(request, 'travel/adminDashboard.html',context)

def admin_logout(request):
    # Clear the session to log out the admin
    if 'is_admin' in request.session:
        del request.session['is_admin']
        messages.success(request, 'You have logged out successfully.')
    else:
        messages.error(request, 'You are not logged in.')
    
    # Redirect to the login page after logging out
    return redirect('admin_login')  # Adjust to your actual login page URL


def gallery(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/gallary.html',context)

def feedback(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/feedback.html',context)

def accomodations(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/accomodations.html',context)

def agentRegistration(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/agentRegistration.html',context)

def contact(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/contact.html',context)

def customer(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/customer.html',context)

def privacy_policy(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/privacy_policy.html',context)

def terms_conditions(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/terms_conditions.html',context)