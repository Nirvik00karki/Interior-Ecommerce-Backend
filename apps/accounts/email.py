from django.conf import settings
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import logging

logger = logging.getLogger(__name__)

# Configure Brevo API
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.BREVO_API_KEY

def send_verification_email(user, token):
    verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}&uid={user.pk}"
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    sender = {"name": "Interior Design", "email": settings.DEFAULT_FROM_EMAIL}
    to = [{"email": user.email, "name": f"{user.first_name} {user.last_name}"}]
    subject = "Verify your Email"
    html_content = f"""
        <html>
        <body>
            <p>Hello {user.first_name},</p>
            <p>Click the link below to verify your email:</p>
            <a href="{verify_url}">Verify Email</a>
        </body>
        </html>
    """
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        html_content=html_content,
        sender=sender,
        subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.info(f"Verification email sent to {user.email}. Response: {api_response}")
        return api_response
    except ApiException as e:
        logger.error(f"Exception when calling TransactionalEmailsApi->send_transp_email: {e}")
        raise e

def send_password_reset_email(user, token):
    reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={user.pk}&token={token}"
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    sender = {"name": "Interior Design", "email": settings.DEFAULT_FROM_EMAIL}
    to = [{"email": user.email, "name": f"{user.first_name} {user.last_name}"}]
    subject = "Reset Your Password"
    html_content = f"""
        <html>
        <body>
            <p>Hello {user.first_name},</p>
            <p>You requested to reset your password. Click below:</p>
            <a href="{reset_url}">Reset Password</a>
            <p>If you did not request this, you can safely ignore it.</p>
        </body>
        </html>
    """
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        html_content=html_content,
        sender=sender,
        subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.info(f"Password reset email sent to {user.email}. Response: {api_response}")
        return api_response
    except ApiException as e:
        logger.error(f"Exception when calling TransactionalEmailsApi->send_transp_email: {e}")
        raise e
