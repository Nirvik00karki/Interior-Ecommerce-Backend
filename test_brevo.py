import os
import django
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interior_backend.settings')
django.setup()

from django.conf import settings

def test_brevo_email():
    print(f"DEBUG: Using Brevo API Key starting with: {settings.BREVO_API_KEY[:10]}...")
    print(f"DEBUG: Using From Email: {settings.DEFAULT_FROM_EMAIL}")

    # Configure Brevo API
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    sender = {"name": "Test Runner", "email": settings.DEFAULT_FROM_EMAIL}
    to = [{"email": "nirvik.karki00@gmail.com", "name": "Nirvik Karki"}]
    subject = "Brevo Integration Test"
    html_content = "<html><body><h1>It Works!</h1><p>Brevo is successfully integrated with your Django backend.</p></body></html>"
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        html_content=html_content,
        sender=sender,
        subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent successfully! Response: {api_response}")
    except ApiException as e:
        print(f"Exception when calling TransactionalEmailsApi->send_transp_email: {e}")

if __name__ == "__main__":
    test_brevo_email()
