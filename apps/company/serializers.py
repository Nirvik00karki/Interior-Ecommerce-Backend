from rest_framework import serializers
from .models import Office, TeamMember, Award, Partner, Testimonial, SocialMedia    
from apps.accounts.serializers import UserSerializer  # if need author linkage anywhere
from cloudinary.models import CloudinaryField

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"

class TeamMemberSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(write_only=True, required=False, allow_null=True)
    profile_picture_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TeamMember
        fields = (
            "id", "name", "designation", "bio", "social_links",
            "office", "order",
            "profile_picture", "profile_picture_url",
        )

    def get_profile_picture_url(self, obj):
        return getattr(obj.profile_picture, "url", None)

    def create(self, validated_data):
        image = validated_data.pop("profile_picture", None)
        instance = super().create(validated_data)
        if image:
            instance.profile_picture = image
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop("profile_picture", None)
        instance = super().update(instance, validated_data)
        if image:
            instance.profile_picture = image
            instance.save()
        return instance


class AwardSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Award
        fields = ("id", "title", "description", "date_received", "image", "image_url")

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

class PartnerSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(write_only=True, required=False, allow_null=True)
    logo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Partner
        fields = ("id", "name", "website_url", "logo", "logo_url")

    def get_logo_url(self, obj):
        return getattr(obj.logo, "url", None)

    def create(self, validated_data):
        logo = validated_data.pop("logo", None)
        instance = super().create(validated_data)
        if logo:
            instance.logo = logo
            instance.save()
        return instance

    def update(self, instance, validated_data):
        logo = validated_data.pop("logo", None)
        instance = super().update(instance, validated_data)
        if logo:
            instance.logo = logo
            instance.save()
        return instance

class TestimonialSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(write_only=True, required=False, allow_null=True)
    profile_picture_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Testimonial
        fields = ("id", "name", "designation", "message",
                  "profile_picture", "profile_picture_url")

    def get_profile_picture_url(self, obj):
        return getattr(obj.profile_picture, "url", None)

    def create(self, validated_data):
        image = validated_data.pop("profile_picture", None)
        instance = super().create(validated_data)
        if image:
            instance.profile_picture = image
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop("profile_picture", None)
        instance = super().update(instance, validated_data)
        if image:
            instance.profile_picture = image
            instance.save()
        return instance

class SocialMediaSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()

    class Meta:
        model = SocialMedia
        fields = ["id", "name", "icon", "icon_url", "link", "isActive"]

    def get_icon_url(self, obj):
        return getattr(obj.icon, "url", None)
