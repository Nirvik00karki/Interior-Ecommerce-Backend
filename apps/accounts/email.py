import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_sendgrid_client():
    key = settings.SENDGRID_API_KEY
    if key:
        print(f"DEBUG: Using SendGrid API Key starting with: {key[:10]}...")
    else:
        print("DEBUG: SendGrid API Key is MISSING in settings.")
    return sendgrid.SendGridAPIClient(api_key=key)

def send_verification_email(user, token):
    verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}&uid={user.pk}"

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=user.email,
        subject="Verify your Email",
        html_content=f"""
            <p>Hello {user.first_name},</p>
            <p>Click the link below to verify your email:</p>
            <a href="{verify_url}">Verify Email</a>
        """
    )

    try:
        sg = get_sendgrid_client()
        # Removed EU residency as per user feedback
        response = sg.send(message)
        logger.info(f"Verification email sent to {user.email}. Status Code: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error sending verification email to {user.email}: {e}")
        raise e

def send_password_reset_email(user, token):
    reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={user.pk}&token={token}"

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=user.email,
        subject="Reset Your Password",
        html_content=f"""
            <p>Hello {user.first_name},</p>
            <p>You requested to reset your password. Click below:</p>
            <a href="{reset_url}">Reset Password</a>
            <p>If you did not request this, you can safely ignore it.</p>
        """
    )

    try:
        sg = get_sendgrid_client()
        # Removed EU residency as per user feedback
        response = sg.send(message)
        logger.info(f"Password reset email sent to {user.email}. Status Code: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error sending password reset email to {user.email}: {e}")
        raise e
