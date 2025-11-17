from rest_framework import viewsets
from .models import EstimationCategory
from .serializers import EstimationCategorySerializer


class EstimationCategoryViewSet(viewsets.ModelViewSet):
    queryset = EstimationCategory.objects.all().order_by("id")
    serializer_class = EstimationCategorySerializer
