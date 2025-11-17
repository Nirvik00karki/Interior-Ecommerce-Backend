from rest_framework import viewsets, permissions
from django.db import transaction

from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer


class ContactSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ContactSubmission.objects.all().order_by("-created_at")
    serializer_class = ContactSubmissionSerializer

    def get_permissions(self):
        """
        Allow anonymous users to create contact submissions (for frontend contact form).
        All other actions (list, retrieve, update, delete) require authentication.
        """
        if getattr(self, 'action', None) == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()
