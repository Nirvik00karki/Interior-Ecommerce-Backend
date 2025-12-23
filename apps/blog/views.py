from rest_framework import viewsets, permissions
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db import transaction

from .models import BlogCategory, BlogPost
from .serializers import BlogCategorySerializer, BlogPostSerializer
from rest_framework.parsers import MultiPartParser, FormParser

CACHE_TIME = 60 * 5


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    # Allow anyone to list/retrieve categories, require auth for create/update/delete
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"


@method_decorator(cache_page(CACHE_TIME), name="list")
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.select_related("blogpost_user", "blog_category").order_by("-date")
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "id"

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()
