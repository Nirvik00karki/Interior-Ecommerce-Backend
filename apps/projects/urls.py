from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    SectorViewSet,
    ServiceViewSet,
    ProjectViewSet,
    ProjectGalleryImageViewSet,
    PackageViewSet,
    PackageItemViewSet,
)

router = DefaultRouter()
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

urlpatterns = [
    # slug-based detail routes for customer-facing APIs
    path(
        "sectors/<slug:slug>/",
        SectorViewSet.as_view({"get": "retrieve"}),
        name="sector-by-slug"
    ),
    path(
        "services/<slug:slug>/",
        ServiceViewSet.as_view({"get": "retrieve"}),
        name="service-by-slug"
    ),
    path(
        "projects/<slug:slug>/",
        ProjectViewSet.as_view({"get": "retrieve"}),
        name="project-by-slug"
    ),
    path(
        "packages/<slug:slug>/",
        PackageViewSet.as_view({"get": "retrieve"}),
        name="package-by-slug"
    ),
] + router.urls
