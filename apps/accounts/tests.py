from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountTests(APITestCase):
    def test_registration_and_login(self):
        # 1. Test Registration
        register_url = reverse('register')  # Assuming the name is 'register'
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Registration successful. You can now log in.")
        
        # Verify user is active
        user = User.objects.get(email="testuser@example.com")
        self.assertTrue(user.is_active)

        # 2. Test Login
        login_url = reverse('login')
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Standard JWT returns tokens at the root
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
