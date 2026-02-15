import requests
import json

BASE_URL = "https://interior-ecommerce-backend.onrender.com/api/accounts"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcxMTYxNTQxLCJpYXQiOjE3NzExNjA2NDEsImp0aSI6ImQxMzhjOTRiMjhlYjQ4MmRhOTg0ZGZiYmQ3ZGVlNjhhIiwidXNlcl9pZCI6IjEiLCJlbWFpbCI6Im5pcnZpa0BnbWFpbC5jb20ifQ.2ILbHGCSc19paA7E_Acl2wqbrYMc_402Onq_yP8XdmE"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def reproduce():
    # 1. Get a valid zone
    print("Fetching shipping zones...")
    try:
        response = requests.get(f"{BASE_URL}/shipping-zones/", headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch zones: {response.status_code} - {response.text}")
            return
        
        zones = response.json()
        if not zones:
            print("No shipping zones found.")
            return
            
        zone_id = zones[0]['id']
        print(f"Using zone ID: {zone_id}")
    except Exception as e:
        print(f"Error fetching zones: {e}")
        return

    # 2. Create shipping address with is_default=True
    data = {
        "full_name": "Test User Remote",
        "phone": "9876543210",
        "address_line1": "Test Address Remote",
        "zone": zone_id,
        "state": "Bagmati",
        "country": "Nepal",
        "is_default": True,
        "label": "home"
    }
    
    print("\nCreating shipping address with is_default=True...")
    try:
        response = requests.post(f"{BASE_URL}/shipping-addresses/", headers=headers, json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            resp_data = response.json()
            if resp_data.get('is_default') is True:
                print("\nSUCCESS: is_default is True in response.")
            else:
                print("\nFAILURE: is_default is False in response. Issue reproduced!")
        else:
             print("\nFailed to create address.")

    except Exception as e:
        print(f"Error creating address: {e}")

if __name__ == "__main__":
    reproduce()
