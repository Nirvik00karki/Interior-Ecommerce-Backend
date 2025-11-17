from rest_framework import viewsets, permissions
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Service, Project
from .serializers import ServiceSerializer, ProjectSerializer

CACHE_TIME = 60 * 5


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by("id")
    serializer_class = ServiceSerializer
    # Services listing is public; creating/updating requires authentication
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related("service").prefetch_related("team").order_by("-date_completed")
    serializer_class = ProjectSerializer
    # Projects are public to read; write operations require authentication
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()
