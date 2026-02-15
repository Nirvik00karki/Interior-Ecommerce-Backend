import requests
import json

# Replace with your local or live base URL
BASE_URL = "https://interior-ecommerce-backend.onrender.com/api/accounts"
# Use the token provided by the user
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcxMTYxNTQxLCJpYXQiOjE3NzExNjA2NDEsImp0aSI6ImQxMzhjOTRiMjhlYjQ4MmRhOTg0ZGZiYmQ3ZGVlNjhhIiwidXNlcl9pZCI6IjEiLCJlbWFpbCI6Im5pcnZpa0BnbWFpbC5jb20ifQ.2ILbHGCSc19paA7E_Acl2wqbrYMc_402Onq_yP8XdmE"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_patch_address():
    # 1. Get existing addresses to find an ID
    print("Fetching shipping addresses...")
    response = requests.get(f"{BASE_URL}/shipping-addresses/", headers=headers)
    if response.status_code != 200:
        print(f"Error fetching addresses: {response.status_code} - {response.text}")
        return

    addresses = response.json()
    if not addresses:
        print("No shipping addresses found. Please create one first.")
        return

    # Use the first address for patching
    address_id = addresses[0]['id']
    print(f"Patching address ID: {address_id}")

    # 2. Perform PATCH request
    # Toggle is_default or update label as a test
    new_is_default = not addresses[0].get('is_default', False)
    payload = {
        "is_default": True,  # Testing the fix specifically
        "label": "office" if addresses[0].get('label') == "home" else "home"
    }

    print(f"Sending PATCH request with payload: {json.dumps(payload)}")
    patch_url = f"{BASE_URL}/shipping-addresses/{address_id}/"
    response = requests.patch(patch_url, headers=headers, json=payload)

    print(f"Response status: {response.status_code}")
    if response.status_code == 200:
        print("Success! Response data:")
        print(json.dumps(response.json(), indent=2))
        
        # Verify is_default in response
        if response.json().get('is_default') is True:
            print("Verification PASSED: is_default is now True.")
        else:
            print("Verification FAILED: is_default is still False.")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_patch_address()
