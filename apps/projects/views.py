from rest_framework import viewsets, permissions
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.accounts.permissions import IsAdminOrReadOnly

from .models import Service, Project, ProjectGalleryImage, Package, PackageItem
from .models import Sector
from .serializers import (SectorSerializer, ServiceSerializer, ProjectSerializer, 
                          ProjectGalleryImageSerializer, PackageSerializer, PackageItemSerializer)
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

CACHE_TIME = 60 * 5


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related("parent").all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "parent",
        "type",
        "is_ksp",
    ]

    @action(detail=False, methods=["get"], url_path="slug/(?P<slug>[^/.]+)")
    def retrieve_by_slug(self, request, slug=None):
        service = get_object_or_404(Service, slug=slug)
        serializer = self.get_serializer(service)
        return Response(serializer.data)

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=["get"], url_path="slug/(?P<slug>[^/.]+)")
    def retrieve_by_slug(self, request, slug=None):
        sector = get_object_or_404(Sector, slug=slug)
        serializer = self.get_serializer(sector)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = (
        Project.objects
        .select_related("sector")
        .prefetch_related(
            "services",
            "gallery_images"
        )
    )

    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]    

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "sector",
        "services",
        "status",
        "is_featured",
    ]

    @action(detail=False, methods=["get"], url_path="slug/(?P<slug>[^/.]+)")
    def retrieve_by_slug(self, request, slug=None):
        project = get_object_or_404(Project, slug=slug)
        serializer = self.get_serializer(project)
        return Response(serializer.data)

class ProjectGalleryImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectGalleryImage.objects.select_related("project")
    serializer_class = ProjectGalleryImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]
    
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.prefetch_related("items")
    serializer_class = PackageSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "is_published",
    ]

    @action(detail=False, methods=["get"], url_path="slug/(?P<slug>[^/.]+)")
    def retrieve_by_slug(self, request, slug=None):
        package = get_object_or_404(Package, slug=slug)
        serializer = self.get_serializer(package)
        return Response(serializer.data)

class PackageItemViewSet(viewsets.ModelViewSet):
    queryset = PackageItem.objects.select_related("package")
    serializer_class = PackageItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["package"]

