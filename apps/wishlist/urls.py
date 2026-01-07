from rest_framework.routers import DefaultRouter
from .views import WishlistViewSet

router = DefaultRouter()
router.register("items", WishlistViewSet, basename="wishlist-items")

urlpatterns = router.urls
