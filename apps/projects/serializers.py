from rest_framework import serializers
from .models import (
    Sector,
    Service,
    Project,
    ProjectGalleryImage,
    ProjectServiceLink,
    Package,
    PackageItem
)


# Simple nested serializers for read-only display
class SectorNestedSerializer(serializers.ModelSerializer):
    """Lightweight serializer for nested sector display"""
    class Meta:
        model = Sector
        fields = ["id", "name", "slug"]

class ServiceNestedSerializer(serializers.ModelSerializer):
    """Lightweight serializer for nested service display"""
    class Meta:
        model = Service
        fields = ["id", "name", "slug"]

class ServiceSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        required=False,
        allow_null=True
    )
    cover_image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    cover_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Service
        fields = ("id", "name", "slug", "description",
                  "cover_image", "cover_image_url", "parent", "type", "is_ksp")

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

class ProjectGalleryImageNestedSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProjectGalleryImage
        fields = ["id", "image", "image_url"]

    def get_image_url(self, obj):
        return getattr(obj.image, "url", None)

class ProjectGalleryImageSerializer(ProjectGalleryImageNestedSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta(ProjectGalleryImageNestedSerializer.Meta):
        fields = ProjectGalleryImageNestedSerializer.Meta.fields + ["project"]

class ProjectSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    cover_image_url = serializers.SerializerMethodField()

    sector = serializers.PrimaryKeyRelatedField(
        queryset=Sector.objects.all(),
        required=False,
        allow_null=True
    )

    services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        many=True,
        required=False
    )

    gallery_images = ProjectGalleryImageNestedSerializer(
        many=True, required=False
    )

    class Meta:
        model = Project
        fields = [
            "id", "title", "slug", "description",
            "cover_image", "cover_image_url",
            "location", "date_completed",
            "status", "is_featured",
            "sector", "services",
            "gallery_images",
        ]

    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)

    def create(self, validated_data):
        services = validated_data.pop("services", [])
        gallery_data = validated_data.pop("gallery_images", [])
        cover_image = validated_data.pop("cover_image", None)

        project = Project.objects.create(**validated_data)

        if cover_image:
            project.cover_image = cover_image
            project.save()

        for service in services:
            ProjectServiceLink.objects.create(
                project=project, service=service
            )

        for image_data in gallery_data:
            ProjectGalleryImage.objects.create(
                project=project,
                image=image_data["image"]
            )

        return project

    def update(self, instance, validated_data):
        services = validated_data.pop("services", None)
        gallery_data = validated_data.pop("gallery_images", None)
        cover_image = validated_data.pop("cover_image", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cover_image:
            instance.cover_image = cover_image

        instance.save()

        if services is not None:
            instance.services.clear()
            for service in services:
                ProjectServiceLink.objects.create(
                    project=instance, service=service
                )

        if gallery_data is not None:
            instance.gallery_images.all().delete()
            for image_data in gallery_data:
                ProjectGalleryImage.objects.create(
                    project=instance,
                    image=image_data["image"]
                )

        return instance

class ProjectDetailSerializer(ProjectSerializer):
    """
    Extended Project serializer for detail views.
    Returns nested objects for sector and services instead of just IDs.
    """
    sector = SectorNestedSerializer(read_only=True)
    services = ServiceNestedSerializer(many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields

class SectorSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(write_only=True, required=False)
    icon = serializers.ImageField(write_only=True, required=False)

    cover_image_url = serializers.SerializerMethodField()
    icon_url = serializers.SerializerMethodField()

    class Meta:
        model = Sector
        fields = [
            "id", "name", "slug", "description",
            "cover_image", "cover_image_url",
            "icon", "icon_url",
        ]

    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)

    def get_icon_url(self, obj):
        return getattr(obj.icon, "url", None)
    def create(self, validated_data):
        cover_image = validated_data.pop("cover_image", None)
        icon = validated_data.pop("icon", None)

        sector = Sector.objects.create(**validated_data)

        if cover_image:
            sector.cover_image = cover_image
        if icon:
            sector.icon = icon
        if cover_image or icon:
            sector.save()

        return sector
    def update(self, instance, validated_data):
        cover_image = validated_data.pop("cover_image", None)
        icon = validated_data.pop("icon", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cover_image:
            instance.cover_image = cover_image
        if icon:
            instance.icon = icon

        instance.save()

        return instance
    
class PackageItemNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageItem
        fields = ["id", "product_id"]

class PackageItemSerializer(PackageItemNestedSerializer):
    package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all())

    class Meta(PackageItemNestedSerializer.Meta):
        fields = PackageItemNestedSerializer.Meta.fields + ["package"]

class PackageSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    cover_image_url = serializers.SerializerMethodField()

    items = PackageItemNestedSerializer(many=True, required=False)

    class Meta:
        model = Package
        fields = [
            "id", "name", "slug",
            "cover_image", "cover_image_url",
            "project_design_time",
            "project_manufacture_time",
            "project_installation_time",
            "basic_price", "premium_price",
            "support_service",
            "is_published",
            "items",
        ]

    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)

    def create(self, validated_data):
        items = validated_data.pop("items", [])
        cover_image = validated_data.pop("cover_image", None)

        package = Package.objects.create(**validated_data)

        if cover_image:
            package.cover_image = cover_image
            package.save()

        for item in items:
            PackageItem.objects.create(package=package, **item)

        return package

    def update(self, instance, validated_data):
        items = validated_data.pop("items", None)
        cover_image = validated_data.pop("cover_image", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cover_image:
            instance.cover_image = cover_image

        instance.save()

        if items is not None:
            instance.items.all().delete()
            for item in items:
                PackageItem.objects.create(package=instance, **item)

        return instance

