from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import ShippingAddress, ShippingZone

User = get_user_model()

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "full_name",
            "phone",
            "address_line1",
            "address_line2",
            "is_default",
            "label",
            "zone",
            "state",
            "country",
        ]
        read_only_fields = ("is_default",)

class ShippingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingZone
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    full_name = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()
    default_address = serializers.SerializerMethodField()
    address = ShippingAddressSerializer(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "full_name","phone",
            "password", "google_id", "avatar", "is_staff", "profile_picture", "profile_picture_url",
            "default_address", "address"
        ]
        read_only_fields = ("is_staff", "google_id", "avatar", "profile_picture_url")

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return email
    
    def get_default_address(self, obj):
        address = obj.shipping_addresses.filter(is_default=True).first()
        return ShippingAddressSerializer(address).data if address else None

    def create(self, validated_data):
        password = validated_data.pop("password")
        profile_picture = validated_data.pop("profile_picture", None)
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
        return user
    
    def update(self, instance, validated_data):
        # Pop ALL nested/special fields FIRST before calling super().update()
        password = validated_data.pop("password", None)
        profile_picture = validated_data.pop("profile_picture", None)
        address_data = validated_data.pop("address", None)
        
        # Now update the user with remaining fields
        user = super().update(instance, validated_data)
        
        # Handle address update/creation
        if address_data:
            address = instance.shipping_addresses.filter(is_default=True).first()
            if address:
                # Update existing default address
                for attr, value in address_data.items():
                    setattr(address, attr, value)
                address.save()
            else:
                # Create new default address if none exists
                ShippingAddress.objects.create(
                    user=instance,
                    is_default=True,
                    **address_data
                )
        
        # Handle password and profile picture (batch updates)
        needs_save = False
        if password:
            user.set_password(password)
            needs_save = True
        if profile_picture:
            user.profile_picture = profile_picture
            needs_save = True
        
        if needs_save:
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

class AdminCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password", "is_superuser", "is_staff"]
        read_only_fields = ["is_superuser", "is_staff"]

    def validate(self, data):
        request_user = self.context["request"].user
        if not request_user.is_staff:
            raise serializers.ValidationError("Only admin users can create staff accounts.")
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create(
            **validated_data,
            is_staff=True,
            is_superuser=False,
            is_active=True,
        )
        user.set_password(password)
        user.save()
        return user
