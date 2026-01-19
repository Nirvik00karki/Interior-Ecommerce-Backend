from rest_framework import status, generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (EmailTokenObtainPairSerializer, ShippingAddressSerializer
                          , ShippingZoneSerializer, AdminCreateUserSerializer)
from rest_framework.views import APIView
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from .utils import email_verification_token
from rest_framework.views import APIView
from .email import send_verification_email
from .email import send_password_reset_email
from .utils import password_reset_token
from .models import ShippingAddress, ShippingZone
from .permissions import IsAdminOrSuperUser

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    # Ensure registration endpoint does not attempt authentication and is open to anyone.
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)

            user = User.objects.get(id=response.data["id"])

            # Try to send verification email, but don't fail registration if it fails
            email_sent = True
            error_message = None
            try:
                # Generate verification token
                token = email_verification_token.make_token(user)
                # Send verification email
                send_verification_email(user, token)
            except Exception as e:
                email_sent = False
                error_message = str(e)
                # Log email failure (In a real app, use logger.error)
                print(f"Error sending verification email: {e}")

            message = "Registration successful. Please check your email to verify your account."
            if not email_sent:
                message = "Registration successful, but there was an error sending the verification email. Please contact support."

            return Response(
                {
                    "message": message,
                    "user": response.data,
                    "email_sent": email_sent,
                    "email_error": error_message if not email_sent else None
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            # Let DRF handle validation errors (e.g. "Email already exists")
            raise e
        except Exception as e:
            transaction.set_rollback(True)
            return Response(
                {"error": "Internal server error during registration.", "detail": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EmailTokenObtainPairView(TokenObtainPairView):
    # Allow login via email without prior authentication
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailTokenObtainPairSerializer


class GoogleAuthView(APIView):
    """
    Login or Signup with Google using ID Token
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        id_token_str = request.data.get("id_token")
        if not id_token_str:
            return Response({"error": "id_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify token with Google
            google_info = id_token.verify_oauth2_token(
                id_token_str,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            email = google_info.get("email")
            google_id = google_info.get("sub")
            first_name = google_info.get("given_name", "")
            last_name = google_info.get("family_name", "")
            avatar = google_info.get("picture", "")

            if not email:
                return Response({"error": "Google token has no email."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user exists
            user, created = User.objects.get_or_create(email=email)

            if created:
                # New user → set Google info
                user.google_id = google_id
                user.first_name = first_name
                user.last_name = last_name
                user.avatar = avatar
                user.set_unusable_password()
                user.save()

            # Issue JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Login successful",
                "is_new_user": created,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "avatar": user.avatar,
                },
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            })

        except ValueError:
            return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        uid = request.GET.get("uid")
        token = request.GET.get("token")

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"error": "Invalid user"}, status=400)

        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully!"})
        else:
            return Response({"error": "Invalid or expired token"}, status=400)

class ResendVerificationEmailView(APIView):
    """
    Allows a user to request a new email verification link.
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Avoid leaking whether an email exists
            return Response(
                {"message": "If your account exists, a verification email has been sent."},
                status=status.HTTP_200_OK
            )

        if user.is_active:
            return Response(
                {"message": "Your account is already verified."},
                status=status.HTTP_200_OK
            )

        # Generate new token
        token = email_verification_token.make_token(user)

        # Send verification email
        try:
            send_verification_email(user, token)
        except Exception:
            # Error is logged in email.py
            return Response(
                {"error": "There was an error sending the verification email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"message": "A new verification email has been sent."},
            status=status.HTTP_200_OK
        )
    
class PasswordResetRequestView(APIView):
    """
    Sends a password reset email if the user exists.
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)

            # Do NOT reveal if user exists
            token = password_reset_token.make_token(user)
            try:
                send_password_reset_email(user, token)
            except Exception:
                # Error is logged in email.py
                # We still return 200 to avoid leaking information
                pass

        except User.DoesNotExist:
            pass  # still pretend success

        return Response(
            {"message": "If an account exists, a password reset email has been sent."},
            status=status.HTTP_200_OK
        )
class PasswordResetValidateView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        uid = request.GET.get("uid")
        token = request.GET.get("token")

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"valid": False}, status=400)

        if password_reset_token.check_token(user, token):
            return Response({"valid": True})
        return Response({"valid": False}, status=400)

class PasswordResetCompleteView(APIView):
    """
    Final step: user provides new password.
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("password")

        if not new_password:
            return Response(
                {"error": "Password is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"error": "Invalid user"}, status=400)

        # Validate token
        if not password_reset_token.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        # Update password
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )

class ShippingAddressViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #PATCH method to update shipping address
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"error": "You are not authorized to update this shipping address."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    #DELETE method to delete shipping address
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"error": "You are not authorized to delete this shipping address."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ShippingZoneViewSet(viewsets.ModelViewSet):
    queryset = ShippingZone.objects.all()
    serializer_class = ShippingZoneSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["GET"], permission_classes=[permissions.IsAuthenticated])
    def user_shipping_cost(self, request):
        user = request.user

        # Assuming user.shipping_addresses.first().zone.cost
        address = user.shipping_addresses.first()
        if not address:
            return Response(
                {"detail": "No shipping address found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not address.zone:
            return Response(
                {"detail": "Shipping zone is missing for this address."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"shipping_cost": address.zone.cost})
    
class UserProfileView(APIView):
    """
    GET: Retrieve the authenticated user's profile information
    PATCH: Update the authenticated user's profile information
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get current user's profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Update current user's profile (partial update)"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            # If password is being updated, handle it separately
            if 'password' in request.data:
                request.user.set_password(request.data['password'])
                request.user.save()
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminUserCreateView(generics.CreateAPIView):
    serializer_class = AdminCreateUserSerializer
    permission_classes = [ IsAdminOrSuperUser ]

    def get_queryset(self):
        return User.objects.none()