from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from .views import BlogCategoryViewSet, BlogPostViewSet

router = DefaultRouter()
router.register("categories", BlogCategoryViewSet)
router.register("posts", BlogPostViewSet)

urlpatterns = [
    # slug-based detail routes for customer-facing APIs (only match non-numeric slugs)
    re_path(
        r"^categories/(?P<slug>(?!\d+$)[\w-]+)/$",
        BlogCategoryViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="blogcategory-by-slug"
    ),
    re_path(
        r"^posts/(?P<slug>(?!\d+$)[\w-]+)/$",
        BlogPostViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="blogpost-by-slug"
    ),
] + router.urls
