# API Endpoints Documentation for Frontend Integration

**Base URL**: `http://localhost:8000/` (local) | `https://interior-ecommerce-backend.onrender.com/` (production)

---

This document lists the current API endpoints defined in the backend and their expected behavior. URLs map to Django REST Framework viewsets and views. Protected endpoints require a JWT access token in the `Authorization` header: `Authorization: Bearer <access_token>`.

## Top-level route map

- `POST /api/accounts/` → accounts endpoints (see Authentication section)
- `GET/POST/PUT/DELETE /api/blog/...` → blog app
- `GET/POST/PUT/DELETE /api/cms/...` → cms app
- `GET/POST/PUT/DELETE /api/company/...` → company app
- `GET/POST/PUT/DELETE /api/contact/...` → contact app
- `GET/POST/PUT/DELETE /api/catalog/...` → catalog (products, variants, inventory)
- `GET/POST/PUT/DELETE /api/estimation/...` → estimation app
- `GET/POST/PUT/DELETE /api/projects/...` → projects app
- `GET/POST/PUT/DELETE /api/...` → order & coupons (registered at top-level `api/`)
- `GET/POST/PUT/DELETE /api/admin/...` → admin order endpoints

---

**Notes about pluralization & router behavior**: Many endpoints are registered via DRF routers and therefore follow the standard patterns: `GET /resource/` (list), `POST /resource/` (create), `GET /resource/{id}/` (retrieve), `PUT /resource/{id}/` (update), `PATCH /resource/{id}/` (partial update), `DELETE /resource/{id}/` (delete).

---

## Authentication / Accounts (`/api/accounts/`)

Base URLs:
- Local: `http://localhost:8000/api/accounts/`
- Production: `https://interior-ecommerce-backend.onrender.com/api/accounts/`

Endpoints:
- `POST token/refresh/` — `POST /api/accounts/token/refresh/`
  - Request: `{ "refresh": "<refresh_token>" }`
  - Response: `{ "access": "<access_token>" }`

- `POST register/` — `POST /api/accounts/register/`
  - Registers a new user. Request should include `email`, `password`, `first_name`, `last_name` (see serializer expectations).
  - New users are created with `is_active=False`; a verification email is sent. Response: 201 Created with `user` data and a message.

- `POST login/` — `POST /api/accounts/login/`
  - Login using email and password. Returns JWT `access` and `refresh` tokens on success.

- `POST google/` — `POST /api/accounts/google/`
  - Sign in/up using Google ID token provided in the body as `id_token`.
  - Response includes `tokens` (`access` and `refresh`), `user` info, and `is_new_user` flag.

- `GET verify-email/` — `GET /api/accounts/verify-email/?uid=<uid>&token=<token>`
  - Verifies an email link. Uses query params `uid` and `token`. On success marks `is_active=True`.

- `POST resend-verification/` — `POST /api/accounts/resend-verification/`
  - Request body: `{ "email": "user@example.com" }`. Sends a new verification email if the account exists and is not active. Returns 200 with a message (does not reveal account existence).

- `POST password-reset/request/` — `POST /api/accounts/password-reset/request/`
  - Request body: `{ "email": "user@example.com" }`. Sends a password reset email if the account exists. Returns 200.

- `GET password-reset/validate/?uid=<uid>&token=<token>` — `GET /api/accounts/password-reset/validate/`
  - Validates a password reset token, returns `{ "valid": true }` or `400`.

- `POST password-reset/complete/` — `POST /api/accounts/password-reset/complete/`
  - Request body: `{ "uid": "<uid>", "token": "<token>", "password": "<new_password>" }`. Completes the reset and sets the new password. Returns 200 on success.

- `GET/POST shipping-addresses/` — `GET /api/accounts/shipping-addresses/`, `POST /api/accounts/shipping-addresses/`
  - Authenticated users only. `GET` lists the user's addresses; `POST` creates a new shipping address for the authenticated user.

- `GET shipping-cost/` — `GET /api/accounts/shipping-cost/`
  - Authenticated-only action that returns the shipping cost for the user's first shipping address (calls `user_shipping_cost`).

Authentication headers:
- Protected endpoints require: `Authorization: Bearer <access_token>`

---

## Catalog (`/api/catalog/`)

Base:
- `http://localhost:8000/api/catalog/`

Registered resources (via router):
- `categories` — `GET/POST /api/catalog/categories/` and `GET/PUT/PATCH/DELETE /api/catalog/categories/{id}/`
- `products` — `GET/POST /api/catalog/products/` and detail
- `product-images` — `GET/POST /api/catalog/product-images/` and detail
- `variants` — `GET/POST /api/catalog/variants/` and detail
- `attributes` — `GET/POST /api/catalog/attributes/` and detail
- `inventory` — `GET/POST /api/catalog/inventory/` and detail

Querying & filters:
- `products` supports `search` (name, description), `category`, `is_active`, ordering (`created_at`, `updated_at`) and pagination.
- `inventory` supports filtering on `variant__product` and `variant` and searching by `variant__sku`.

Permissions:
- Most catalog endpoints use the `IsAdminOrReadOnly` permission: admin users can create/update/delete; public can list/retrieve.

---

## Blog (`/api/blog/`)

Resources:
- `categories` — `/api/blog/categories/`
- `posts` — `/api/blog/posts/`

Query params:
- `search`, `category`, `page` are supported for listing posts (see viewset filters).

---

## CMS (`/api/cms/`)

Resources:
- `pages`, `hero-slides`, `methodologies`, `faq` — standard list/create/detail routes at `/api/cms/<resource>/`

---

## Company (`/api/company/`)

Resources:
- `offices`, `team-members`, `awards`, `partners`, `testimonials` — standard router routes.

---

## Contact (`/api/contact/`)

Resources:
- `contact-submissions` — `/api/contact/contact-submissions/` (list/create and detail). Uses DRF router viewset.

---

## Estimation (`/api/estimation/`)

Resources:
- `estimation-categories` — `/api/estimation/estimation-categories/` (list/create and detail).

---

## Projects (`/api/projects/`)

Resources:
- `services` — `/api/projects/services/`
- `projects` — `/api/projects/projects/`

Querying:
- `projects` supports `search`, `service`, `status`, and pagination.

---

## Orders & Payments (`/api/`)

Order and payment endpoints are mounted at the top-level `api/` path (i.e. `GET /api/orders/`). Registered viewsets:
- `orders` — `/api/orders/`
  - Standard list/create/detail behavior.
  - Permissions: authenticated users; staff can list all orders. Users can only access their own orders.
  - Custom actions:
    - `POST /api/orders/apply-coupon/` (detail=False)
      - Body: `{ "code": "COUPONCODE", "order_total": <number> }` — validates coupon and returns discounted total and discount amount.
    - `POST /api/orders/{id}/cancel/` (detail=True)
      - Cancels a pending order, restores inventory, and sets status to `cancelled`. Requires authentication.
- `payments` — `/api/payments/` (read-only for admin users)

Admin order endpoints:
- `/api/admin/orders/` — admin-specific order management (registered in `apps.order.admin_urls`).

---

## Coupons (`/api/`)

Registered resources at top-level `api/`:
- `coupons` — `/api/coupons/` (admin full CRUD; read-only for non-admins)
- `coupon-usage` — `/api/coupon-usage/` (read-only history, admin-access)

Special behaviors:
- `CouponViewSet` protects deletion if there are usages (cannot delete coupons that have been used).

---

## Common headers & auth

- Protected endpoints require `Authorization: Bearer <access_token>`.
- For JSON requests, include `Content-Type: application/json`.

---

If you want, I can:
- Add example request/response payloads for any specific endpoint.
- Generate a compact JSON summary of endpoints the frontend can consume.
- Run a quick script to list all routes programmatically from Django (requires environment).

Next step: mark the todo steps for verification and finalize the doc. If you'd like extra examples or OpenAPI export, tell me which endpoints to prioritize.