# coupons/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.catalog.models import Product, Category
# from apps.order.models import Order

class Coupon(models.Model):
    """
    Standard ecommerce coupon system.
    Supports percentage or fixed amount discounts.
    """

    DISCOUNT_TYPE_CHOICES = [
        ("percent", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    usage_limit = models.PositiveIntegerField(null=True, blank=True)      # total usage limit
    usage_limit_per_user = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid_now(self):
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_to
        )

    def __str__(self):
        return self.code


class CouponProductRestriction(models.Model):
    """
    Restrict coupon to specific products.
    """
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="product_restrictions")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.coupon.code} → {self.product.name}"


class CouponCategoryRestriction(models.Model):
    """
    Restrict coupon to specific categories.
    """
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="category_restrictions")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.coupon.code} → {self.category.name}"

class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="usages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey("order.Order", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.email} used {self.coupon.code}"