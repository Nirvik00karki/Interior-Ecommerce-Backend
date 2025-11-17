from rest_framework import serializers
from .models import ProductCategory, Product

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("id", "name", "slug")

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category_detail = ProductCategorySerializer(source="category", read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "category", "category_detail", "price", "description", "image_url")

    def get_image_url(self, obj):
        return getattr(obj.image, "url", None)
