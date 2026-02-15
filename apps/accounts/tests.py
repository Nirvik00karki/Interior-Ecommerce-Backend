from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

from unittest.mock import patch

class AccountTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()

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
        user = self.User.objects.get(email="testuser_new@example.com")
        self.assertFalse(user.is_active)
        
        # Verify email was "sent"
        mock_send_email.assert_called_once()

    @patch('apps.accounts.views.send_password_reset_email')
    def test_password_reset_request(self, mock_send_reset_email):
        # 0. Create user first
        self.User.objects.create_user(email="reset_new@example.com", password="oldpassword123")
        
        # 1. Test Password Reset Request
        reset_url = reverse('password_reset_request')
        data = {"email": "reset_new@example.com"}
        response = self.client.post(reset_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "If an account exists, a password reset email has been sent.")
        
        # Verify reset email was "sent"
        mock_send_reset_email.assert_called_once()

class ShippingAddressTests(APITestCase):
    def setUp(self):
        from apps.accounts.models import ShippingAddress, ShippingZone
        self.User = get_user_model()
        self.ShippingAddress = ShippingAddress
        self.ShippingZone = ShippingZone
        self.user = self.User.objects.create_user(email="test_shipping@example.com", password="password")
        self.client.force_authenticate(user=self.user)
        self.zone = self.ShippingZone.objects.create(name="inside_valley", cost=100)
    
    def test_create_shipping_address_is_default(self):
        print("\nRunning test_create_shipping_address_is_default...")
        url = reverse("shipping_addresses")
        data = {
            "full_name": "Test User",
            "phone": "1234567890",
            "address_line1": "Test Address",
            "zone": self.zone.id,
            "state": "Bagmati",
            "country": "Nepal",
            "is_default": True
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check database
        address = self.ShippingAddress.objects.get(id=response.data['id'])
        self.assertTrue(response.data['is_default'], "is_default should be True in response")
        self.assertTrue(address.is_default, "is_default should be True in database")

    def test_update_shipping_address_is_default(self):
        print("\nRunning test_update_shipping_address_is_default...")
        # Create a default address first
        address1 = self.ShippingAddress.objects.create(
            user=self.user,
            full_name="Address 1",
            phone="1234567890",
            address_line1="Line 1",
            zone=self.zone,
            state="State",
            country="Country",
            is_default=True
        )
        
        # Create another non-default address
        address2 = self.ShippingAddress.objects.create(
            user=self.user,
            full_name="Address 2",
            phone="0987654321",
            address_line1="Line 2",
            zone=self.zone,
            state="State",
            country="Country",
            is_default=False
        )
        
        url = reverse("shipping_address_detail", kwargs={"pk": address2.id})
        data = {"is_default": True}
        
        response = self.client.patch(url, data)
        print(f"Response status: {response.status_code}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        address1.refresh_from_db()
        address2.refresh_from_db()
            
        self.assertFalse(address1.is_default, "Address 1 should no longer be default")
        self.assertTrue(address2.is_default, "Address 2 should be default")
