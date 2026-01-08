from rest_framework import serializers
from .models import Cart, CartItem
from apps.catalog.serializers import ProductVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):
    variant_details = ProductVariantSerializer(source="variant", read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "variant", "variant_details", "quantity", "subtotal"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_price", "total_items", "updated_at"]
