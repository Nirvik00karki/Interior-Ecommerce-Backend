# coupons/serializers.py

from rest_framework import serializers
from .models import (
    Coupon,
    CouponProductRestriction,
    CouponCategoryRestriction,
    CouponUsage,
)
from apps.catalog.models import Product, Category


class CouponProductRestrictionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = CouponProductRestriction
        fields = ["id", "product", "product_name"]


class CouponCategoryRestrictionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = CouponCategoryRestriction
        fields = ["id", "category", "category_name"]


class CouponSerializer(serializers.ModelSerializer):
    """
    Main Coupon serializer with nested restrictions.
    """

    product_restrictions = CouponProductRestrictionSerializer(many=True, read_only=True)
    category_restrictions = CouponCategoryRestrictionSerializer(many=True, read_only=True)

    class Meta:
        model = Coupon
        fields = [
            "id",
            "code",
            "description",
            "discount_type",
            "discount_value",
            "min_purchase_amount",
            "valid_from",
            "valid_until",
            "usage_limit",
            "usage_limit_per_user",
            "is_active",
            "product_restrictions",
            "category_restrictions",
            "created_at",
        ]


class CouponCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Separate serializer for creating/updating coupons properly.
    Allows posting arrays of restriction IDs.
    """

    product_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    category_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    class Meta:
        model = Coupon
        fields = [
            "code",
            "description",
            "discount_type",
            "discount_value",
            "min_purchase_amount",
            "valid_from",
            "valid_until",
            "usage_limit",
            "usage_limit_per_user",
            "is_active",
            "product_ids",
            "category_ids",
        ]

    def create(self, validated_data):
        product_ids = validated_data.pop("product_ids", [])
        category_ids = validated_data.pop("category_ids", [])

        coupon = Coupon.objects.create(**validated_data)

        # Add product restrictions
        for pid in product_ids:
            CouponProductRestriction.objects.create(coupon=coupon, product_id=pid)

        # Add category restrictions
        for cid in category_ids:
            CouponCategoryRestriction.objects.create(coupon=coupon, category_id=cid)

        return coupon

    def update(self, coupon, validated_data):
        product_ids = validated_data.pop("product_ids", None)
        category_ids = validated_data.pop("category_ids", None)

        # update simple fields
        for attr, value in validated_data.items():
            setattr(coupon, attr, value)
        coupon.save()

        # replace product restrictions
        if product_ids is not None:
            coupon.product_restrictions.all().delete()
            for pid in product_ids:
                CouponProductRestriction.objects.create(coupon=coupon, product_id=pid)

        # replace category restrictions
        if category_ids is not None:
            coupon.category_restrictions.all().delete()
            for cid in category_ids:
                CouponCategoryRestriction.objects.create(coupon=coupon, category_id=cid)

        return coupon

class CouponUsageSerializer(serializers.ModelSerializer):
    coupon_code = serializers.CharField(source="coupon.code", read_only=True)

    class Meta:
        model = CouponUsage
        fields = ["id", "coupon", "coupon_code", "user", "used_at"]

