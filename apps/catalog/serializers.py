# catalog/serializers.py

from rest_framework import serializers
from .models import (
    Category, Product, ProductImage,
    Attribute, AttributeValue,
    ProductVariant, ProductVariantAttribute, Inventory
)


# ---------------------------------------------------------
# ATTRIBUTE SERIALIZERS
# ---------------------------------------------------------
class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ["id", "value"]


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ["id", "name", "values"]


# ---------------------------------------------------------
# PRODUCT IMAGE SERIALIZER
# ---------------------------------------------------------
class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image", "image_url", "alt_text", "is_featured"]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


# ---------------------------------------------------------
# VARIANT ATTRIBUTE SERIALIZER
# ---------------------------------------------------------
class ProductVariantAttributeSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source="attribute.name", read_only=True)
    value_display = serializers.CharField(source="value.value", read_only=True)

    class Meta:
        model = ProductVariantAttribute
        fields = ["attribute", "attribute_name", "value", "value_display"]


# ---------------------------------------------------------
# PRODUCT VARIANT SERIALIZER
# ---------------------------------------------------------
class ProductVariantSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    attributes = ProductVariantAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id", "sku", "name", "price", "compare_at_price", "stock",
            "image", "image_url", "is_active", "attributes"
        ]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


# ---------------------------------------------------------
# PRODUCT SERIALIZER
# ---------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()

    main_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description",
            "main_image", "main_image_url",
            "min_price", "max_price",
            "category", "images", "variants",
            "is_active"
        ]

    def get_main_image_url(self, obj):
        return obj.main_image.url if obj.main_image else None

    def get_min_price(self, obj):
        variant = obj.variants.order_by("price").first()
        return variant.price if variant else None

    def get_max_price(self, obj):
        variant = obj.variants.order_by("-price").first()
        return variant.price if variant else None


# ---------------------------------------------------------
# CATEGORY SERIALIZER
# ---------------------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id", "name", "slug", "description", "image", "image_url", "is_active"
        ]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

# ---------------------------------------------------------
# INVENTORY SERIALIZER
# ---------------------------------------------------------
class InventorySerializer(serializers.ModelSerializer):
    variant_sku = serializers.CharField(source="variant.sku", read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "variant",
            "variant_sku",
            "quantity",
            "low_stock_threshold",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]
