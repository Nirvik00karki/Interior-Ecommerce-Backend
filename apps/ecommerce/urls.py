from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register("product-categories", ProductCategoryViewSet)
router.register("products", ProductViewSet)

urlpatterns = router.urls
