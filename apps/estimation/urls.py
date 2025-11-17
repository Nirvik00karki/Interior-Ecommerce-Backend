from rest_framework.routers import DefaultRouter
from .views import EstimationCategoryViewSet

router = DefaultRouter()
router.register("estimation-categories", EstimationCategoryViewSet)

urlpatterns = router.urls
