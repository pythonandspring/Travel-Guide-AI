from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Guide


class TestGuideRegistration(TestCase):

    def test_registration_valid_data(self):
        # Test case for valid guide registration
        data = {
            'name': 'Arun',
            'place': 'The Taj Mahal',
            'email': 'arun1@gmail.com',
            'password': 'jksksdjd$2',
            'confirm_password': 'jksksdjd$2',
        }
        response = self.client.post(reverse('guide_registration'), data)

        # Check if it redirects to the login page
        # self.assertEqual(response.status_code, 302)  # Ensure it redirects
        self.assertRedirects(response, reverse('guide_login'))

        # Check the success message
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Registration successful!", [str(message) for message in messages])

        # Ensure the guide is created and password is hashed
        guide = Guide.objects.get(email='arun1@gmail.com')
        self.assertTrue(check_password('jksksdjd$2', guide.password))

    def test_registration_password_mismatch(self):
        # Test case where passwords do not match
        data = {
            'name': 'Arun',
            'place': 'The Taj Mahal',
            'email': 'arun1@gmail.com',
            'password': 'jksksdjd$2',
            'confirm_password': 'wrong_password',
        }
        response = self.client.post(reverse('guide_registration'), data)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Passwords do not match!", [str(message) for message in messages])

    def test_registration_invalid_email(self):
        # Test case with invalid email
        data = {
            'name': 'Arun',
            'place': 'The Taj Mahal',
            'email': 'arun1gmail.com',
            'password': 'jksksdjd$2',
            'confirm_password': 'jksksdjd$2',
        }
        response = self.client.post(reverse('guide_registration'), data)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')


class TestGuideLogin(TestCase):

    def setUp(self):
        self.guide = Guide.objects.create(
            name='Arun',
            email='arun1@gmail.com',
            password=make_password('jksksdjd$2'),  # Password should be hashed
            is_super_guide=False
        )

    def test_login_valid_credentials(self):
        # Test valid login credentials
        data = {'email': 'arun1@gmail.com', 'password': 'jksksdjd$2'}
        response = self.client.post(reverse('guide_login'), data)
        self.assertRedirects(response, reverse('guide_dashboard'))

        # Check session for guide_id and success message
        self.assertEqual(self.client.session.get('guide_id'), self.guide.id)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Login successful!")

    def test_login_invalid_credentials(self):
        # Test invalid login credentials
        data = {'email': 'arun1@gmail.com', 'password': 'wrong_password'}
        response = self.client.post(reverse('guide_login'), data)
        self.assertContains(response, "Invalid password.")

    def test_login_guide_not_exist(self):
        # Test case where guide doesn't exist in the database
        data = {'email': 'nonexistent@gmail.com', 'password': 'jksksdjd$2'}
        response = self.client.post(reverse('guide_login'), data)
        self.assertContains(response, "Guide profile doesn't exist.")