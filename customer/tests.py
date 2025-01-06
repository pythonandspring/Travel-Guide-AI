from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from unittest.mock import patch


class CustomerAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.profile_url = reverse('profile')
        self.edit_profile_url = reverse('edit_profile')
        self.logout_url = reverse('logout')
        self.accommodations_url = reverse('accomodations')

        self.user = User.objects.create_user(
            username='naveen', password='kumar1234@', email='gairuboina.naveenkumar45@gmail.com')
        self.profile = Profile.objects.create(user=self.user)

    def test_login_valid_user(self):
        response = self.client.post(
            self.login_url, {'username': 'naveen', 'password': 'kumar1234@'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

    def test_login_invalid_user(self):
        response = self.client.post(
            self.login_url, {'username': 'wronguser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "there is some Issue check your credentials again.")

    def test_register_valid_user(self):
        with patch('travelling.send_mail.send_confirmation_email') as mock_send_email:
            response = self.client.post(self.register_url, {
                'username': 'chandu',
                'password1': 'mentor1@',
                'password2': 'mentor1@',
                'email': 'chandu@gmail.com'
            })
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, self.login_url)

    def test_register_valid_user(self):
        with patch('travelling.send_mail.send_confirmation_email') as mock_send_email:
            response = self.client.post(self.register_url, {
                'username': 'chandu',
                'password1': 'mentor1@',
                'password2': 'mentor1@',
                'email': 'chandu@gmail.com'
            })
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('create_profile'))

    def test_edit_profile(self):
        self.client.login(username='naveen', password='kumar1234@')
        response = self.client.post(self.edit_profile_url, {
            'email': 'updated@example.com',
            'location': 'New York',
            'birth_date': '1990-01-01',
        })
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.location, 'New York')

    def test_logout(self):
        self.client.login(username='naveen', password='kumar1234@')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_accommodations_submission(self):
        self.client.login(username='naveen', password='kumar1234@')
        response = self.client.post(self.accommodations_url, {
                                    'accomodations': 'Request for luxury suite'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.accommodations_url)
