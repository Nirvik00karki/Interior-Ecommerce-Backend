from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import ShippingAddress, ShippingZone

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    full_name = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "full_name",
            "password", "google_id", "avatar", "is_staff", "profile_picture", "profile_picture_url",
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
        password = validated_data.pop("password", None)
        profile_picture = validated_data.pop("profile_picture", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        if profile_picture:
            user.profile_picture = profile_picture
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
