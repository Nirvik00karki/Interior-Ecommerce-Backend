from rest_framework import serializers
from .models import Review
from apps.accounts.models import User

class UserSummarySerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "full_name", "email"]

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id", "user", "product", "rating", "comment", 
            "image", "image_url", "is_active", "created_at"
        ]
        read_only_fields = ["is_active", "created_at"]

    def get_image_url(self, obj):
        return getattr(obj.image, "url", None)

    def create(self, validated_data):
        from apps.order.models import Order, OrderItem
        
        user = self.context["request"].user
        product = validated_data["product"]
        
        # Check if already reviewed
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        
        # Check if user has purchased this product
        has_purchased = OrderItem.objects.filter(
            order__user=user,
            order__status__in=["delivered", "completed"],
            variant__product=product
        ).exists()
        
        if not has_purchased:
            raise serializers.ValidationError(
                "You can only review products you have purchased and received."
            )
        
        return Review.objects.create(user=user, **validated_data)
