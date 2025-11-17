from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ProjectViewSet

router = DefaultRouter()
router.register("services", ServiceViewSet)
router.register("projects", ProjectViewSet)

urlpatterns = router.urls
