import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_verification_email(user, token):
    verify_url = f"https://your-frontend.com/verify-email?token={token}&uid={user.pk}"

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

    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    sg.send(message)

def send_password_reset_email(user, token):
    reset_url = f"https://your-frontend.com/reset-password?uid={user.pk}&token={token}"

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

    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    sg.send(message)
