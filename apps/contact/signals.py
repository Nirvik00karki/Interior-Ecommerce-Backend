from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactSubmission


@receiver(post_save, sender=ContactSubmission)
def notify_admin_on_contact(sender, instance, created, **kwargs):
    """
    Send email notification to admin when new contact submission is received.
    Ensures timely response to customer inquiries.
    """
    if created:
        try:
            send_mail(
                subject=f"New Contact Submission: {instance.name}",
                message=f"""
New contact submission received:

Name: {instance.name}
Email: {instance.email}
Phone: {instance.phone}

Message:
{instance.message}

---
Received at: {instance.created_at}
                """.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Send to admin
                fail_silently=True,  # Don't break app if email fails
            )
        except Exception as e:
            # Log error but don't break the submission process
            print(f"Failed to send contact notification email: {e}")
