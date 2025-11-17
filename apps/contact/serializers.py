from rest_framework import serializers
from .models import ContactSubmission

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ("id", "name", "email", "phone", "message", "is_read", "created_at")
        read_only_fields = ("is_read", "created_at")
