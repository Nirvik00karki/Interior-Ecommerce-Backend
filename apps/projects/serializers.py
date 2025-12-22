from rest_framework import serializers
from apps.company.serializers import TeamMemberSerializer
from apps.company.models import TeamMember
from .models import (
    Sector,
    Service,
    ServiceList,
    Project,
    ProjectGalleryImage
)

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

class ProjectGalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProjectGalleryImage
        fields = ["id", "image", "image_url"]

    def get_image_url(self, obj):
        return getattr(obj.image, "url", None)

class ProjectSerializer(serializers.ModelSerializer):
    gallery_images = ProjectGalleryImageSerializer(many=True, required=False)

    cover_image = serializers.ImageField(write_only=True)
    cover_image_url = serializers.SerializerMethodField(read_only=True)

    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    service_list = serializers.PrimaryKeyRelatedField(
        queryset=ServiceList.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "cover_image",
            "cover_image_url",
            "location",
            "date_completed",
            "status",
            "is_featured",
            "sector",
            "service",
            "service_list",
            "gallery_images",
        ]
    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)

    def create(self, validated_data):
        gallery_data = validated_data.pop("gallery_images", [])
        cover_image = validated_data.pop("cover_image", None)

        project = Project.objects.create(**validated_data)

        if cover_image:
            project.cover_image = cover_image
            project.save()

        for image_data in gallery_data:
            ProjectGalleryImage.objects.create(
                project=project,
                image=image_data["image"]
            )

        return project

    def update(self, instance, validated_data):
        gallery_data = validated_data.pop("gallery_images", [])
        cover_image = validated_data.pop("cover_image", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cover_image:
            instance.cover_image = cover_image

        instance.save()

        if gallery_data:
            instance.gallery_images.all().delete()
            for image_data in gallery_data:
                ProjectGalleryImage.objects.create(
                    project=instance,
                    image=image_data["image"]
                )

        return instance


class SectorSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()
    icon_url = serializers.SerializerMethodField()

    class Meta:
        model = Sector
        fields = ["id", "name", "slug", "description", "cover_image_url", "icon_url"]

    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)

    def get_icon_url(self, obj):
        return getattr(obj.icon, "url", None)

class ServiceListSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = ServiceList
        fields = ["id", "name", "slug", "service", "cover_image_url"]

    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)
