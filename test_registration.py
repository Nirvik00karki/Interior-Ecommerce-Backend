import requests
import json
from datetime import datetime

# Generate unique email
timestamp = datetime.now().strftime("%H%M%S%f")
email = f"testuser{timestamp}@example.com"

# Registration data
data = {
    "email": email,
    "password": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
}

# Send registration request
response = requests.post(
    "http://127.0.0.1:8000/api/accounts/register/",
    headers={"Content-Type": "application/json"},
    json=data
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response:\n{json.dumps(response.json(), indent=2)}")
