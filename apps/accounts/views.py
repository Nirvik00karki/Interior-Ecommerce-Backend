from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer
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

            # Generate verification token
            token = email_verification_token.make_token(user)

            # Send verification email
            send_verification_email(user, token)

            return Response(
                {
                    "message": "Registration successful. Please check your email to verify your account.",
                    "user": response.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        send_verification_email(user, token)

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
            send_password_reset_email(user, token)

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
