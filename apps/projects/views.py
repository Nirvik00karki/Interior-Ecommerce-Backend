from rest_framework import viewsets, permissions
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from apps.accounts.permissions import IsAdminOrReadOnly

from .models import Service, Project, ProjectGalleryImage
from .models import ServiceList, Sector
from .serializers import ServiceListSerializer, SectorSerializer, ServiceSerializer, ProjectSerializer, ProjectGalleryImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

CACHE_TIME = 60 * 5


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "slug"

class ServiceListViewSet(viewsets.ModelViewSet):
    queryset = ServiceList.objects.select_related("service")
    serializer_class = ServiceListSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["service"]
    lookup_field = "slug"

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "slug"


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related(
        "sector", "service", "service_list"
    ).prefetch_related("gallery_images")

    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sector", "service", "status", "is_featured"]
    lookup_field = "slug"

class ProjectGalleryImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectGalleryImage.objects.select_related("project")
    serializer_class = ProjectGalleryImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]
