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
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ["id", "image", "image_url", "alt_text", "is_featured"]

    def get_image_url(self, obj):
        return getattr(obj.image, "url", None)

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        instance = super().create(validated_data)
        if image:
            instance.image = image
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        instance = super().update(instance, validated_data)
        if image:
            instance.image = image
            instance.save()
        return instance

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
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    attributes = ProductVariantAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id", "sku", "name", "price", "compare_at_price", "stock",
            "image", "image_url", "is_active", "attributes"
        ]

    def get_image_url(self, obj):
        return getattr(obj.image, "url", None)

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        instance = super().create(validated_data)
        if image:
            instance.image = image
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        instance = super().update(instance, validated_data)
        if image:
            instance.image = image
            instance.save()
        return instance


# ---------------------------------------------------------
# PRODUCT SERIALIZER
# ---------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    # Accept file upload from multipart/form-data
    main_image = serializers.ImageField(write_only=True, required=False, allow_null=True)

    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()

    main_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "main_image",
            "main_image_url",
            "min_price",
            "max_price",
            "category",
            "images",
            "variants",
            "is_active",
        ]

    def get_main_image_url(self, obj):
        return getattr(obj.main_image, "url", None)

    def create(self, validated_data):
        image = validated_data.pop("main_image", None)
        instance = super().create(validated_data)
        if image:
            instance.main_image = image
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop("main_image", None)
        instance = super().update(instance, validated_data)
        if image:
            instance.main_image = image
            instance.save()
        return instance

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
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id", "name", "slug", "description",
            "image", "image_url",
            "is_active"
        ]

    def get_image_url(self, obj):
        return getattr(obj.image, "url", None)

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        instance = super().create(validated_data)
        if image:
            instance.image = image
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        instance = super().update(instance, validated_data)
        if image:
            instance.image = image
            instance.save()
        return instance

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
