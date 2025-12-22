from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ProjectViewSet

router = DefaultRouter()
from .views import (
    SectorViewSet,
    ServiceViewSet,
    ServiceListViewSet,
    ProjectViewSet,
    ProjectGalleryImageViewSet,
)

router.register(r"sectors", SectorViewSet, basename="sector")
router.register(r"services", ServiceViewSet, basename="service")
router.register(r"service-lists", ServiceListViewSet, basename="service-list")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(
    r"project-gallery-images",
    ProjectGalleryImageViewSet,
    basename="project-gallery-image"
)

urlpatterns = router.urls
