from django.test import TestCase, Client
from django.urls import reverse
from .models import Hotel
from django.contrib.auth.hashers import make_password


class HotelAuthenticationTests(TestCase):
    def test_hotel_registration(self):
        response = self.client.post(reverse('hotel_registration'), {
            'hotel_owner_name': 'Srinivas',
            'owner_phone_number': '9209348123',
            'owner_email': 'srinivas@gmail.com',
            'hotel_name': 'Green Valley Hotel',
            'hotel_phone_number': '8102349123',
            'hotel_email': 'greenvalley@gmail.com',
            'hotel_address': 'Test Address',
            'description': 'Test Description',
            'country': 'India',
            'state': 'Andhra Pradesh',
            'city': 'Vijayawada',
            'place': 'Test Place',
            'password': 'pass@1234',
            'confirm_password': 'pass@1234',
            'week_days_opening_time': '09:00:00',
            'week_days_closing_time': '22:00:00',
            'weekends_opening_time': '09:00:00',
            'weekends_closing_time': '22:00:00'
        })
        self.assertEqual(response.status_code, 200)


class HotelRoomManagementTests(TestCase):
    def test_add_room(self):
        response = self.client.post(reverse('add_room_type'), {
            'room_category': 'DELUXE',
            'room_type': 'AC',
            'total_rooms': 10,
            'available_rooms': 8,
            'price_per_6hrs': 2000,

        })
        self.assertEqual(response.status_code, 302)


class HotelImageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.hotel = Hotel.objects.create(
            hotel_owner_name="Rangaiah",
            hotel_email="lakshmi@gmail.com",
            password=make_password("ksjsid*12")
        )
        self.client.post(reverse('hotel_login'), {
            'email': 'lakshmi@gmail.com',
            'password': 'ksjsid*12'
        })
        self.client.session['hotel_owner_id'] = self.hotel.id
        self.client.session.save()


class HotelDetailsUpdateTests(TestCase):
    def test_update_hotel_details(self):
        response = self.client.post(reverse('update_dashboard'), {
            'hotel_name': 'Updated Hotel Name',
            'hotel_phone_number': '9876543210',
            'hotel_email': 'lakshmi@gmail.com',
            'hotel_address': 'Updated Address',
            'description': 'Updated Description',
            'week_days_opening_time': '08:00:00',
            'week_days_closing_time': '23:00:00',
            'weekends_opening_time': '09:00:00',
            'weekends_closing_time': '22:00:00'
        })
        self.assertEqual(response.status_code, 302)


class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.hotel = Hotel.objects.create(
            hotel_owner_name="Rangaiah",
            hotel_email="lakshmi@gmail.com",
            password=make_password("ksjsid*12")
        )

    def test_password_reset_request(self):
        response = self.client.post(reverse('hotel_request_password_reset'), {
            'email': 'lakshmi@gmail.com'
        })
        self.assertEqual(response.status_code, 200)
