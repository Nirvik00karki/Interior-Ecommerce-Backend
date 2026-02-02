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
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "image_url", "alt_text", "is_featured"]

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
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    attributes = ProductVariantAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id","product", "sku", "name", "price", "stock",
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
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

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
            "average_rating",
            "review_count",
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

    # Rating fields are now cached in model, no need to calculate
    def get_average_rating(self, obj):
        return float(obj.average_rating)

    def get_review_count(self, obj):
        return obj.review_count


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
    available_stock = serializers.IntegerField(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "variant",
            "variant_sku",
            "stock",
            "reserved_stock",
            "available_stock",
            "low_stock_threshold",
            "updated_at",
        ]
        read_only_fields = ["updated_at", "available_stock"]
