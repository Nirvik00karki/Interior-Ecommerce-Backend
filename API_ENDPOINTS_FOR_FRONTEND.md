# API Endpoints Documentation for Frontend Integration

**Base URL**: `http://localhost:8000/` (local) | `https://<your-render-domain>/` (production)

---

## Authentication Endpoints

All endpoints use the base path: `/api/accounts/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/accounts/`
- Production: `https://<your-render-domain>/api/accounts/`

### 1. **User Registration**
- **Endpoint**: `POST /api/accounts/register/`
- **Full URL**: `http://localhost:8000/api/accounts/register/`
- **Description**: Register a new user
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
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
- **Endpoint**: `POST /api/accounts/verify-email/`
- **Full URL**: `http://localhost:8000/api/accounts/verify-email/`
- **Description**: Verify user email with OTP/token
- **Request Body**:
  ```json
  {
    "otp": "123456"
  }
  ```
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
- **Endpoint**: `POST /api/accounts/password-reset/validate/`
- **Full URL**: `http://localhost:8000/api/accounts/password-reset/validate/`
- **Description**: Validate password reset token
- **Request Body**:
  ```json
  {
    "token": "reset_token_from_email"
  }
  ```
- **Response**: Token validity confirmation
- **Status**: 200 OK

---

### 9. **Password Reset - Complete**
- **Endpoint**: `POST /api/accounts/password-reset/complete/`
- **Full URL**: `http://localhost:8000/api/accounts/password-reset/complete/`
- **Description**: Complete password reset with new password
- **Request Body**:
  ```json
  {
    "token": "reset_token_from_email",
    "new_password": "newsecurepassword123",
    "new_password2": "newsecurepassword123"
  }
  ```
- **Response**: Password updated
- **Status**: 200 OK

---

## Blog Endpoints

All endpoints use the base path: `/api/blog/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/blog/`
- Production: `https://<your-render-domain>/api/blog/`

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
    "slug": "technology",
    "description": "Tech related blogs"
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
    "category": 1,
    "featured_image": "<cloudinary_url_or_file>",
    "is_published": true
  }
  ```
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
- Production: `https://<your-render-domain>/api/cms/`

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
    "content": "Page content here...",
    "is_published": true
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
    "subtitle": "Transform Your Space",
    "image": "<cloudinary_url_or_file>",
    "order": 1,
    "is_active": true
  }
  ```
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
    "icon": "<cloudinary_url_or_file>",
    "order": 1
  }
  ```
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
    "order": 1,
    "is_active": true
  }
  ```
- **Response**: List of FAQs or created FAQ
- **Status**: 200 OK / 201 Created

---

## Company Endpoints

All endpoints use the base path: `/api/company/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/company/`
- Production: `https://<your-render-domain>/api/company/`

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
    "coordinates": "40.7128,-74.0060"
  }
  ```
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
    "title": "Senior Designer",
    "bio": "Experienced interior designer...",
    "photo": "<cloudinary_url_or_file>",
    "email": "john@company.com"
  }
  ```
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
    "year": 2024,
    "description": "Award description",
    "certificate": "<cloudinary_url_or_file>"
  }
  ```
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
    "logo": "<cloudinary_url_or_file>",
    "website": "https://furniture.com",
    "description": "Partner description"
  }
  ```
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
    "client_name": "Jane Doe",
    "client_title": "Homeowner",
    "testimonial_text": "Amazing service and design!",
    "rating": 5,
    "photo": "<cloudinary_url_or_file>"
  }
  ```
- **Response**: List of testimonials or created testimonial
- **Status**: 200 OK / 201 Created

---

## Contact Endpoints

All endpoints use the base path: `/api/contact/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/contact/`
- Production: `https://<your-render-domain>/api/contact/`

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
    "subject": "Project Inquiry",
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

## E-Commerce Endpoints

All endpoints use the base path: `/api/ecommerce/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/ecommerce/`
- Production: `https://<your-render-domain>/api/ecommerce/`

### 1. **Product Categories - List / Create**
- **Endpoint**: `GET /api/ecommerce/product-categories/` | `POST /api/ecommerce/product-categories/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/ecommerce/product-categories/`
  - Create: `http://localhost:8000/api/ecommerce/product-categories/`
- **Description**: List product categories
- **Request Body (POST)**:
  ```json
  {
    "name": "Furniture",
    "slug": "furniture",
    "description": "All furniture products"
  }
  ```
- **Response**: List of categories or created category
- **Status**: 200 OK / 201 Created

---

### 2. **Products - List / Create**
- **Endpoint**: `GET /api/ecommerce/products/` | `POST /api/ecommerce/products/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/ecommerce/products/`
  - Create: `http://localhost:8000/api/ecommerce/products/`
- **Description**: List all products
- **Query Parameters (GET)**:
  - `search`: Search by name
  - `category`: Filter by category ID
  - `min_price`, `max_price`: Price range filter
  - `page`: Pagination
- **Request Body (POST)**:
  ```json
  {
    "name": "Modern Sofa",
    "slug": "modern-sofa",
    "description": "Comfortable modern sofa",
    "category": 1,
    "price": 1299.99,
    "quantity": 50,
    "image": "<cloudinary_url_or_file>"
  }
  ```
- **Response**: List of products or created product
- **Status**: 200 OK / 201 Created

---

### 3. **Products - Retrieve / Update / Delete**
- **Endpoint**: `GET /api/ecommerce/products/{id}/` | `PUT /api/ecommerce/products/{id}/` | `DELETE /api/ecommerce/products/{id}/`
- **Full URLs**: 
  - Get: `http://localhost:8000/api/ecommerce/products/1/`
  - Update: `http://localhost:8000/api/ecommerce/products/1/`
  - Delete: `http://localhost:8000/api/ecommerce/products/1/`
- **Description**: Get, update, or delete a specific product

---

## Estimation Endpoints

All endpoints use the base path: `/api/estimation/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/estimation/`
- Production: `https://<your-render-domain>/api/estimation/`

### 1. **Estimation Categories - List / Create**
- **Endpoint**: `GET /api/estimation/estimation-categories/` | `POST /api/estimation/estimation-categories/`
- **Full URLs**: 
  - List: `http://localhost:8000/api/estimation/estimation-categories/`
  - Create: `http://localhost:8000/api/estimation/estimation-categories/`
- **Description**: List estimation/service categories
- **Request Body (POST)**:
  ```json
  {
    "name": "Residential Design",
    "description": "For home interior design projects",
    "base_cost": 500
  }
  ```
- **Response**: List of categories or created category
- **Status**: 200 OK / 201 Created

---

## Projects Endpoints

All endpoints use the base path: `/api/projects/`

**Complete URLs**: 
- Local: `http://localhost:8000/api/projects/`
- Production: `https://<your-render-domain>/api/projects/`

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
    "description": "Complete home renovation service",
    "cover_image": "<cloudinary_url_or_file>"
  }
  ```
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
    "cover_image": "<cloudinary_url_or_file>",
    "gallery_images": ["url1", "url2", "url3"],
    "location": "Brooklyn, NY",
    "date_completed": "2024-12-15",
    "status": "Completed",
    "is_featured": true,
    "service": 1,
    "team_ids": [1, 2, 3]
  }
  ```
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