import requests
import json

BASE_URL = "https://interior-ecommerce-backend.onrender.com/api"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcxMTY1NzgyLCJpYXQiOjE3NzExNjQ4ODIsImp0aSI6ImMxNzlmNjQzYjljMzQ2NTJhMzcyNDgzOTc5ODExODgxIiwidXNlcl9pZCI6IjEiLCJlbWFpbCI6Im5pcnZpa0BnbWFpbC5jb20ifQ.rufwRihaMJyc3dvG1QwGAFtC9DtZEJsegU5UZQonwnk"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def log_res(name, response):
    print(f"\n--- {name} ---")
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(f"Data: {json.dumps(data, indent=2)[:1000]}...")
        return data
    except:
        print(f"Raw: {response.text[:500]}")
        return None

def test_order_apis():
    # 1. Fetch prerequisite: Shipping Address
    print("\nStep 1: Fetching valid shipping address...")
    addr_res = requests.get(f"{BASE_URL}/accounts/shipping-addresses/", headers=headers)
    addresses = log_res("GET Shipping Addresses", addr_res)
    
    if not addresses or len(addresses) == 0:
        print("Error: No shipping addresses found for this account. Create one first.")
        return
    
    address_id = addresses[0]['id']
    print(f"Using Address ID: {address_id}")

    # 2. Fetch prerequisite: Product Variant with stock
    print("\nStep 2: Fetching valid product variant...")
    var_res = requests.get(f"{BASE_URL}/catalog/variants/", headers=headers)
    variants = log_res("GET Variants", var_res)
    
    # Look for a variant with available stock > 0
    variant = next((v for v in variants if v.get('available_stock', 0) > 0), None)
    if not variant:
        print("Error: No variants with available stock found.")
        return
    
    variant_id = variant['id']
    print(f"Using Variant ID: {variant_id} (Stock: {variant['available_stock']})")

    # 3. Create Order
    print("\nStep 3: Creating a new Order...")
    order_data = {
        "shipping_address_id": address_id,
        "items": [
            {
                "variant_id": variant_id,
                "quantity": 1
            }
        ]
    }
    create_res = requests.post(f"{BASE_URL}/order/orders/", headers=headers, json=order_data)
    order_obj = log_res("POST Create Order", create_res)

    if order_obj and 'id' in order_obj:
        order_id = order_obj['id']
        
        # 4. List Orders
        print("\nStep 4: Listing user orders...")
        log_res("GET Orders List", requests.get(f"{BASE_URL}/order/orders/", headers=headers))

        # 5. Cancel Order (Cleanup)
        print(f"\nStep 5: Cancelling test order {order_id}...")
        cancel_res = requests.post(f"{BASE_URL}/order/orders/{order_id}/cancel/", headers=headers)
        log_res("POST Cancel Order", cancel_res)
    else:
        print("Failed to create order.")

if __name__ == "__main__":
    test_order_apis()
