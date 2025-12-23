from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ProjectViewSet

router = DefaultRouter()
from .views import (
    SectorViewSet,
    ServiceViewSet,
    ProjectViewSet,
    ProjectGalleryImageViewSet,
    PackageViewSet,
    PackageItemViewSet,
)

router.register(r"sectors", SectorViewSet, basename="sector")
router.register(r"services", ServiceViewSet, basename="service")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(
    r"project-gallery-images",
    ProjectGalleryImageViewSet,
    basename="project-gallery-image"
)
router.register(r"packages", PackageViewSet, basename="package")
router.register(r"package-items", PackageItemViewSet, basename="package-item")

urlpatterns = router.urls
