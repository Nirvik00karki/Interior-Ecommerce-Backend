from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
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
    # slug-based detail routes for customer-facing APIs (only match non-numeric slugs)
    re_path(
        r"^sectors/(?P<slug>(?!\d+$)[\w-]+)/$",
        SectorViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="sector-by-slug"
    ),
    re_path(
        r"^services/(?P<slug>(?!\d+$)[\w-]+)/$",
        ServiceViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="service-by-slug"
    ),
    re_path(
        r"^projects/(?P<slug>(?!\d+$)[\w-]+)/$",
        ProjectViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="project-by-slug"
    ),
    re_path(
        r"^packages/(?P<slug>(?!\d+$)[\w-]+)/$",
        PackageViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="package-by-slug"
    ),
] + router.urls
