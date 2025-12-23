from rest_framework import viewsets, permissions
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

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
    lookup_field = "id"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "parent",
        "type",
        "is_ksp",
    ]

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "id"


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
    lookup_field = "id"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "sector",
        "services",
        "status",
        "is_featured",
    ]

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
    lookup_field = "id"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "is_published",
    ]

class PackageItemViewSet(viewsets.ModelViewSet):
    queryset = PackageItem.objects.select_related("package")
    serializer_class = PackageItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["package"]

