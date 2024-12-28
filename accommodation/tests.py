from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password
from .models import Hotel, HotelRoom
from django.urls import reverse
from django.test import TestCase, Client
from django.urls import reverse
from .models import Hotel, HotelRoom

class HotelModelTests(TestCase):
    def setUp(self):
        self.hotel_data = {
            'hotel_owner_name': 'Rangaiah',
            'owner_phone_number': '9109302390',
            'owner_email': 'ranga@gmail.com',
            'hotel_name': 'Hotel Lakshmi Grand',
            'hotel_phone_number': '9320239129',
            'hotel_email': 'lakshmi@gmail.com',
            'hotel_address': 'Hotel Lakshmi Grand, Beach Road, Ramnagar, Vizag',
            'location_on_map': 'https://www.google.com/maps?q=Hotel+Lakshmi+Grand',
            'description': 'The simply furnished rooms provide flat-screen TVs and Wi-Fi.',
            'country': 'India',
            'state': 'Andhra Pradesh',
            'city': 'Vijayawada',
            'place': 'Sunrise Park',
            'weekly_closed_on': 'Sunday',
            'week_days_opening_time': '9:00:00',
            'week_days_closing_time': '23:00:00',
            'weekends_opening_time': '8:00:00',
            'weekends_closing_time': '23:00:00',
            'password': make_password('ksjsid*12')
        }
        self.hotel = Hotel.objects.create(**self.hotel_data)

    def test_hotel_creation(self):
        self.assertTrue(isinstance(self.hotel, Hotel))
        self.assertEqual(self.hotel.hotel_name, 'Hotel Lakshmi Grand')

    def test_hotel_str_representation(self):
        expected_str = f"{self.hotel.hotel_name} - Owned by {self.hotel.hotel_owner_name}"
        self.assertEqual(str(self.hotel), expected_str)



class HotelRoomModelTests(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            hotel_owner_name='Rangaiah',
            hotel_name='Hotel Lakshmi Grand',
            hotel_email='lakshmi@gmail.com',
            password=make_password('testpass123')
        )
        self.room_data = {
            'hotel': self.hotel,
            'room_category': 'AC',
            'room_type': 'Single Bed',
            'total_rooms': 10,
            'available_rooms': 5,
            'price_per_6hrs': 2000.00
        }
        self.room = HotelRoom.objects.create(**self.room_data)

    def test_room_creation(self):
        self.assertTrue(isinstance(self.room, HotelRoom))
        self.assertEqual(self.room.room_category, 'AC')
        self.assertEqual(self.room.available_rooms, 5)



# class HotelViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.hotel_data = {
            'hotel_owner_name': 'Rangaiah',
            'owner_phone_number': '9109302390',
            'owner_email': 'ranga@gmail.com',
            'hotel_name': 'Hotel Lakshmi Grand',
            'hotel_phone_number': '9320239129',
            'hotel_email': 'lakshmi@gmail.com',
            'hotel_address': 'Hotel Lakshmi Grand, Beach Road, Ramnagar, Vizag, Visakhapatnam, Andhra Pradesh, India, PIN: 530002',
            'country': 'India',
            'state': 'Andhra Pradesh',
            'city': 'Vijayawada',
            'location_on_map': 'https://www.google.com/maps?q=Hotel+Lakshmi+Grand',
            'description': 'The simply furnished rooms provide flat-screen TVs and Wi-Fi. Room service available 24/7.',
            'password': 'ksjsid*12',
            'confirm_password': 'ksjsid*12'
        }

    def test_hotel_registration_view(self):
        response = self.client.post(reverse('hotel_registration'), self.hotel_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Hotel.objects.filter(hotel_email='lakshmi@gmail.com').exists())
