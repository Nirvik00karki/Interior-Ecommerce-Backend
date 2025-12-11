from rest_framework import serializers
from .models import BlogCategory, BlogPost
from apps.accounts.serializers import UserSerializer

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ("id", "name", "slug")

class BlogPostSerializer(serializers.ModelSerializer):
    blogpost_user = UserSerializer(read_only=True)
    cover_image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    cover_image_url = serializers.SerializerMethodField(read_only=True)
    blog_category_detail = BlogCategorySerializer(source="blog_category", read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            "id", "title", "slug",
            "cover_image", "cover_image_url",
            "excerpt", "content",
            "tags", "blogpost_user", "author",
            "is_published",
            "blog_category", "blog_category_detail",
            "date",
        )

    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)

    def create(self, validated_data):
        request = self.context.get("request")
        image = validated_data.pop("cover_image", None)

        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["blogpost_user"] = request.user

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
