from django.contrib import admin
from .models import (
    Coupon,
    CouponProductRestriction,
    CouponCategoryRestriction
)


class CouponProductRestrictionInline(admin.TabularInline):
    model = CouponProductRestriction
    extra = 1


class CouponCategoryRestrictionInline(admin.TabularInline):
    model = CouponCategoryRestriction
    extra = 1


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "discount_value",
        "is_active",
        "valid_from",
        "valid_to",
        "usage_limit",
    )
    list_filter = ("discount_type", "is_active")
    search_fields = ("code", "description")
    ordering = ("-valid_from",)

    readonly_fields = ("created_at",)

    inlines = [
        CouponProductRestrictionInline,
        CouponCategoryRestrictionInline,
    ]

    fieldsets = (
        ("Basic Info", {
            "fields": ("code", "description", "is_active")
        }),
        ("Discount Settings", {
            "fields": ("discount_type", "discount_value", "min_purchase_amount")
        }),
        ("Validity Period", {
            "fields": ("valid_from", "valid_until")
        }),
        ("Usage Limits", {
            "fields": ("usage_limit", "usage_limit_per_user")
        }),
        ("Metadata", {
            "fields": ("created_at",),
        }),
    )


# @admin.register(CouponUsage)
# class CouponUsageAdmin(admin.ModelAdmin):
#     list_display = ("coupon", "user", "used_at")
#     list_filter = ("coupon", "user")
#     search_fields = ("coupon__code", "user__email")
#     ordering = ("-used_at",)
