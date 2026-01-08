import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interior_backend.settings')
django.setup()

from django.conf import settings

key = settings.SENDGRID_API_KEY
if not key:
    print("SENDGRID_API_KEY is empty")
else:
    print(f"SENDGRID_API_KEY length: {len(key)}")
    print(f"SENDGRID_API_KEY prefix: {key[:10]}...")
