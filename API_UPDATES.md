# Backend API Updates - Jan 2026

## Recent Changes

This document tracks the recent backend improvements that affect API behavior.

### 1. Stock Validation in Cart
**Affected Endpoints**: 
- `POST /api/cart/add-item/`
- `POST /api/cart/update-item/`

**Changes**:
- Both endpoints now validate available stock before adding/updating items
- Returns 400 error with stock availability information if insufficient
- Uses `available_stock` (stock - reserved_stock) to prevent overselling

**Example Error Response**:
```json
{
  "error": "Insufficient stock. Available: 5, Requested: 10"
}
```

---

### 2. Verified Purchase Requirement for Reviews
**Affected Endpoints**: 
- `POST /api/reviews/`

**Changes**:
- Users can only review products they've purchased and received
- Order must have status "delivered" or "completed"
- One review per product per user (existing constraint)

**Example Error Response**:
```json
{
  "error": "You can only review products you have purchased and received."
}
```

---

### 3. Product Rating Cache 
**Affected Endpoints**: 
- `GET /api/catalog/products/`
- `GET /api/catalog/products/{id}/`
- `GET /api/catalog/products/slug/{slug}/`

**Changes**:
- Product responses now include `average_rating` (decimal) and `review_count` (integer)
- These fields are cached and auto-updated via signals when reviews change
- Significant performance improvement for product listings

**Updated Response**:
```json
{
  "id": 1,
  "name": "Modern Sofa",
  "average_rating": 4.5,
  "review_count": 12,
  ...
}
```

---

### 4. Coupon Field Name Fix 
**Affected Endpoints**: 
- `GET /api/coupons/`
- `POST /api/coupons/`
- `PUT /api/coupons/{code}/`

**Changes**:
- Field name changed from `valid_until` to `valid_to`
- Affects request and response bodies

**Updated Request/Response**:
```json
{
  "code": "WELCOME10",
  "valid_from": "2025-01-01T00:00:00Z",
  "valid_to": "2025-12-31T23:59:59Z"
}
```

---

### 5. Automatic Cart Clearing 
**Affected Behavior**: 
- Order creation process

**Changes**:
- Cart is automatically cleared when order is successfully created
- Happens via Django signal, no API change required
- Prevents stale cart items after checkout

---

### 6. Automatic Inventory Creation 
**Affected Behavior**: 
- Product variant creation

**Changes**:
- Inventory record is automatically created when ProductVariant is created
- Default: stock=0, low_stock_threshold=10
- Ensures consistent inventory tracking

---

### 7. Contact Notification Emails 
**Affected Endpoints**: 
- `POST /api/contact/contact-submissions/`

**Changes**:
- Admin receives automatic email notification on new contact submissions
- Fails silently if email service unavailable
- No API response changes

---

## Migration Required

Database migrations are required for the following changes:
- Product model: Added `average_rating` and `review_count` fields
- Cart model: Added database index on `user` field
- Wishlist model: Added database index on `user` field
- ContactSubmission model: Added database index on `is_read` field
- Coupon model: Added `related_name="usages"` to CouponUsage relationship

**Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

**Backfill product ratings** (optional but recommended):
```bash
python manage.py backfill_ratings
```

---

## Breaking Changes

### ⚠️ Coupon Field Name
**Old**: `valid_until`  
**New**: `valid_to`

**Action Required**: Update frontend to use `valid_to` instead of `valid_until` in coupon forms and displays.

---

## Non-Breaking Enhancements

All other changes are backward compatible or add new validation that improves data integrity without breaking existing integrations.
