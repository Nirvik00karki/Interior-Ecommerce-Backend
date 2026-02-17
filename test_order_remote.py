import requests
import json

BASE_URL = "https://interior-ecommerce-backend.onrender.com/api"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcxMjQwNDI5LCJpYXQiOjE3NzEyMzk1MjksImp0aSI6ImFhYzU0NjM4Njk0ODQ0NzhiOTJjZGIwMTYwOTkwYTIxIiwidXNlcl9pZCI6IjkiLCJlbWFpbCI6ImdhcmFnZTg5MDhAbmV3dHJlYS5jb20ifQ.i3azJpZl9aENjwIVH6N8-DhFD-gBx_kr-14L_H7AUWk"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOG_FILE = "remote_order_test.log"

def log_to_file(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)

def log_res(name, response):
    log_to_file(f"\n--- {name} ---")
    log_to_file(f"URL: {response.url}")
    log_to_file(f"Status: {response.status_code}")
    if response.status_code >= 400:
        log_to_file(f"ERROR DETECTED")
    try:
        data = response.json()
        log_to_file(f"Data: {json.dumps(data, indent=2)[:2000]}")
        return data
    except Exception as e:
        log_to_file(f"JSON Parse Error: {e}")
        log_to_file(f"Raw Response (first 2000 chars): {response.text[:2000]}")
        return None

def test_order_apis():
    # Clear log file
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("Starting Remote Order API Test\n")

    # 1. Fetch prerequisite: Shipping Address and Zones
    log_to_file("\nStep 1: Checking Addresses and Zones consistency...")
    
    zones_res = requests.get(f"{BASE_URL}/accounts/shipping-zones/", headers=headers)
    zones = log_res("GET Shipping Zones", zones_res)
    zone_ids = [z['id'] for z in zones] if zones else []
    log_to_file(f"Available Zone IDs on server: {zone_ids}")

    addr_res = requests.get(f"{BASE_URL}/accounts/shipping-addresses/", headers=headers)
    addresses = log_res("GET Shipping Addresses", addr_res)
    
    if not addresses or len(addresses) == 0:
        log_to_file("Error: No shipping addresses found.")
        return
    
    for i, addr in enumerate(addresses):
        z_id = addr.get('zone')
        is_valid = z_id in zone_ids
        log_to_file(f"Address {i}: ID={addr['id']}, ZoneID={z_id}, Is Valid Zone={is_valid}")

    address = addresses[0]
    address_id = address['id']
    log_to_file(f"Using Address ID: {address_id} for order creation.")

    # 2. Fetch prerequisite: Product Variant with stock
    log_to_file("\nStep 2: Fetching valid product variant...")
    var_res = requests.get(f"{BASE_URL}/catalog/variants/", headers=headers)
    variants = log_res("GET Variants", var_res)
    
    if not variants or len(variants) == 0:
        log_to_file("Error: No variants found.")
        return

    # Look for a variant with available stock > 0
    variant = next((v for v in variants if v.get('available_stock', 0) > 0), None)
    if not variant:
        log_to_file("Error: No variants with available stock found.")
        return
    
    variant_id = variant['id']
    log_to_file(f"Using Variant ID: {variant_id} (Stock: {variant['available_stock']})")

    # 3. Create Order
    log_to_file(f"\nStep 3: Creating a new Order using Address: {json.dumps(address, indent=2)}")
    log_to_file("\nCreating a new Order...")
    order_data = {
        "shipping_address_id": address_id,
        "items": [
            {
                "variant_id": variant_id,
                "quantity": 1
            }
        ]
    }
    create_res = requests.post(f"{BASE_URL}/orders/", headers=headers, json=order_data)
    order_obj = log_res("POST Create Order", create_res)

    if order_obj and 'id' in order_obj:
        order_id = order_obj['id']
        
        # 4. List Orders
        log_to_file("\nStep 4: Listing user orders...")
        log_res("GET Orders List", requests.get(f"{BASE_URL}/orders/", headers=headers))

        # 5. Cancel Order (Cleanup)
        log_to_file(f"\nStep 5: Cancelling test order {order_id}...")
        cancel_res = requests.post(f"{BASE_URL}/orders/{order_id}/cancel/", headers=headers)
        log_res("POST Cancel Order", cancel_res)
    else:
        log_to_file("Failed to create order.")

if __name__ == "__main__":
    test_order_apis()
