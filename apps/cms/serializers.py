from rest_framework import serializers
from .models import Page, HeroSlide, Methodology, FAQ

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"

class HeroSlideSerializer(serializers.ModelSerializer):
    # Accept uploaded file from multipart/form-data. write_only so it's not repeated in JSON response.
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HeroSlide
        fields = (
            "id",
            "title",
            "sub_title",
            "image",
            "image_url",
            "video_url",
            "link",
            "order",
            "is_published",
        )

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
