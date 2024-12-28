from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Guide


class TestGuideRegistration(TestCase):

    def test_registration_valid_data(self):
        data = {
            'name': 'Arun',
            'place': 'The Taj Mahal',
            'email': 'arun1@gmail.com',
            'password': 'jksksdjd$2',
            'confirm_password': 'jksksdjd$2',
        }
        response = self.client.post(reverse('guide_registration'), data)

        
        self.assertRedirects(response, reverse('guide_login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Registration successful!", [str(message) for message in messages])

        # Ensure the guide is created and password is hashed
        guide = Guide.objects.get(email='arun1@gmail.com')
        self.assertTrue(check_password('jksksdjd$2', guide.password))

    def test_registration_password_mismatch(self):
        data = {
            'name': 'Arun',
            'place': 'The Taj Mahal',
            'email': 'arun1@gmail.com',
            'password': 'jksksdjd$2',
            'confirm_password': 'jksksdjd$1',  
        }
        response = self.client.post(reverse('guide_registration'), data)
        self.assertContains(response, "Passwords do not match!")

    def test_registration_invalid_email(self):
        data = {
            'name': 'Arun',
            'place': 'The Taj Mahal',
            'email': 'arun1gmail.com',
            'password': 'jksksdjd$2',
            'confirm_password': 'jksksdjd$2',
        }
        response = self.client.post(reverse('guide_registration'), data)
        self.assertContains(response, "Enter a valid email address.")


class TestGuideLogin(TestCase):

    def setUp(self):
        self.guide = Guide.objects.create(
            name='Arun',
            email='arun1@gmail.com',
            password=make_password('jksksdjd$2'),  # Password should be hashed
            is_super_guide=False
        )

    def test_login_valid_credentials(self):
        data = {'email': 'arun1@gmail.com', 'password': 'jksksdjd$2'}
        response = self.client.post(reverse('guide_login'), data)

       

        self.assertRedirects(response, reverse('guide_dashboard'))

        # Check session for guide_id and success message
        self.assertEqual(self.client.session.get('guide_id'), self.guide.id)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Login successful!")

    def test_login_invalid_credentials(self):
        
        data = {'email': 'arun1@gmail.com', 'password': 'wrong_password'}
        response = self.client.post(reverse('guide_login'), data)
        self.assertContains(response, "Invalid password.")

    def test_login_guide_not_exist(self):
        data = {'email': 'nonexistent@gmail.com', 'password': 'jksksdjd$2'}
        response = self.client.post(reverse('guide_login'), data)
        self.assertContains(response, "Guide profile doesn't exist.")
