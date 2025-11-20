from rest_framework import routers
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

urlpatterns = router.urls
