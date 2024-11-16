from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User 
from django.urls import reverse
from django.conf import settings



class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a specific user
class UserDetail(APIView):
    def get_object(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, user_id):
        user = self.get_object(user_id)
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        user = self.get_object(user_id)
        if user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        user = self.get_object(user_id)
        if user:
            user.delete()
            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


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

def mainPage(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'travel/mainPage.html',context)