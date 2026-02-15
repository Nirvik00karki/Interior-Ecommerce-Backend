import requests
import json

BASE_URL = "https://interior-ecommerce-backend.onrender.com/api/catalog"
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
        print(f"Data: {json.dumps(data, indent=2)[:500]}...") # Truncate long outputs
        return data
    except:
        print(f"Raw: {response.text[:500]}")
        return None

def test_catalog_apis():
    # 1. Categories
    log_res("GET Categories", requests.get(f"{BASE_URL}/categories/", headers=headers))
    
    # Try to create a category (will use cleanup if possible, or just log)
    cat_data = {"name": "Test Category Remote", "slug": "test-category-remote", "description": "Testing from script"}
    cat_res = requests.post(f"{BASE_URL}/categories/", headers=headers, json=cat_data)
    cat_obj = log_res("POST Category", cat_res)
    
    if cat_obj and 'id' in cat_obj:
        cat_id = cat_obj['id']
        log_res("GET Category Detail", requests.get(f"{BASE_URL}/categories/{cat_id}/", headers=headers))
        log_res("GET Category by Slug", requests.get(f"{BASE_URL}/categories/test-category-remote/", headers=headers))

        # 2. Products
        prod_data = {
            "name": "Test Product Remote", 
            "slug": "test-product-remote", 
            "category": cat_id,
            "description": "Testing product creation"
        }
        prod_res = requests.post(f"{BASE_URL}/products/", headers=headers, json=prod_data)
        prod_obj = log_res("POST Product", prod_res)

        if prod_obj and 'id' in prod_obj:
            prod_id = prod_obj['id']
            log_res("GET Product by Slug", requests.get(f"{BASE_URL}/products/slug/test-product-remote/", headers=headers))

            # 3. Variants
            var_data = {
                "product": prod_id,
                "sku": f"TEST-SKU-{prod_id}",
                "name": "Standard Variant",
                "price": "99.99"
            }
            var_res = requests.post(f"{BASE_URL}/variants/", headers=headers, json=var_data)
            var_obj = log_res("POST Variant", var_res)

            if var_obj and 'id' in var_obj:
                var_id = var_obj['id']
                
                # 4. Inventory
                # Inventory is usually created automatically via signals, let's check
                inv_list = requests.get(f"{BASE_URL}/inventory/", headers=headers).json()
                print("\nLooking for inventory for newly created variant...")
                inv_obj = next((i for i in inv_list if i['variant'] == var_id), None)
                if inv_obj:
                    print(f"Found inventory ID: {inv_obj['id']}")
                    log_res("PATCH Inventory", requests.patch(f"{BASE_URL}/inventory/{inv_obj['id']}/", headers=headers, json={"stock": 50}))
                else:
                    print("Inventory not found for variant.")

            # 5. Attributes
            attr_res = requests.post(f"{BASE_URL}/attributes/", headers=headers, json={"name": "Material"})
            attr_obj = log_res("POST Attribute", attr_res)
            
            if attr_obj and 'id' in attr_obj:
                attr_id = attr_obj['id']
                val_res = requests.post(f"{BASE_URL}/attribute-values/", headers=headers, json={"attribute": attr_id, "value": "Wood"})
                val_obj = log_res("POST Attribute Value", val_res)

        # Cleanup (Delete Test Data)
        print("\nCleaning up test data...")
        if 'prod_id' in locals():
            requests.delete(f"{BASE_URL}/products/{prod_id}/", headers=headers)
            print(f"Deleted product {prod_id}")
        if 'cat_id' in locals():
            requests.delete(f"{BASE_URL}/categories/{cat_id}/", headers=headers)
            print(f"Deleted category {cat_id}")
        if 'attr_id' in locals():
            requests.delete(f"{BASE_URL}/attributes/{attr_id}/", headers=headers)
            print(f"Deleted attribute {attr_id}")

    else:
        print("Failed to create category, skipping nested tests.")

if __name__ == "__main__":
    test_catalog_apis()
