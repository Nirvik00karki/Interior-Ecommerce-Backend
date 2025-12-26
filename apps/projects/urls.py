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
    path(
        "sectors/slug/<slug:slug>/",
        SectorViewSet.as_view({"get": "retrieve_by_slug"}),
        name="sector-by-slug"
    ),
    path(
        "services/slug/<slug:slug>/",
        ServiceViewSet.as_view({"get": "retrieve_by_slug"}),
        name="service-by-slug"
    ),
    path(
        "projects/slug/<slug:slug>/",
        ProjectViewSet.as_view({"get": "retrieve_by_slug"}),
        name="project-by-slug"
    ),
    path(
        "packages/slug/<slug:slug>/",
        PackageViewSet.as_view({"get": "retrieve_by_slug"}),
        name="package-by-slug"
    ),
] + router.urls
