from rest_framework import viewsets
from django.db import transaction

from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer


class ContactSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ContactSubmission.objects.all().order_by("-created_at")
    serializer_class = ContactSubmissionSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()
