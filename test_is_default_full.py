import requests
import json
import uuid

# Base URL for accounts API
BASE_URL = "https://interior-ecommerce-backend.onrender.com/api/accounts"
# Using the token provided by the user
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcxMTYxNTQxLCJpYXQiOjE3NzExNjA2NDEsImp0aSI6ImQxMzhjOTRiMjhlYjQ4MmRhOTg0ZGZiYmQ3ZGVlNjhhIiwidXNlcl9pZCI6IjEiLCJlbWFpbCI6Im5pcnZpa0BnbWFpbC5jb20ifQ.2ILbHGCSc19paA7E_Acl2wqbrYMc_402Onq_yP8XdmE"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def clean_up_test_addresses():
    print("Fetching shipping addresses for cleanup...")
    response = requests.get(f"{BASE_URL}/shipping-addresses/", headers=headers)
    if response.status_code == 200:
        addresses = response.json()
        for addr in addresses:
            if "Test Address" in addr.get('full_name', ''):
                requests.delete(f"{BASE_URL}/shipping-addresses/{addr['id']}/", headers=headers)
                print(f"Deleted test address {addr['id']}")

def test_is_default_flow():
    # 0. Clean up any previous test addresses
    # clean_up_test_addresses()

    # 1. Get a zone first
    print("\nStep 1: Fetching shipping zones...")
    response = requests.get(f"{BASE_URL}/shipping-zones/", headers=headers)
    if response.status_code != 200:
        print(f"Error fetching zones: {response.status_code}")
        return
    zones = response.json()
    if not zones:
        print("No zones found.")
        return
    zone_id = zones[0]['id']

    # 2. Create Address A with is_default=True
    data_a = {
        "full_name": "Test Address A",
        "phone": "1234567890",
        "address_line1": "Address A Line 1",
        "zone": zone_id,
        "state": "Bagmati",
        "country": "Nepal",
        "is_default": True
    }
    print("\nStep 2: Creating Address A as default...")
    response = requests.post(f"{BASE_URL}/shipping-addresses/", headers=headers, json=data_a)
    if response.status_code != 201:
        print(f"Error creating Address A: {response.status_code} - {response.text}")
        return
    addr_a = response.json()
    print(f"Address A created with id {addr_a['id']}, is_default={addr_a['is_default']}")

    # 3. Create Address B with is_default=True
    # This should automatically make Address A non-default
    data_b = {
        "full_name": "Test Address B",
        "phone": "0987654321",
        "address_line1": "Address B Line 1",
        "zone": zone_id,
        "state": "Bagmati",
        "country": "Nepal",
        "is_default": True
    }
    print("\nStep 3: Creating Address B as default (should unset A)...")
    response = requests.post(f"{BASE_URL}/shipping-addresses/", headers=headers, json=data_b)
    if response.status_code != 201:
        print(f"Error creating Address B: {response.status_code} - {response.text}")
        return
    addr_b = response.json()
    print(f"Address B created with id {addr_b['id']}, is_default={addr_b['is_default']}")

    # 4. Create Address C with is_default=False
    data_c = {
        "full_name": "Test Address C",
        "phone": "1122334455",
        "address_line1": "Address C Line 1",
        "zone": zone_id,
        "state": "Bagmati",
        "country": "Nepal",
        "is_default": False
    }
    print("\nStep 4: Creating Address C as non-default...")
    response = requests.post(f"{BASE_URL}/shipping-addresses/", headers=headers, json=data_c)
    if response.status_code != 201:
        print(f"Error creating Address C: {response.status_code} - {response.text}")
        return
    addr_c = response.json()
    print(f"Address C created with id {addr_c['id']}, is_default={addr_c['is_default']}")

    # 5. Verify states
    print("\nStep 5: Verifying addresses states...")
    addresses = requests.get(f"{BASE_URL}/shipping-addresses/", headers=headers).json()
    for addr in addresses:
        if addr['id'] == addr_a['id']:
            print(f"Address A (id={addr['id']}) is_default: {addr['is_default']} (Expected: False)")
        elif addr['id'] == addr_b['id']:
            print(f"Address B (id={addr['id']}) is_default: {addr['is_default']} (Expected: True)")
        elif addr['id'] == addr_c['id']:
            print(f"Address C (id={addr['id']}) is_default: {addr['is_default']} (Expected: False)")

    # 6. Patch Address C to be default
    print(f"\nStep 6: Patching Address C (id={addr_c['id']}) to be default...")
    response = requests.patch(f"{BASE_URL}/shipping-addresses/{addr_c['id']}/", headers=headers, json={"is_default": True})
    if response.status_code == 200:
        print(f"Address C patched successfully.")
        print(f"Response data: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error patching Address C: {response.status_code} - {response.text}")

    # 7. Final Verification
    print("\nStep 7: Final Verification...")
    addresses = requests.get(f"{BASE_URL}/shipping-addresses/", headers=headers).json()
    for addr in addresses:
        if addr['id'] == addr_a['id']:
            print(f"Address A (id={addr['id']}) is_default: {addr['is_default']} (Expected: False)")
        elif addr['id'] == addr_b['id']:
            print(f"Address B (id={addr['id']}) is_default: {addr['is_default']} (Expected: False)")
        elif addr['id'] == addr_c['id']:
            print(f"Address C (id={addr['id']}) is_default: {addr['is_default']} (Expected: True)")

if __name__ == "__main__":
    test_is_default_flow()
