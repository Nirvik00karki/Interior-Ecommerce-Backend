from rest_framework import serializers
from .models import Page, HeroSlide, Methodology, FAQ

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"

class HeroSlideSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroSlide
        fields = ("id", "title", "sub_title", "image_url", "video_url", "link", "order", "is_published")

    def get_image_url(self, obj):
        return getattr(obj.image, "url", None)

class MethodologySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Methodology
        fields = ("id", "title", "description", "image_url", "order")

    def get_image_url(self, obj):
        return getattr(obj.image_or_icon, "url", None)

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("id", "question", "answer", "order")
