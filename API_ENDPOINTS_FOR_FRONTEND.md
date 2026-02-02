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
- **Response**: User created, returns token and verification status.
  ```json
  {
    "message": "Registration successful. Please check your email to verify your account.",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe"
    },
    "email_sent": true,
    "email_error": null
  }
  ```
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

### 10. **User Profile - Get / Update**
- **Endpoint**: `GET /api/accounts/profile/` | `PATCH /api/accounts/profile/`
- **Full URL**: `http://localhost:8000/api/accounts/profile/`
- **Description**: Retrieve or update the authenticated user's profile information
- **Authentication**: Required (Bearer token)
- **Request Headers**:
  ```
  Authorization: Bearer <your_access_token>
  ```

#### 10.1 GET - Retrieve User Profile
- **Request**: No body required
- **Response**: Current user's profile data
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "google_id": null,
    "avatar": null,
    "is_staff": false
  }
  ```
- **Status**: 200 OK

#### 10.2 PATCH - Update User Profile
- **Description**: Partial update of user profile (only send fields to update)
- **Request Body**:
  ```json
  {
    "first_name": "Jane",
    "last_name": "Smith"
  }
  ```
  
  Or to update password:
  ```json
  {
    "password": "newSecurePassword123"
  }
  ```
  
  Updatable fields:
  - `first_name`: optional
  - `last_name`: optional
  - `password`: optional (will be hashed)
  
  **Note**: `email`, `google_id`, `avatar`, and `is_staff` are read-only
- **Response**: Updated user profile
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "full_name": "Jane Smith",
    "google_id": null,
    "avatar": null,
    "is_staff": false
  }
  ```
- **Status**: 200 OK / 400 Bad Request

---

### 11. **Shipping & Addresses**
All endpoints use the base path: `/api/accounts/`

#### 11.1 **List / Create Shipping Addresses**
- **Endpoint**: `GET /api/accounts/shipping-addresses/` | `POST /api/accounts/shipping-addresses/`
- **Description**: Manage user's saved shipping addresses.
- **Request Body (POST)**:
  ```json
  {
    "full_name": "John Doe",
    "phone": "9800000000",
    "address_line1": "Kathmandu, Nepal",
    "address_line2": "Next to the mall",
    "zone": 1,
    "state": "Bagmati",
    "postal_code": "44600",
    "country": "Nepal"
  }
  ```
- **Response**: List of addresses or created address object.
- **Status**: 200 OK / 201 Created

#### 11.2 **Get Shipping Cost**
- **Endpoint**: `GET /api/accounts/shipping-cost/`
- **Description**: Calculate shipping cost based on the user's primary (latest) address.
- **Response**:
  ```json
  {
    "shipping_cost": 100.00
  }
  ```
- **Status**: 200 OK / 404 Not Found (if no address)

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
- **Endpoint**: `GET /api/blog/categories/slug/{slug}/` | `PUT /api/blog/categories/{id}/` | `DELETE /api/blog/categories/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/blog/categories/slug/technology/`
  - Update: `http://localhost:8000/api/blog/categories/3/`
  - Delete: `http://localhost:8000/api/blog/categories/3/`
- **Description**: Get (by slug), update, or delete a specific blog category (update/delete use numeric ID)

- **Alternate slug endpoint (action)**: `GET /api/blog/categories/slug/{slug}/`
  - Get: `http://localhost:8000/api/blog/categories/slug/technology/`

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
    "cover_image": "<image_file>",
    "blog_category": 1,
    "excerpt": "Short excerpt...",
    "tags": "design, trends",
    "author": "Jane Author",
    "is_published": true
  }
  ```
  
  Optional / nullable fields (not required):
  - `excerpt`: optional (blank=True)
  - `tags`: optional (string, e.g. "modern, sleek")
  - `blog_category`: nullable FK (null=True) — optional
- **Response**: List of posts or created post
- **Status**: 200 OK / 201 Created

---

### 4. **Blog Posts - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/blog/posts/slug/{slug}/` | `PUT /api/blog/posts/{id}/` | `DELETE /api/blog/posts/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/blog/posts/slug/interior-design-trends-2025/`
  - Update: `http://localhost:8000/api/blog/posts/123/`
  - Delete: `http://localhost:8000/api/blog/posts/123/`
- **Description**: Get (by slug), update, or delete a specific blog post (update/delete use numeric ID)

- **Alternate slug endpoint (action)**: `GET /api/blog/posts/slug/{slug}/`
  - Get: `http://localhost:8000/api/blog/posts/slug/interior-design-trends-2025/`

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

### 1.5 **Pages - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/cms/pages/slug/{slug}/` | `PUT /api/cms/pages/{id}/` | `DELETE /api/cms/pages/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/cms/pages/slug/about-us/`
  - Update: `http://localhost:8000/api/cms/pages/5/`
  - Delete: `http://localhost:8000/api/cms/pages/5/`
- **Description**: Get (by slug), update, or delete a specific page (update/delete use numeric ID)

- **Alternate slug endpoint (action)**: `GET /api/cms/pages/slug/{slug}/`
  - Get: `http://localhost:8000/api/cms/pages/slug/about-us/`

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

### 5. **Partners - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/company/partners/slug/{slug}/` | `PUT /api/company/partners/{id}/` | `DELETE /api/company/partners/{id}/`
- **Full URLs**:
  - Get: `http://localhost:8000/api/company/partners/slug/furniture-co/`
  - Update: `http://localhost:8000/api/company/partners/7/`
  - Delete: `http://localhost:8000/api/company/partners/7/`
- **Description**: Get (by slug), update, or delete a partner (update/delete use numeric ID)
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
- **Note**: Contact submissions use numeric ID lookup (no slug field)

---

## Catalog Endpoints

All endpoints use the base path: `/api/catalog/`

**Complete URLs**:
- Local: `http://localhost:8000/api/catalog/`
- Production: `https://interior-ecommerce-backend.onrender.com/api/catalog/`


**Note on ID vs slug lookups**: Some apps expose a slug-based action for retrieval in addition to the standard router endpoints. Use `GET /resource/slug/{slug}/` to retrieve by slug when available. For updates and deletes, use the numeric ID endpoints: `PUT/PATCH /resource/{id}/` and `DELETE /resource/{id}/`. For catalog and many other standard resources the DRF router `GET /resource/{id}/` (retrieve), `PUT/PATCH /resource/{id}/` (update), and `DELETE /resource/{id}/` (delete) still apply.


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

---

### 2.1 **Products - Retrieve by Slug (action)**
- **Endpoint**: `GET /api/catalog/products/slug/{slug}/`
- **Full URLs**:
  - Get: `http://localhost:8000/api/catalog/products/slug/modern-sofa/`
- **Description**: Retrieve a product by slug using the viewset action (useful to avoid PK/slug collisions)

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
  
  - `description`: optional (blank=True, null=True)
  - `main_image`: optional (blank=True, null=True)
  - `category`: optional FK (null=True)

 - **Response**: Product JSON including `id`, `name`, `slug`, `main_image`, `is_active`, `average_rating`, `review_count`, timestamps
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
- **Note**: Inventory uses numeric ID lookup (no slug field)
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

- **Response**: Created coupon object (id, code, discount_type, discount_value, valid_from, valid_to, ...)
- **Status**: 200 OK / 201 Created

**Behavior / Permissions**:
- `CouponViewSet` uses `IsAdminOrReadOnly`: only admins may create/update/delete.
- Deletion is prevented if `CouponUsage` entries exist for that coupon (API will return 400 error).

---

### 2. **Coupons - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/coupons/{code}/` | `PUT /api/coupons/{code}/` | `DELETE /api/coupons/{code}/`
- **Full URLs**:
  - Get: `http://localhost:8000/api/coupons/WELCOME10/`
  - Update: `http://localhost:8000/api/coupons/WELCOME10/`
  - Delete: `http://localhost:8000/api/coupons/WELCOME10/`
- **Description**: Get, update, or delete a specific coupon by its code

---

### 3. **Coupon Usage - List (Admin)**
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

## Wishlist Endpoints

All endpoints use the base path: `/api/wishlist/`

### 1. **Wishlist items - List / Add**
- **Endpoint**: `GET /api/wishlist/items/` | `POST /api/wishlist/items/`
- **Description**: Manage user's personal wishlist.
- **Request Body (POST)**:
  ```json
  {
    "product": 1
  }
  ```
- **Response**: List of wishlist items or created item.
- **Note**: `product_details` are included in the response for display.
- **Status**: 200 OK / 201 Created

### 2. **Wishlist items - Remove**
- **Endpoint**: `DELETE /api/wishlist/items/{id}/`
- **Description**: Remove an item from wishlist using its primary ID.
- **Status**: 204 No Content

---

## Shopping Cart Endpoints

All endpoints use the base path: `/api/cart/`

### 1. **Cart - View**
- **Endpoint**: `GET /api/cart/`
- **Description**: Get current user's cart (auto-created if not exists).
- **Response**: Includes `items` (with `variant_details`), `total_price`, and `total_items`.
- **Status**: 200 OK

### 2. **Cart - Add Item**
- **Endpoint**: `POST /api/cart/add-item/`
- **Description**: Add a product variant to the cart.
- **Request Body**:
  ```json
  {
    "variant_id": 5,
    "quantity": 2
  }
  ```
- **Status**: 200 OK

### 3. **Cart - Update Item**
- **Endpoint**: `POST /api/cart/update-item/`
- **Description**: Update quantity of an item in the cart.
- **Request Body**:
  ```json
  {
    "variant_id": 5,
    "quantity": 3
  }
  ```
- **Note**: Setting quantity to 0 removes the item.
- **Status**: 200 OK

### 4. **Cart - Remove Item**
- **Endpoint**: `POST /api/cart/remove-item/`
- **Description**: Remove a specific variant from the cart.
- **Request Body**:
  ```json
  {
    "variant_id": 5
  }
  ```
- **Status**: 200 OK

### 5. **Cart - Clear**
- **Endpoint**: `POST /api/cart/clear/`
- **Description**: Empty the entire cart.
- **Status**: 200 OK

---

## Product Reviews & Ratings Endpoints

All endpoints use the base path: `/api/reviews/`

### 1. **Reviews - List**
- **Endpoint**: `GET /api/reviews/`
- **Description**: List all active reviews.
- **Query Parameters**:
  - `product`: Filter by product ID (Required for specific product reviews)
  - `ordering`: `created_at`, `rating`
- **Status**: 200 OK

### 2. **Reviews - Create**
- **Endpoint**: `POST /api/reviews/`
- **Description**: Post a review for a product. (Authenticated only, one per product).
- **Request Body (Multipart/Form-Data)**:
  - `product`: integer (ID)
  - `rating`: integer (1-5)
  - `comment`: string (optional)
  - `image`: file (optional)
- **Status**: 201 Created

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
- **Query Parameters (GET)**:
  - `parent`: Filter by parent service ID
  - `type`: Filter by type (service, product, both)
  - `is_ksp`: Filter by KSP status (true/false)
- **Request Body (POST)**:
  ```json
  {
    "name": "Full Home Renovation",
    "slug": "full-home-renovation",
    "description": "Complete home renovation service",
    "cover_image": "<image_file>",
    "icon": "<icon_file>",
    "parent": null,
    "type": "service",
    "is_ksp": false
  }
  ```
  
  Required fields:
  - `name`: required (max_length=100)
  - `slug`: required (unique)
  - `type`: required (choices: service, product, both)

  Optional / nullable fields (not required):
  - `description`: optional (blank=True)
  - `cover_image`: required (CloudinaryField)
  - `icon`: optional (CloudinaryField, blank=True, null=True)
  - `parent`: optional (ForeignKey to Service, null=True)
  - `is_ksp`: optional (defaults to False)

 - **Response**: List of services or created service
- **Status**: 200 OK / 201 Created

---

### 2. **Services - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/projects/services/slug/{slug}/` | `PUT /api/projects/services/{id}/` | `DELETE /api/projects/services/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/projects/services/slug/full-home-renovation/`
  - Update: `http://localhost:8000/api/projects/services/3/`
  - Delete: `http://localhost:8000/api/projects/services/3/`
- **Description**: Get (by slug), update, or delete a specific service (update/delete use numeric ID)

- **Alternate slug endpoint (action)**: `GET /api/projects/services/slug/{slug}/`
  - Get: `http://localhost:8000/api/projects/services/slug/full-home-renovation/`

---

### 3. **Sectors - List / Create**
- **Endpoint**: `GET /api/projects/sectors/` | `POST /api/projects/sectors/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/projects/sectors/`
  - Create: `http://localhost:8000/api/projects/sectors/`
- **Description**: List all project sectors (categories)
- **Request Body (POST)**:
  ```json
  {
    "name": "Commercial",
    "slug": "commercial",
    "description": "Commercial real estate projects",
    "cover_image": "<image_file>",
    "icon": "<icon_file>"
  }
  ```
  
  Fields:
  - `name`: required (max_length=100, unique)
  - `slug`: required (unique)
  - `description`: optional (blank=True)
  - `cover_image`: optional (CloudinaryField, blank=True, null=True)
  - `icon`: optional (CloudinaryField, blank=True, null=True)

- **Response**: List of sectors or created sector
- **Status**: 200 OK / 201 Created

---

### 4. **Sectors - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/projects/sectors/slug/{slug}/` | `PUT /api/projects/sectors/{id}/` | `DELETE /api/projects/sectors/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/projects/sectors/slug/commercial/`
  - Update: `http://localhost:8000/api/projects/sectors/4/`
  - Delete: `http://localhost:8000/api/projects/sectors/4/`
- **Description**: Get (by slug), update, or delete a specific sector (update/delete use numeric ID)

- **Alternate slug endpoint (action)**: `GET /api/projects/sectors/slug/{slug}/`
  - Get: `http://localhost:8000/api/projects/sectors/slug/commercial/`

---

### 7. **Projects - List / Create**
- **Endpoint**: `GET /api/projects/projects/` | `POST /api/projects/projects/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/projects/projects/`
  - Create: `http://localhost:8000/api/projects/projects/`
- **Description**: List all projects
- **Query Parameters (GET)**:
  - `sector`: Filter by sector slug/ID
  - `services`: Filter by service ID
  - `status`: Filter by status (completed, ongoing, future)
  - `is_featured`: Filter by featured status (true/false)
- **Request Body (POST)**:
  ```json
  {
    "title": "Modern Apartment Redesign",
    "slug": "modern-apartment-redesign",
    "description": "Complete apartment redesign project",
    "cover_image": "<image_file>",
    "location": "Brooklyn, NY",
    "date_completed": "2024-12-15",
    "status": "completed",
    "is_featured": true,
    "sector": 1,
    "services": [1, 2],
    "gallery_images": [
      {"image": "<image_file>"},
      {"image": "<image_file>"}
    ]
  }
  ```
  
  Required fields:
  - `title`: required (max_length=200)
  - `slug`: required (unique)
  - `description`: required
  - `cover_image`: required (CloudinaryField)
  - `status`: required (choices: completed, ongoing, future)

  Optional / nullable fields (not required):
  - `location`: optional (blank=True)
  - `date_completed`: optional (blank=True, null=True)
  - `is_featured`: optional (default=False)
  - `sector`: optional (ForeignKey to Sector, null=True)
  - `services`: optional (ManyToMany to Service through ProjectServiceLink)
  - `gallery_images`: optional (nested array of ProjectGalleryImage)

- **Response**: List of projects or created project
- **Status**: 200 OK / 201 Created

---

### 8. **Projects - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/projects/projects/slug/{slug}/` | `PUT /api/projects/projects/{id}/` | `DELETE /api/projects/projects/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/projects/projects/slug/modern-apartment-redesign/`
  - Update: `http://localhost:8000/api/projects/projects/8/`
  - Delete: `http://localhost:8000/api/projects/projects/8/`
- **Description**: Get (by slug), update, or delete a project (update/delete use numeric ID)

- **Alternate slug endpoint (action)**: `GET /api/projects/projects/slug/{slug}/`
  - Get: `http://localhost:8000/api/projects/projects/slug/modern-apartment-redesign/`
  ```json
  {
    "id": 1,
    "title": "Modern Apartment Redesign",
    "slug": "modern-apartment-redesign",
    "description": "Complete apartment redesign project",
    "cover_image_url": "https://cloudinary.com/...",
    "location": "Brooklyn, NY",
    "date_completed": "2024-12-15",
    "status": "completed",
    "is_featured": true,
    "sector": 1,
    "services": [1, 2],
    "gallery_images": [
      {
        "id": 10,
        "image_url": "https://cloudinary.com/..."
      },
      {
        "id": 11,
        "image_url": "https://cloudinary.com/..."
      }
    ]
  }
  ```

---

### 9. **Project Gallery Images**
- **Endpoint**: `GET /api/projects/project-gallery-images/` | `POST /api/projects/project-gallery-images/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/projects/project-gallery-images/`
  - Create: `http://localhost:8000/api/projects/project-gallery-images/`
- **Description**: Manage project gallery images
- **Query Parameters (GET)**:
  - `project`: Filter by project ID
- **Request Body (POST)**:
  ```json
  {
    "project": 1,
    "image": "<image_file>"
  }
  ```
- **Response**: Gallery image object with image_url
- **Status**: 200 OK / 201 Created
  - Remove Image: `http://localhost:8000/api/projects/projects/1/gallery/5/`
- **Description**: Add or remove gallery images from a project
- **Request Body (POST)**:
  ```json
  {
    "image": "<image_file>"
  }
  ```
- **Response (POST)**: Created gallery image object
  ```json
  {
    "id": 10,
    "image_url": "https://cloudinary.com/..."
  }
  ```
- **Status**: 201 Created (POST) / 204 No Content (DELETE)

---

### 10. **Packages - List / Create**
- **Endpoint**: `GET /api/projects/packages/` | `POST /api/projects/packages/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/projects/packages/`
  - Create: `http://localhost:8000/api/projects/packages/`
- **Description**: List and manage project packages with pricing and timelines
- **Query Parameters (GET)**:
  - `is_published`: Filter by published status (true/false)
- **Request Body (POST)**:
  ```json
  {
    "name": "Premium Package",
    "slug": "premium-package",
    "cover_image": "<image_file>",
    "project_design_time": 30,
    "project_manufacture_time": 45,
    "project_installation_time": 15,
    "basic_price": 5000.00,
    "premium_price": 8000.00,
    "support_service": "24/7 customer support and maintenance",
    "is_published": true,
    "items": [
      {"product_id": 1},
      {"product_id": 2}
    ]
  }
  ```
  
  Required fields:
  - `name`: required (max_length=100)
  - `slug`: required (unique)
  - `cover_image`: required (CloudinaryField)
  - `project_design_time`: required (PositiveInteger - days)
  - `project_manufacture_time`: required (PositiveInteger - days)
  - `project_installation_time`: required (PositiveInteger - days)
  - `basic_price`: required (Decimal)
  - `premium_price`: required (Decimal)

  Optional / nullable fields (not required):
  - `support_service`: optional (TextField)
  - `is_published`: optional (defaults to False)
  - `items`: optional (nested array of PackageItems with product_id)

- **Response**: List of packages or created package
- **Status**: 200 OK / 201 Created

---

### 11. **Packages - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/projects/packages/slug/{slug}/` | `PUT /api/projects/packages/{id}/` | `DELETE /api/projects/packages/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/projects/packages/slug/premium-package/`
  - Update: `http://localhost:8000/api/projects/packages/12/`
  - Delete: `http://localhost:8000/api/projects/packages/12/`
- **Description**: Get (by slug), update, or delete a specific package (update/delete use numeric ID)

- **Alternate slug endpoint (action)**: `GET /api/projects/packages/slug/{slug}/`
  - Get: `http://localhost:8000/api/projects/packages/slug/premium-package/`

---

### 12. **Package Items - List / Create**
- **Endpoint**: `GET /api/projects/package-items/` | `POST /api/projects/package-items/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/projects/package-items/`
  - Create: `http://localhost:8000/api/projects/package-items/`
- **Description**: List and manage individual items within packages
- **Query Parameters (GET)**:
  - `package`: Filter by package ID
- **Request Body (POST)**:
  ```json
  {
    "package": 1,
    "product_id": 5
  }
  ```
  
  Required fields:
  - `package`: required (ForeignKey to Package)
  - `product_id`: required (PositiveInteger)

- **Response**: List of package items or created item
- **Status**: 200 OK / 201 Created

---

## Data Models Reference

### **Project Model**
```
id: Integer (Primary Key)
title: String (max_length=200, required)
slug: String (unique, required)
description: Text (required)
cover_image: CloudinaryField (required)
location: String (max_length=200, optional)
date_completed: Date (optional, null=True)
status: String (choices: "completed", "ongoing", "future", required)
is_featured: Boolean (default=False)
sector: ForeignKey to Sector (optional, null=True)
services: ManyToMany to Service through ProjectServiceLink
team: ForeignKey to TeamMember (optional, null=True, blank=True)
created_at: DateTime (auto_now_add=True)
```

### **Sector Model**
```
id: Integer (Primary Key)
name: String (max_length=100, unique, required)
slug: String (unique, required)
description: Text (optional)
cover_image: CloudinaryField (optional, null=True)
icon: CloudinaryField (optional, null=True)
```

### **Service Model**
```
id: Integer (Primary Key)
name: String (max_length=100, required)
slug: String (unique, required)
description: Text (optional)
cover_image: CloudinaryField (required)
icon: CloudinaryField (optional, null=True)
parent: ForeignKey to Service (self-referential, optional, null=True)
type: String (choices: "service", "product", "both", required)
is_ksp: Boolean (default=False)
```

### **ServiceList Model**
```
id: Integer (Primary Key)
service: ForeignKey to Service (required)
name: String (max_length=100, required)
slug: String (required, must be unique per service)
cover_image: CloudinaryField (optional, null=True)
```

### **ProjectGalleryImage Model**
```
id: Integer (Primary Key)
project: ForeignKey to Project (required)
image: CloudinaryField (required)
```

### **ProjectServiceLink Model** (Through table)
```
id: Integer (Primary Key)
project: ForeignKey to Project (required)
service: ForeignKey to Service (required)
unique_together: (project, service)
```

### **Package Model**
```
id: Integer (Primary Key)
name: String (max_length=100, required)
slug: String (unique, required)
cover_image: CloudinaryField (required)
project_design_time: PositiveInteger (days, required)
project_manufacture_time: PositiveInteger (days, required)
project_installation_time: PositiveInteger (days, required)
basic_price: Decimal (10 digits, 2 decimals, required)
premium_price: Decimal (10 digits, 2 decimals, required)
support_service: TextField (optional)
is_published: Boolean (default=False)
```

### **PackageItem Model**
```
id: Integer (Primary Key)
package: ForeignKey to Package (required)
product_id: PositiveInteger (required)
```

---

## Serializers Reference

### **ProjectSerializer**
Serializes the Project model with the following fields:
- `id`: Integer (read-only)
- `title`: String
- `slug`: String
- `description`: String
- `cover_image`: ImageField (write-only on create/update)
- `cover_image_url`: String (read-only, dynamically generated from Cloudinary)
- `location`: String
- `date_completed`: Date
- `status`: String
- `is_featured`: Boolean
- `sector`: PrimaryKeyRelatedField (accepts Sector ID)
- `services`: List of PrimaryKeyRelatedField (accepts Service IDs, many=True)
- `gallery_images`: List of ProjectGalleryImageSerializer objects (read-only on GET, write-only nested on POST/PUT)

**Features**:
- Handles cover image upload to Cloudinary
- Supports multiple services through ProjectServiceLink
- Supports nested gallery images creation/update
- Automatically manages gallery images (deletes old ones on update)
- Handles services ManyToMany relationship (creates/updates ProjectServiceLink entries)

### **SectorSerializer**
Serializes the Sector model with the following fields:
- `id`: Integer (read-only)
- `name`: String
- `slug`: String
- `description`: String
- `cover_image_url`: String (read-only, dynamically generated from Cloudinary)
- `icon_url`: String (read-only, dynamically generated from Cloudinary)

### **ServiceSerializer**
Serializes the Service model with the following fields:
- `id`: Integer (read-only)
- `name`: String
- `slug`: String
- `description`: String
- `cover_image`: ImageField (write-only on create/update)
- `cover_image_url`: String (read-only, dynamically generated from Cloudinary)
- `parent`: PrimaryKeyRelatedField (accepts Service ID, optional)
- `type`: String (choices: service, product, both)
- `is_ksp`: Boolean

**Features**:
- Handles image upload to Cloudinary
- Supports self-referential parent-child relationships
- Supports create and update operations with image handling

### **ServiceListSerializer**
Serializes the ServiceList model with the following fields:
- `id`: Integer (read-only)
- `name`: String
- `slug`: String
- `service`: Integer (ForeignKey to Service)
- `cover_image_url`: String (read-only, dynamically generated from Cloudinary)

### **ProjectGalleryImageSerializer**
Serializes the ProjectGalleryImage model with the following fields:
- `id`: Integer (read-only)
- `image`: ImageField (write-only on create/update)
- `image_url`: String (read-only, dynamically generated from Cloudinary)

### **PackageSerializer**
Serializes the Package model with the following fields:
- `id`: Integer (read-only)
- `name`: String
- `slug`: String
- `cover_image`: ImageField (write-only on create/update)
- `cover_image_url`: String (read-only, dynamically generated from Cloudinary)
- `project_design_time`: Integer
- `project_manufacture_time`: Integer
- `project_installation_time`: Integer
- `basic_price`: Decimal
- `premium_price`: Decimal
- `support_service`: String
- `is_published`: Boolean
- `items`: List of PackageItemSerializer objects (nested)

**Features**:
- Handles cover image upload to Cloudinary
- Supports nested package items creation/update
- Automatically manages items (deletes old ones on update)

### **PackageItemSerializer**
Serializes the PackageItem model with the following fields:
- `id`: Integer (read-only)
- `product_id`: Integer

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