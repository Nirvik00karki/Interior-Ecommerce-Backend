from rest_framework import serializers
from .models import Wishlist
from apps.catalog.serializers import ProductSerializer

class WishlistSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "product", "product_details", "created_at"]
        read_only_fields = ["created_at"]
