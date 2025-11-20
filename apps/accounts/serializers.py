from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import ShippingAddress, ShippingZone

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "full_name",
            "password", "google_id", "avatar", "is_staff",
        ]
        read_only_fields = ("is_staff", "google_id", "avatar")

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return email

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Convert "username" to email for JWT
        attrs["username"] = email

        return super().validate(attrs)


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "full_name",
            "phone",
            "address_line1",
            "address_line2",
            "zone",
            "state",
            "postal_code",
            "country",
        ]

class ShippingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingZone
        fields = "__all__"