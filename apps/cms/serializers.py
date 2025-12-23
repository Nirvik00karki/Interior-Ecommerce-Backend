from rest_framework import serializers
from .models import Page, HeroSlide, Methodology, FAQ

class PageSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(write_only=True, required=False)
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = [
            "id", "title", "slug",
            "content", "brief",
            "cover_image", "cover_image_url",
        ]

    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)


class HeroSlideSerializer(serializers.ModelSerializer):
    # Upload fields (write-only)
    image = serializers.ImageField(
        write_only=True,
        required=False,
        allow_null=True
    )

    video = serializers.FileField(
        write_only=True,
        required=False,
        allow_null=True
    )

    # Read-only URLs
    image_url = serializers.SerializerMethodField(read_only=True)
    video_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HeroSlide
        fields = (
            "id",
            "title",
            "sub_title",
            "image",
            "image_url",
            "video",
            "video_url",
            "link",
            "order",
            "is_published",
        )

    def get_image_url(self, obj):
        return getattr(obj.image, "url", None)

    def get_video_url(self, obj):
        return getattr(obj.video_url, "url", None)

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        video = validated_data.pop("video", None)
        instance = super().create(validated_data)
        if image:
            instance.image = image
        if video:
            instance.video_url = video
        if image or video:
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        video = validated_data.pop("video", None)
        instance = super().update(instance, validated_data)
        if image:
            instance.image = image
        if video:
            instance.video_url = video
        if image or video:
            instance.save()
        return instance
    
class MethodologySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Methodology
        fields = ("id", "title", "description", "image", "image_url", "order")

    def get_image_url(self, obj):
        return getattr(obj.image_or_icon, "url", None)

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        instance = super().create(validated_data)
        if image:
            instance.image_or_icon = image
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        instance = super().update(instance, validated_data)
        if image:
            instance.image_or_icon = image
            instance.save()
        return instance


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("id", "question", "answer", "order")
