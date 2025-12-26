from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BlogCategoryViewSet, BlogPostViewSet

router = DefaultRouter()
router.register("categories", BlogCategoryViewSet)
router.register("posts", BlogPostViewSet)

urlpatterns = [
    # slug-based detail routes for customer-facing APIs (use the action on the viewset)
    path(
        "categories/slug/<slug:slug>/",
        BlogCategoryViewSet.as_view({"get": "retrieve_by_slug"}),
        name="blogcategory-by-slug"
    ),
    path(
        "posts/slug/<slug:slug>/",
        BlogPostViewSet.as_view({"get": "retrieve_by_slug"}),
        name="blogpost-by-slug"
    ),
] + router.urls
