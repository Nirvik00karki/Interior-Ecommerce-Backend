from rest_framework import serializers
from .models import EstimationCategory

class EstimationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimationCategory
        fields = ("id", "name")
