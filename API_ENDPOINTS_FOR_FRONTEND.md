# API Endpoints Documentation for Frontend Integration

**Base URL**: `http://localhost:8000/` (local) | `https://interior-ecommerce-backend.onrender.com/` (production)

---

## Authentication Endpoints

All endpoints use the base path: `/api/accounts/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/accounts/`
- Production: `https://interior-ecommerce-backend.onrender.com/api/accounts/`

### 1. **User Registration**
- **Endpoint**: `POST /api/accounts/register/`
- **Full URL**: `http://localhost:8000/api/accounts/register/`
- **Description**: Register a new user
- **Request Body**:
  ```
  {
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
  
  Optional / nullable fields (not required):
  - `first_name`: optional (blank=True)
  - `last_name`: optional (blank=True)
  - `google_id`: optional on model (null=True) — note: API sets this via Google auth (read-only for registration)
  - `avatar`: optional on model (null=True) — read-only
- **Response**: User created, returns token
- **Status**: 201 Created

---

### 2. **User Login**
- **Endpoint**: `POST /api/accounts/login/`
- **Full URL**: `http://localhost:8000/api/accounts/login/`
- **Description**: Login with email and password
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**: Returns access & refresh tokens
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
  ```
- **Status**: 200 OK

---

### 3. **Refresh Access Token**
- **Endpoint**: `POST /api/accounts/token/refresh/`
- **Full URL**: `http://localhost:8000/api/accounts/token/refresh/`
- **Description**: Get a new access token using refresh token
- **Request Body**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
  ```
- **Response**: New access token
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
  ```
- **Status**: 200 OK

---

### 4. **Google Authentication**
- **Endpoint**: `POST /api/accounts/google/`
- **Full URL**: `http://localhost:8000/api/accounts/google/`
- **Description**: Authenticate using Google OAuth token
- **Request Body**:
  ```json
  {
    "id_token": "<google_id_token>"
  }
  ```
- **Response**: Returns access & refresh tokens or creates new user
- **Status**: 200 OK / 201 Created

---

### 5. **Verify Email**
- **Endpoint**: `GET /api/accounts/verify-email/?uid={uid}&token={token}`
- **Full URL**: `http://localhost:8000/api/accounts/verify-email/?uid=123&token=abcdef`
- **Description**: Verify user email via query parameters received in verification link (`uid` and `token`).
- **Request Body**: none (use query params)
- **Response**: Email verified confirmation
- **Status**: 200 OK

---

### 6. **Resend Verification Email**
- **Endpoint**: `POST /api/accounts/resend-verification/`
- **Full URL**: `http://localhost:8000/api/accounts/resend-verification/`
- **Description**: Resend verification email
- **Request Body**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response**: Verification email sent
- **Status**: 200 OK

---

### 7. **Password Reset - Request**
- **Endpoint**: `POST /api/accounts/password-reset/request/`
- **Full URL**: `http://localhost:8000/api/accounts/password-reset/request/`
- **Description**: Request password reset
- **Request Body**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response**: Reset email sent
- **Status**: 200 OK

---

### 8. **Password Reset - Validate Token**
- **Endpoint**: `GET /api/accounts/password-reset/validate/?uid={uid}&token={token}`
- **Full URL**: `http://localhost:8000/api/accounts/password-reset/validate/?uid=123&token=abcdef`
- **Description**: Validate password reset token via query parameters (`uid` and `token`).
- **Request Body**: none (use query params)
- **Response**: Token validity confirmation (JSON `{ "valid": true }`)
- **Status**: 200 OK

---

### 9. **Password Reset - Complete**
- **Endpoint**: `POST /api/accounts/password-reset/complete/`
- **Full URL**: `http://localhost:8000/api/accounts/password-reset/complete/`
- **Description**: Complete password reset with new password
- **Request Body**:
  ```json
  {
    "uid": "<user_id_from_email_link>",
    "token": "reset_token_from_email",
    "password": "newsecurepassword123"
  }
  ```
- **Response**: Password updated
- **Status**: 200 OK

---

## Blog Endpoints

All endpoints use the base path: `/api/blog/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/blog/`
- Production: `https://interior-ecommerce-backend.onrender.com/api/blog/`

### 1. **Blog Categories - List / Create**
- **Endpoint**: `GET /api/blog/categories/` | `POST /api/blog/categories/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/blog/categories/`
  - Create: `http://localhost:8000/api/blog/categories/`
- **Description**: List all blog categories or create new
- **Query Parameters (GET)**:
  - `search`: Search by name
  - `page`: Pagination
- **Request Body (POST)**:
  ```json
  {
    "name": "Technology",
    "slug": "technology"
  }
  ```
- **Response**: List of categories or created category
- **Status**: 200 OK / 201 Created

---

### 2. **Blog Categories - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/blog/categories/{id}/` | `PUT /api/blog/categories/{id}/` | `DELETE /api/blog/categories/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/blog/categories/1/`
  - Update: `http://localhost:8000/api/blog/categories/1/`
  - Delete: `http://localhost:8000/api/blog/categories/1/`
- **Description**: Get, update, or delete a specific blog category

---

### 3. **Blog Posts - List / Create**
- **Endpoint**: `GET /api/blog/posts/` | `POST /api/blog/posts/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/blog/posts/`
  - Create: `http://localhost:8000/api/blog/posts/`
- **Description**: List all blog posts or create new
- **Query Parameters (GET)**:
  - `search`: Search by title or content
  - `category`: Filter by category ID
  - `page`: Pagination
- **Request Body (POST)**:
  ```json
  {
    "title": "Interior Design Trends 2025",
    "slug": "interior-design-trends-2025",
    "content": "Detailed blog content here...",
    "cover_image": "",
    "blog_category": 1,
    "excerpt": "Short excerpt...",
    "tags": ["design", "trends"],
    "author": "Jane Author",
    "is_published": true
  }
  ```
  
  Optional / nullable fields (not required):
  - `excerpt`: optional (blank=True)
  - `tags`: optional (blank=True)
  - `blog_category`: nullable FK (null=True) — optional
- **Response**: List of posts or created post
- **Status**: 200 OK / 201 Created

---

### 4. **Blog Posts - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/blog/posts/{id}/` | `PUT /api/blog/posts/{id}/` | `DELETE /api/blog/posts/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/blog/posts/1/`
  - Update: `http://localhost:8000/api/blog/posts/1/`
  - Delete: `http://localhost:8000/api/blog/posts/1/`
- **Description**: Get, update, or delete a specific blog post

---

## CMS Endpoints

All endpoints use the base path: `/api/cms/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/cms/`
- Production: `https://interior-ecommerce-backend.onrender.com/api/cms/`

### 1. **Pages - List / Create**
- **Endpoint**: `GET /api/cms/pages/` | `POST /api/cms/pages/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/cms/pages/`
  - Create: `http://localhost:8000/api/cms/pages/`
- **Description**: List all CMS pages or create new
- **Request Body (POST)**:
  ```json
  {
    "title": "About Us",
    "slug": "about-us",
    "content": "Page content here..."
  }
  ```
- **Response**: List of pages or created page
- **Status**: 200 OK / 201 Created

---

### 2. **Hero Slides - List / Create**
- **Endpoint**: `GET /api/cms/hero-slides/` | `POST /api/cms/hero-slides/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/cms/hero-slides/`
  - Create: `http://localhost:8000/api/cms/hero-slides/`
- **Description**: Manage hero/banner slides
- **Request Body (POST)**:
  ```json
  {
    "title": "Welcome to Our Interior Design",
    "sub_title": "Transform Your Space",
    "order": 1,
    "is_published": true
  }
  ```
  
  Optional / nullable fields (not required):
  - `sub_title`: optional (blank=True)
  - `image`: optional (blank=True, null=True)
  - `video`: optional (blank=True, null=True)
  - `link`: optional (blank=True, null=True)
- **Response**: List of slides or created slide
- **Status**: 200 OK / 201 Created

---

### 3. **Methodologies - List / Create**
- **Endpoint**: `GET /api/cms/methodologies/` | `POST /api/cms/methodologies/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/cms/methodologies/`
  - Create: `http://localhost:8000/api/cms/methodologies/`
- **Description**: List design methodologies
- **Request Body (POST)**:
  ```json
  {
    "title": "Client Consultation",
    "description": "Detailed methodology description",
    "order": 1
  }
  ```
  
  Optional / nullable fields (not required):
  - `image_or_icon`: optional (blank=True, null=True)
- **Response**: List of methodologies or created methodology
- **Status**: 200 OK / 201 Created

---

### 4. **FAQ - List / Create**
- **Endpoint**: `GET /api/cms/faq/` | `POST /api/cms/faq/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/cms/faq/`
  - Create: `http://localhost:8000/api/cms/faq/`
- **Description**: Manage FAQs
- **Request Body (POST)**:
  ```json
  {
    "question": "What is your design process?",
    "answer": "We follow a 5-step process...",
    "order": 1
  }
  ```
- **Response**: List of FAQs or created FAQ
- **Status**: 200 OK / 201 Created

---

## Company Endpoints

All endpoints use the base path: `/api/company/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/company/`
- Production: `https://interior-ecommerce-backend.onrender.com/api/company/`

### 1. **Offices - List / Create**
- **Endpoint**: `GET /api/company/offices/` | `POST /api/company/offices/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/company/offices/`
  - Create: `http://localhost:8000/api/company/offices/`
- **Description**: List company offices
- **Request Body (POST)**:
  ```json
  {
    "name": "New York Office",
    "address": "123 Main St, NY",
    "phone": "+1-555-1234",
    "email": "ny@company.com",
    "google_maps_url": "https://maps.google.com/?q=40.7128,-74.0060"
  }
  ```
  
  Optional / nullable fields (not required):
  - `phone`: optional (blank=True, null=True)
  - `email`: optional (blank=True, null=True)
  - `google_maps_url`: optional (blank=True, null=True)
- **Response**: List of offices or created office
- **Status**: 200 OK / 201 Created

---

### 2. **Team Members - List / Create**
- **Endpoint**: `GET /api/company/team-members/` | `POST /api/company/team-members/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/company/team-members/`
  - Create: `http://localhost:8000/api/company/team-members/`
- **Description**: List team members
- **Request Body (POST)**:
  ```json
  {
    "name": "John Smith",
    "designation": "Senior Designer",
    "bio": "Experienced interior designer...",
    "social_links": [{"platform": "linkedin", "url": "https://..."}],
    "office": 1,
    "order": 0
  }
  ```
  
  Optional / nullable fields (not required):
  - `profile_picture`: optional (blank=True, null=True)
  - `bio`: optional (blank=True)
  - `social_links`: optional (JSONField, default=list)
  - `office`: optional FK (null=True)
  - `order`: optional (defaults to 0)
- **Response**: List of team members or created member
- **Status**: 200 OK / 201 Created

---

### 3. **Awards - List / Create**
- **Endpoint**: `GET /api/company/awards/` | `POST /api/company/awards/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/company/awards/`
  - Create: `http://localhost:8000/api/company/awards/`
- **Description**: List company awards
- **Request Body (POST)**:
  ```json
  {
    "title": "Best Interior Design 2024",
    "date_received": "2024-05-01",
    "description": "Award description"
  }
  ```
  
  Optional / nullable fields (not required):
  - `image`: optional (blank=True, null=True)
  - `date_received`: optional (blank=True, null=True)
  - `description`: optional (blank=True)
- **Response**: List of awards or created award
- **Status**: 200 OK / 201 Created

---

### 4. **Partners - List / Create**
- **Endpoint**: `GET /api/company/partners/` | `POST /api/company/partners/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/company/partners/`
  - Create: `http://localhost:8000/api/company/partners/`
- **Description**: List company partners
- **Request Body (POST)**:
  ```json
  {
    "name": "Furniture Co.",
    "website_url": "https://furniture.com"
  }
  ```
  
  Optional / nullable fields (not required):
  - `logo`: optional (blank=True, null=True)
  - `website_url`: optional (blank=True, null=True)
- **Response**: List of partners or created partner
- **Status**: 200 OK / 201 Created

---

### 5. **Testimonials - List / Create**
- **Endpoint**: `GET /api/company/testimonials/` | `POST /api/company/testimonials/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/company/testimonials/`
  - Create: `http://localhost:8000/api/company/testimonials/`
- **Description**: List client testimonials
- **Request Body (POST)**:
  ```json
  {
    "name": "Jane Doe",
    "designation": "Homeowner",
    "message": "Amazing service and design!"
  }
  ```
- **Response**: List of testimonials or created testimonial
- **Status**: 200 OK / 201 Created

---

## Contact Endpoints

All endpoints use the base path: `/api/contact/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/contact/`
- Production: `https://interior-ecommerce-backend.onrender.com/api/contact/`

### 1. **Contact Submissions - List / Create**
- **Endpoint**: `GET /api/contact/contact-submissions/` | `POST /api/contact/contact-submissions/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/contact/contact-submissions/`
  - Create: `http://localhost:8000/api/contact/contact-submissions/`
- **Description**: Submit or view contact form submissions
- **Request Body (POST)**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-1234",
    "message": "I'm interested in your services..."
  }
  ```
- **Response**: Submission created / List of submissions
- **Status**: 200 OK / 201 Created

---

### 2. **Contact Submissions - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/contact/contact-submissions/{id}/` | `PUT /api/contact/contact-submissions/{id}/` | `DELETE /api/contact/contact-submissions/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/contact/contact-submissions/1/`
  - Update: `http://localhost:8000/api/contact/contact-submissions/1/`
  - Delete: `http://localhost:8000/api/contact/contact-submissions/1/`
- **Description**: Get, update, or delete a specific submission

---

## Catalog Endpoints

All endpoints use the base path: `/api/catalog/`

**Complete URLs**:
- Local: `http://localhost:8000/api/catalog/`
- Production: `https://interior-ecommerce-backend.onrender.com/api/catalog/`

The `catalog` app uses a DRF router. Standard router patterns apply: `GET /resource/` (list), `POST /resource/` (create), `GET /resource/{id}/` (retrieve), `PUT/PATCH /resource/{id}/` (update), `DELETE /resource/{id}/` (delete).

### 1. **Categories - List / Create**
- **Endpoint**: `GET /api/catalog/categories/` | `POST /api/catalog/categories/`
- **Full URLs**:
  - List: `http://localhost:8000/api/catalog/categories/`
  - Create: `http://localhost:8000/api/catalog/categories/`
- **Description**: Manage product categories
- **Request Body (POST)**:
  ```json
  {
    "name": "Furniture",
    "slug": "furniture",
    "description": "All furniture products",
    "image": "<cloudinary_url_or_file>",
    "is_active": true
  }
  ```
  
  Optional / nullable fields (not required):
  - `description`: optional (blank=True, null=True)
  - `image`: optional (blank=True, null=True)
  - `is_active`: optional (defaults to true)

 - **Response**: Created category JSON (id, name, slug, ...)
- **Status**: 200 OK / 201 Created

---

### 2. **Products - List / Create**
- **Endpoint**: `GET /api/catalog/products/` | `POST /api/catalog/products/`
- **Full URLs**:
  - List: `http://localhost:8000/api/catalog/products/`
  - Create: `http://localhost:8000/api/catalog/products/`
- **Description**: List and create products. Products include basic info and link to variants for pricing.
- **Query Parameters (GET)**:
  - `search`: search by `name` or `description`
  - `category`: filter by category id
  - `is_active`: filter active products
  - `ordering`: `created_at`, `updated_at`
  - `page`: pagination
- **Request Body (POST)**:
  ```json
  {
    "name": "Modern Sofa",
    "slug": "modern-sofa",
    "description": "Comfortable modern sofa",
    "category": 1,
    "main_image": "<cloudinary_url_or_file>",
    "is_active": true
  }
  ```
  
  Optional / nullable fields (not required):
  - `description`: optional (blank=True, null=True)
  - `main_image`: optional (blank=True, null=True)
  - `category`: optional FK (null=True)

 - **Response**: Product JSON including `id`, `name`, `slug`, `main_image`, `is_active`, timestamps
- **Status**: 200 OK / 201 Created

---

### 3. **Product Images - List / Create**
- **Endpoint**: `GET /api/catalog/product-images/` | `POST /api/catalog/product-images/`
- **Full URLs**:
  - List: `http://localhost:8000/api/catalog/product-images/`
  - Create: `http://localhost:8000/api/catalog/product-images/`
- **Description**: Upload additional gallery images for products
- **Request Body (POST)**:
  ```json
  {
    "product": 1,
    "image": "<cloudinary_url_or_file>",
    "alt_text": "Sofa angle view",
    "is_featured": false
  }
  ```
  
  Optional / nullable fields (not required):
  - `alt_text`: optional (blank=True, null=True)
  - `is_featured`: optional (defaults to false)

 - **Response**: Created image object
- **Status**: 200 OK / 201 Created

---

### 4. **Variants - List / Create**
- **Endpoint**: `GET /api/catalog/variants/` | `POST /api/catalog/variants/`
- **Full URLs**:
  - List: `http://localhost:8000/api/catalog/variants/`
  - Create: `http://localhost:8000/api/catalog/variants/`
- **Description**: Manage product variants (price, sku, stock)
- **Request Body (POST)**:
  ```json
  {
    "product": 1,
    "sku": "SOFA-RED-L",
    "name": "Red / Large",
    "price": 1299.99,
    "stock": 50,
    "is_active": true
  }
  ```
  
  Optional / nullable fields (not required):
  - `image`: optional (blank=True, null=True)
  - `is_active`: optional (defaults to true)

 - **Response**: Created variant object
- **Status**: 200 OK / 201 Created

---

### 5. **Attributes - List / Create**
- **Endpoint**: `GET /api/catalog/attributes/` | `POST /api/catalog/attributes/`
- **Full URLs**:
  - List: `http://localhost:8000/api/catalog/attributes/`
  - Create: `http://localhost:8000/api/catalog/attributes/`
- **Description**: Manage attribute definitions (e.g., Color, Size) and attribute values
- **Request Body (POST)** (attribute):
  ```json
  { "name": "Color" }
  ```
- **Request Body (POST)** (attribute value):
  ```json
  { "attribute": 1, "value": "Red" }
  ```
  
  Optional / nullable fields (not required):
  - Attribute: none (name required)
  - AttributeValue: none (both fields required)
- **Status**: 200 OK / 201 Created

---

### 6. **Inventory - List / Create / Update**
- **Endpoint**: `GET /api/catalog/inventory/` | `POST /api/catalog/inventory/` | `PUT/PATCH /api/catalog/inventory/{id}/`
- **Full URLs**:
  - List: `http://localhost:8000/api/catalog/inventory/`
  - Create: `http://localhost:8000/api/catalog/inventory/`
  - Update: `http://localhost:8000/api/catalog/inventory/1/`
- **Description**: Inventory entries are linked to `ProductVariant` and track `quantity`, `reserved_stock`, and thresholds.
- **Request Body (POST/PUT)**:
  ```json
  {
    "variant": 1,
    "quantity": 100,
    "low_stock_threshold": 5
  }
  ```
 - **Response**: Inventory object
- **Status**: 200 OK / 201 Created
  
  Optional / nullable fields (not required):
  - `variant`: required (OneToOne relation to ProductVariant)
  - `quantity`: required (defaults to 0 if omitted)
  - `low_stock_threshold`: required (defaults to 0 if omitted)
  - `reserved_stock`: managed by system (optional, default 0) — do not set unless admin API supports it
  - `updated_at`: read-only (auto populated)

---

## Coupons Endpoints

Coupons are registered at the top-level `api/` (see main `urls.py`).

**Base path**: `/api/`

### 1. **Coupons - List / Create**
- **Endpoint**: `GET /api/coupons/` | `POST /api/coupons/`
- **Full URLs**:
  - List: `http://localhost:8000/api/coupons/`
  - Create: `http://localhost:8000/api/coupons/`
- **Description**: Admins can create/update/delete coupons. Non-admins can list and view.
- **Request Body (POST)**:
  ```json
  {
    "code": "WELCOME10",
    "description": "10% off for new customers",
    "discount_type": "percent",        
    "discount_value": 10.00,
    "min_purchase_amount": 50.00,
    "valid_from": "2025-01-01T00:00:00Z",
    "valid_until": "2025-12-31T23:59:59Z",
    "usage_limit": 100,
    "usage_limit_per_user": 1,
    "is_active": true
  }
  ```
  
  Optional / nullable fields (not required):
  - `description`: optional (blank=True)
  - `min_purchase_amount`: optional (null=True, blank=True)
  - `usage_limit`: optional (null=True, blank=True)
  - `usage_limit_per_user`: optional (null=True, blank=True)
  - `is_active`: optional (defaults to true)

- **Response**: Created coupon object (id, code, discount_type, discount_value, valid_from, valid_until, ...)
- **Status**: 200 OK / 201 Created

**Behavior / Permissions**:
- `CouponViewSet` uses `IsAdminOrReadOnly`: only admins may create/update/delete.
- Deletion is prevented if `CouponUsage` entries exist for that coupon (API will return 400 error).

---

### 2. **Coupon Usage - List (Admin)**
- **Endpoint**: `GET /api/coupon-usage/`
- **Full URL**: `http://localhost:8000/api/coupon-usage/`
- **Description**: Read-only list of coupon usage for admins. Returns records with `coupon`, `user`, `order`, `used_at`.
- **Status**: 200 OK

---

## Orders & Payments

Orders and payments are registered at top-level `/api/`.

### 1. **Orders - List / Create**
- **Endpoint**: `GET /api/orders/` | `POST /api/orders/`
- **Full URLs**:
  - List: `http://localhost:8000/api/orders/`
  - Create: `http://localhost:8000/api/orders/`
- **Description**: Authenticated users create orders; staff can list all orders. Order creation reserves stock and creates a payment record (COD by default).
- **Request Body (POST)** (see `OrderCreateSerializer`):
  ```json
  {
    "shipping_address_id": 12,
    "items": [
      { "variant_id": 5, "quantity": 2 },
      { "variant_id": 8, "quantity": 1 }
    ],
    "coupon_code": "WELCOME10"
  }
  ```
  
  Optional / nullable fields (not required):
  - `coupon_code`: optional (can be omitted or blank)

 - **Response**: Created order JSON (id, user, status, subtotal, shipping_cost, total, items, created_at)
- **Status**: 201 Created

---

### 2. **Orders - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/orders/{id}/` | `PUT/PATCH /api/orders/{id}/` | `DELETE /api/orders/{id}/`
- **Full URLs**:
  - Get: `http://localhost:8000/api/orders/1/`
  - Update: `http://localhost:8000/api/orders/1/`
  - Delete: `http://localhost:8000/api/orders/1/`
- **Permissions**: Users can access their own orders; staff may access all orders.

---

### 3. **Apply Coupon (Order-level)**
- **Endpoint**: `POST /api/orders/apply-coupon/`
- **Full URL**: `http://localhost:8000/api/orders/apply-coupon/`
- **Description**: Validates a coupon code against a provided `order_total` and returns discounted totals.
- **Request Body**:
  ```json
  {
    "code": "WELCOME10",
    "order_total": 250.00
  }
  ```
- **Response**:
  ```json
  {
    "valid": true,
    "coupon": "WELCOME10",
    "discount": 25.00,
    "total_after_discount": 225.00
  }
  ```
- **Status**: 200 OK

---

### 4. **Cancel Order**
- **Endpoint**: `POST /api/orders/{id}/cancel/`
- **Full URL**: `http://localhost:8000/api/orders/123/cancel/`
- **Description**: Cancels a pending order, restores reserved stock, and sets status to `cancelled`. Only allowed for orders with status `pending`.
- **Request Body**: none
- **Response**:
  ```json
  { "message": "Order cancelled." }
  ```
- **Status**: 200 OK (or 400 on invalid state)

---

### 5. **Payments (Read / Admin)**
- **Endpoint**: `GET /api/payments/` | `GET /api/payments/{id}/`
- **Full URLs**:
  - List: `http://localhost:8000/api/payments/`
  - Detail: `http://localhost:8000/api/payments/1/`
- **Description**: Payments are read-only via `PaymentViewSet` and restricted to admin users.
- **Response**: Payment object (id, order, method, status, transaction_id, paid_at)
- **Status**: 200 OK

---

### 6. **Admin Orders**
- **Endpoint**: `GET /api/admin/orders/` | `POST /api/admin/orders/` ...
- **Full URLs**:
  - List: `http://localhost:8000/api/admin/orders/`
- **Description**: Admin-specific order endpoints (registered in `apps.order.admin_urls`).

---

## Estimation Endpoints

All endpoints use the base path: `/api/estimation/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/estimation/`
- Production: `https://interior-ecommerce-backend.onrender.com/api/estimation/`

### 1. **Estimation Categories - List / Create**
- **Endpoint**: `GET /api/estimation/estimation-categories/` | `POST /api/estimation/estimation-categories/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/estimation/estimation-categories/`
  - Create: `http://localhost:8000/api/estimation/estimation-categories/`
- **Description**: List estimation/service categories
- **Request Body (POST)**:
  ```json
  {
    "name": "Residential Design"
  }
  ```
- **Response**: List of categories or created category
- **Status**: 200 OK / 201 Created

---

## Projects Endpoints

All endpoints use the base path: `/api/projects/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/projects/`
- Production: `https://interior-ecommerce-backend.onrender.com/api/projects/`

### 1. **Services - List / Create**
- **Endpoint**: `GET /api/projects/services/` | `POST /api/projects/services/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/projects/services/`
  - Create: `http://localhost:8000/api/projects/services/`
- **Description**: List services offered
- **Request Body (POST)**:
  ```json
  {
    "name": "Full Home Renovation",
    "slug": "full-home-renovation",
    "description": "Complete home renovation service"
  }
  ```
  
  Optional / nullable fields (not required):
  - `description`: optional (blank=True)
  - `cover_image`: optional (blank=True, null=True)

 - **Response**: List of services or created service
- **Status**: 200 OK / 201 Created

---

### 2. **Services - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/projects/services/{id}/` | `PUT /api/projects/services/{id}/` | `DELETE /api/projects/services/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/projects/services/1/`
  - Update: `http://localhost:8000/api/projects/services/1/`
  - Delete: `http://localhost:8000/api/projects/services/1/`
- **Description**: Get, update, or delete a specific service

---

### 3. **Projects - List / Create**
- **Endpoint**: `GET /api/projects/projects/` | `POST /api/projects/projects/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/projects/projects/`
  - Create: `http://localhost:8000/api/projects/projects/`
- **Description**: List all projects
- **Query Parameters (GET)**:
  - `search`: Search by title
  - `service`: Filter by service ID
  - `status`: Filter by status (Completed, Ongoing, Future)
  - `page`: Pagination
- **Request Body (POST)**:
  ```json
  {
    "title": "Modern Apartment Redesign",
    "slug": "modern-apartment-redesign",
    "description": "Complete apartment redesign project",
    "gallery_images": ["url1", "url2", "url3"],
    "location": "Brooklyn, NY",
    "date_completed": "2024-12-15",
    "status": "Completed",
    "is_featured": true,
    "service": 1,
    "team_ids": [1, 2, 3]
  }
  ```
  
  Optional / nullable fields (not required):
  - `gallery_images`: optional (JSONField, default=list)
  - `location`: optional (blank=True)
  - `date_completed`: optional (blank=True, null=True)
  - `service`: optional FK (null=True)
  - `team_ids`: optional (many-to-many, can be omitted)

 - **Response**: List of projects or created project
- **Status**: 200 OK / 201 Created

---

### 4. **Projects - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/projects/projects/{id}/` | `PUT /api/projects/projects/{id}/` | `DELETE /api/projects/projects/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/projects/projects/1/`
  - Update: `http://localhost:8000/api/projects/projects/1/`
  - Delete: `http://localhost:8000/api/projects/projects/1/`
- **Description**: Get, update, or delete a specific project

---

## Authentication Headers

For all **protected endpoints** (POST, PUT, DELETE), include:

```
Authorization: Bearer <access_token>
```

**Example**:
```
GET /api/projects/projects/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```