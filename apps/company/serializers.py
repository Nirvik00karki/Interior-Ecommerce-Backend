from rest_framework import serializers
from .models import Office, TeamMember, Award, Partner, Testimonial
from apps.accounts.serializers import UserSerializer  # if need author linkage anywhere
from cloudinary.models import CloudinaryField

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"

class TeamMemberSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = ("id", "name", "designation", "bio", "social_links", "office", "order", "profile_picture_url")

    def get_profile_picture_url(self, obj):
        return getattr(obj.profile_picture, "url", None)

class AwardSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Award
        fields = ("id", "title", "description", "date_received", "image_url")

    def get_image_url(self, obj):
        return getattr(obj.image, "url", None)

class PartnerSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = ("id", "name", "website_url", "logo_url")

    def get_logo_url(self, obj):
        return getattr(obj.logo, "url", None)

class TestimonialSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = ("id", "name", "designation", "message", "profile_picture_url")

    def get_profile_picture_url(self, obj):
        return getattr(obj.profile_picture, "url", None)
