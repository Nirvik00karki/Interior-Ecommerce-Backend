from datetime import date
from django.utils import timezone
from apps.coupons.models import Coupon
from rest_framework.exceptions import ValidationError

class CouponService:

    @staticmethod
    def validate_coupon(user, code: str, order_total: float):
        """
        Validates and returns the valid Coupon object.
        Raises ValidationError if invalid.
        """

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            raise ValidationError("Invalid coupon code.")

        # Check active
        if not coupon.is_active:
            raise ValidationError("This coupon is no longer active.")

        # Check expiration
        if not (coupon.valid_from <= timezone.now() <= coupon.valid_to):
            raise ValidationError("This coupon is not valid today.")

        # Check minimum order amount
        if coupon.min_purchase_amount and order_total < coupon.min_purchase_amount:
            raise ValidationError(
                f"Order total must be at least {coupon.min_purchase_amount} to use this coupon."
            )

        # Per-user usage limit
        if coupon.usage_limit_per_user:
            used_count = coupon.usages.filter(user=user).count()
            if used_count >= coupon.usage_limit_per_user:
                raise ValidationError("You have already used this coupon.")

        # Global usage limit
        if coupon.usage_limit:
            if coupon.usages.count() >= coupon.usage_limit:
                raise ValidationError("This coupon has reached its maximum usage.")

        return coupon

    @staticmethod
    def apply_discount(coupon: Coupon, order_total: float):
        """
        Returns the discounted price based on coupon type.
        """

        if coupon.discount_type == "percent":
            discount = (order_total * coupon.discount_value) / 100
        else:
            discount = coupon.discount_value

        # Prevent negative totals
        discounted_total = max(order_total - discount, 0)

        return discounted_total, discount
