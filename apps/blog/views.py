from rest_framework import viewsets
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db import transaction

from .models import BlogCategory, BlogPost
from .serializers import BlogCategorySerializer, BlogPostSerializer

CACHE_TIME = 60 * 5


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


@method_decorator(cache_page(CACHE_TIME), name="list")
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.select_related("author", "blog_category").order_by("-date")
    serializer_class = BlogPostSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()
