from rest_framework import serializers
from .models import BlogCategory, BlogPost
from apps.accounts.serializers import UserSerializer

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ("id", "name", "slug")

class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    blog_category_detail = BlogCategorySerializer(source="blog_category", read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            "id", "title", "slug", "cover_image_url", "excerpt", "content",
            "tags", "author", "is_published", "blog_category", "blog_category_detail", "date"
        )

    def get_cover_image_url(self, obj):
        return getattr(obj.cover_image, "url", None)

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)
