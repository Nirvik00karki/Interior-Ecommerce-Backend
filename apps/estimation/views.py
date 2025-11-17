from rest_framework import viewsets, permissions
from .models import EstimationCategory
from .serializers import EstimationCategorySerializer


class EstimationCategoryViewSet(viewsets.ModelViewSet):
    queryset = EstimationCategory.objects.all().order_by("id")
    serializer_class = EstimationCategorySerializer
    # Categories are public to read, protected for create/update/delete
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
