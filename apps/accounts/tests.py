from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

from unittest.mock import patch

class AccountTests(APITestCase):
    @patch('apps.accounts.views.send_verification_email')
    def test_registration_success(self, mock_send_email):
        # 1. Test Registration
        register_url = reverse('register')
        data = {
            "email": "testuser_new@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Registration successful. Please check your email to verify your account.")
        
        # Verify user is NOT active yet
        user = User.objects.get(email="testuser_new@example.com")
        self.assertFalse(user.is_active)
        
        # Verify email was "sent"
        mock_send_email.assert_called_once()

    @patch('apps.accounts.views.send_password_reset_email')
    def test_password_reset_request(self, mock_send_reset_email):
        # 0. Create user first
        User.objects.create_user(email="reset_new@example.com", password="oldpassword123")
        
        # 1. Test Password Reset Request
        reset_url = reverse('password_reset_request')
        data = {"email": "reset_new@example.com"}
        response = self.client.post(reset_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "If an account exists, a password reset email has been sent.")
        
        # Verify reset email was "sent"
        mock_send_reset_email.assert_called_once()
