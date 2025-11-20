from rest_framework.routers import DefaultRouter
from .admin_views import AdminOrderViewSet

router = DefaultRouter()
router.register("orders", AdminOrderViewSet, basename="admin-orders")

urlpatterns = router.urls
