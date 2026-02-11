from rest_framework import serializers
from django.db import transaction
from apps.catalog.models import ProductVariant, Inventory
from .models import Order, OrderItem, ShippingAddress, Payment
from decimal import Decimal
from apps.accounts.serializers import ShippingAddressSerializer
from apps.catalog.services.coupon_service import CouponService
from apps.coupons.models import CouponUsage

class OrderItemSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source="variant.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "variant",
            "variant_name",
            "quantity",
            "price",
        ]

class OrderItemCreateSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        variant_id = attrs["variant_id"]
        quantity = attrs["quantity"]

        try:
            variant = ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError("Invalid variant.")

        # Check inventory - use OneToOne relationship
        try:
            inv = variant.inventory
        except Inventory.DoesNotExist:
            raise serializers.ValidationError("Inventory not found for this item.")
        
        if inv.available_stock < quantity:
            raise serializers.ValidationError("Not enough stock for this item.")

        attrs["variant"] = variant
        attrs["price"] = variant.price
        return attrs

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "subtotal",
            "shipping_cost",
            "discount_amount",
            "total",
            "coupon",
            "shipping_address",
            "items",
            "created_at",
        ]
        read_only_fields = ["user", "subtotal", "total"]

class OrderCreateSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField()
    items = OrderItemCreateSerializer(many=True)
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------
    def validate(self, data):
        request = self.context["request"]
        user = request.user

        # ------------------------------
        # 1. Validate shipping address
        # ------------------------------
        try:
            shipping_address = ShippingAddress.objects.select_related("zone").get(
                id=data["shipping_address_id"],
                user=user
            )
        except ShippingAddress.DoesNotExist:
            raise serializers.ValidationError("Invalid shipping address.")

        data["shipping_address"] = shipping_address

        # Determine shipping cost from zone
        if not shipping_address.zone:
            raise serializers.ValidationError("Shipping zone not set for this address.")

        data["shipping_cost"] = Decimal(str(shipping_address.zone.cost))

        # ------------------------------
        # 2. Validate and price cart items
        # ------------------------------
        subtotal = 0
        validated_items = []

        for item in data["items"]:
            variant_id = item["variant_id"]
            quantity = item["quantity"]

            # Lock inventory row
            try:
                variant = (
                    ProductVariant.objects
                    .select_related("product")
                    .select_for_update()
                    .get(id=variant_id)
                )
                # Lock inventory separately to avoid "FOR UPDATE cannot be applied to outer join" error
                inv = Inventory.objects.select_for_update().get(variant=variant)
            except Inventory.DoesNotExist:
                raise serializers.ValidationError(
                    f"Inventory not found for {variant.product.name} (Variant {variant_id})."
                )

            if inv.available_stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {variant.product.name} (Variant {variant_id})."
                )

            line_total = variant.price * quantity
            subtotal += line_total

            validated_items.append({
                "variant": variant,
                "quantity": quantity,
                "unit_price": variant.price,
                "line_total": line_total,
            })

        data["validated_items"] = validated_items
        data["subtotal"] = Decimal(str(subtotal))

        # ------------------------------
        # 3. Validate coupon if provided
        # ------------------------------
        coupon_code = data.get("coupon_code")
        if coupon_code:
            coupon = CouponService.validate_coupon(
                user=user,
                code=coupon_code,
                order_total=subtotal
            )
            data["coupon"] = coupon
        else:
            data["coupon"] = None

        return data

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------
    def create(self, validated_data):
        user = self.context["request"].user
        items_data = validated_data["validated_items"]
        shipping_address = validated_data["shipping_address"]
        coupon = validated_data["coupon"]
        subtotal = validated_data["subtotal"]
        shipping_cost = validated_data["shipping_cost"]

        # ------------------------------
        # Apply coupon (if exists)
        # ------------------------------
        if coupon:
            discounted_total, discount_amount = CouponService.apply_discount(
                coupon,
                subtotal
            )
        else:
            discounted_total = subtotal
            discount_amount = 0

        # ------------------------------
        # FINAL TOTAL = discounted subtotal + shipping cost
        # ------------------------------
        total = discounted_total + shipping_cost

        # ------------------------------
        # Create Order
        # ------------------------------
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            discount_amount=discount_amount,
            total=total,
            coupon=coupon,
            status="pending",
        )

        # ------------------------------
        # Create Order Items
        # ------------------------------
        items = [
            OrderItem(
                order=order,
                variant=item["variant"],
                quantity=item["quantity"],
                price=item["unit_price"],
            )
            for item in items_data
        ]
        OrderItem.objects.bulk_create(items)
        
        Payment.objects.create(
            order=order,
            method="cod",
            status="pending"
        )

        # ------------------------------
        # Track coupon usage
        # ------------------------------
        if coupon:
            CouponUsage.objects.create(
                coupon=coupon,
                user=user,
                order=order
            )

        return order

    # -------------------------------------------------
    # Output
    # -------------------------------------------------
    def to_representation(self, instance):
        return OrderSerializer(instance).data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "method",
            "status",
            "transaction_id",
            "paid_at",
            "created_at",
        ]

class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, data):
        user = self.context["request"].user
        order_total = self.context["order_total"]  # passed from View

        coupon = CouponService.validate_coupon(
            user=user,
            code=data["code"],
            order_total=order_total
        )

        data["coupon"] = coupon
        return data

class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
