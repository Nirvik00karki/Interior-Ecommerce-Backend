from rest_framework import serializers
from .models import Service, Project
from apps.company.serializers import TeamMemberSerializer
from apps.company.models import TeamMember

class ServiceSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    cover_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Service
        fields = ("id", "name", "slug", "description",
                  "cover_image", "cover_image_url")

    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)

    def create(self, validated_data):
        image = validated_data.pop("cover_image", None)
        instance = super().create(validated_data)
        if image:
            instance.cover_image = image
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop("cover_image", None)
        instance = super().update(instance, validated_data)
        if image:
            instance.cover_image = image
            instance.save()
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    cover_image_url = serializers.SerializerMethodField(read_only=True)

    team = TeamMemberSerializer(many=True, read_only=True)
    team_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=TeamMember.objects.all(), source="team"
    )

    gallery_images = serializers.ListField(
        child=serializers.URLField(), required=False
    )

    class Meta:
        model = Project
        fields = (
            "id", "title", "slug", "description",
            "cover_image", "cover_image_url",
            "gallery_images",
            "location", "date_completed", "status",
            "is_featured", "service",
            "team", "team_ids"
        )
        read_only_fields = ("team",)

    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)

    def create(self, validated_data):
        image = validated_data.pop("cover_image", None)
        instance = super().create(validated_data)
        if image:
            instance.cover_image = image
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop("cover_image", None)
        instance = super().update(instance, validated_data)
        if image:
            instance.cover_image = image
            instance.save()
        return instance
