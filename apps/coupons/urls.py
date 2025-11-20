from rest_framework.routers import DefaultRouter
from .views import CouponViewSet, CouponUsageViewSet

router = DefaultRouter()
router.register("coupons", CouponViewSet, basename="coupons")
router.register("coupon-usage", CouponUsageViewSet, basename="coupon_usage")

urlpatterns = router.urls
