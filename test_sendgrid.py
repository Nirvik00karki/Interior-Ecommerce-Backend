import os
import django
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import python_http_client

# Setup Django environment to get settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interior_backend.settings')
django.setup()

from django.conf import settings

print(f"Testing with From Email: {settings.DEFAULT_FROM_EMAIL}")
print(f"API Key Prefix: {settings.SENDGRID_API_KEY[:10]}...")

message = Mail(
    from_email=settings.DEFAULT_FROM_EMAIL,
    to_emails='nirvik.karki101@gmail.com',
    subject='SendGrid EU Test',
    html_content='<strong>Integration test with EU residency enabled.</strong>')

try:
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    
    response = sg.send(message)
    print(f"Status Code: {response.status_code}")
    print(f"Body: {response.body}")
    print(f"Headers: {response.headers}")
except python_http_client.exceptions.HTTPError as e:
    print(f"HTTP Error: {e.status_code}")
    print(f"Body: {e.body}")
except Exception as e:
    print(f"Unexpected Error: {str(e)}")
