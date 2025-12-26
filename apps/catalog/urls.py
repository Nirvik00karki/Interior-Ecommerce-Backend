from rest_framework import routers
from django.urls import path, re_path
from .views import (
    CategoryViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ProductVariantViewSet,
    ProductVariantAttributeViewSet,
    InventoryViewSet,
)

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("product-images", ProductImageViewSet)
router.register("variants", ProductVariantViewSet)
router.register("attributes", ProductVariantAttributeViewSet)
router.register("inventory", InventoryViewSet)

urlpatterns = [
    # slug-based detail routes (only match non-numeric slugs to avoid conflicting with pk-based routes)
    re_path(
        r"^categories/(?P<slug>(?!\d+$)[\w-]+)/$",
        CategoryViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="category-by-slug"
    ),
    re_path(
        r"^products/(?P<slug>(?!\d+$)[\w-]+)/$",
        ProductViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="product-by-slug"
    ),
] + router.urls
