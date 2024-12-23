from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



def send_confirmation_email(to_email, user_type, username, additional_info):
    subject = ''
    message = ''

    if user_type == 'hotel_owner':
        hotel_name = additional_info.get('hotel_name', 'Your Hotel')
        hotel_email = additional_info.get('hotel_email', 'yourhotel@example.com')
        subject = f'Welcome, {hotel_name}! Your journey with Travel Guide begins'
        message = f'''
        Dear {username},

        Thank you for registering with us as a Hotel Owner! We are excited to connect you with experienced guides and
        customers looking for unique travel experiences. Here’s what you can expect:

        1. Your profile will be visible to potential customers and guides.
        2. You can collaborate with guides and manage bookings directly on our platform.
        3. Customize your profile with details about your hotel "{hotel_name}" to attract more guests.

        Your registered hotel email: {hotel_email}

        We look forward to helping you grow your business!

        Best regards,
        The Travel Guide Team
        '''

    elif user_type == 'guide':
        place_name = additional_info.get('place_name', 'your area')
        guide_name = additional_info.get('guide_name', 'Guide')
        guide_email = additional_info.get(
            'guide_email', 'yourguide@example.com')
        subject = f'Welcome, {guide_name} from {
            place_name}! Your journey with Travel Guide begins'
        message = f'''
        Dear {guide_name},

        Thank you for joining our Travel Guide platform as a Guide for { place_name }! We are thrilled to have you on board. Here's how you can get started:

        1. Your profile will be available to hotels who need guides for their customers.
        2. You can offer your services directly to customers and provide tailored experiences.
        3. Complete your profile to showcase your specialties and services.

        Your registered guide email: {guide_email}

        If you need help or have any questions, feel free to reach out. We're here to support you!

        Best regards,
        The Travel Guide Team
        '''

    elif user_type == 'customer':
        subject = f'Welcome, {username}! Start exploring with Travel Guide'
        customer_email = additional_info.get('email', 'yourcustomer@example.com')
        message = f'''
        Dear {username},

        Thank you for registering as a Customer! We are excited to connect you with a variety of hotels and expert guides
        to help you plan your perfect trip. Here’s what you can do next:

        1. Browse through a variety of hotels and find the perfect one for your travel needs.
        2. Connect with expert guides who can offer personalized travel experiences.
        3. Complete your profile to get personalized recommendations.

        Your registered email: {customer_email}

        We hope you have a fantastic experience on our platform. If you need assistance, we're just an email away!

        Best regards,
        The Travel Guide Team
        '''

    from_email = settings.EMAIL_HOST_USER

    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=False,
    )

from travelling.filter_data.get_data import get_cities
print(get_cities())