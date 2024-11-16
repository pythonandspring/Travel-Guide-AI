from django.test import TestCase, Client
from .models import User
import json


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            user_id=1,
            user_role_id=2,
            user_name="John Doe",
            user_email="john.doe@example.com",
            user_dob="2000-01-01",
            user_address="123 Main Street"
        )

    def test_get_all_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_user(self):
        data = {
            "user_id": 2,
            "user_role_id": 3,
            "user_name": "Jane Smith",
            "user_email": "jane.smith@example.com",
            "user_dob": "1995-05-15",
            "user_address": "456 Elm Street"
        }
        response = self.client.post('/api/users/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_user_by_id(self):
        response = self.client.get(f'/api/users/{self.user.user_id}/')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        data = {"user_name": "John Updated"}
        response = self.client.put(
            f'/api/users/{self.user.user_id}/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        response = self.client.delete(f'/api/users/{self.user.user_id}/')
        self.assertEqual(response.status_code, 200)
