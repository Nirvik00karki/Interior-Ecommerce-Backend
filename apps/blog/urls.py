from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BlogCategoryViewSet, BlogPostViewSet

router = DefaultRouter()
router.register("categories", BlogCategoryViewSet)
router.register("posts", BlogPostViewSet)

urlpatterns = [
    # slug-based detail routes for customer-facing APIs
    path(
        "categories/<slug:slug>/",
        BlogCategoryViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="blogcategory-by-slug"
    ),
    path(
        "posts/<slug:slug>/",
        BlogPostViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="blogpost-by-slug"
    ),
] + router.urls
