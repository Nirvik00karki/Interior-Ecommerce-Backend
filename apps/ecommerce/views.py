from rest_framework import viewsets, permissions
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db import transaction

from .models import ProductCategory, Product
from .serializers import ProductCategorySerializer, ProductSerializer

CACHE_TIME = 300


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    # Public read, authenticated write
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@method_decorator(cache_page(CACHE_TIME), name="list")
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").order_by("id")
    serializer_class = ProductSerializer
    # Public read, authenticated write
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()
