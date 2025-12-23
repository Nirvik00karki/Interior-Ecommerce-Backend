from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductImage, ProductVariant, ProductVariantAttribute, Inventory
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductVariantSerializer,
    ProductVariantAttributeSerializer,
    InventorySerializer,
)
from apps.accounts.permissions import IsAdminOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser

# -------------------
# Category ViewSet
# -------------------

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "slug"


# -------------------
# Product ViewSet
# -------------------

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related("category")
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


# -------------------
# Product Variant ViewSet
# -------------------

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all().select_related("product")
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product", "is_active"]


# -------------------
# Product Images ViewSet
# -------------------

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all().select_related("product")
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product"]


# -------------------
# Product Attributes ViewSet
# -------------------

class ProductVariantAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductVariantAttribute.objects.all()
    serializer_class = ProductVariantAttributeSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product", "variant"]
    
# -------------------
# Inventory ViewSet
# -------------------

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.select_related("variant", "variant__product")
    serializer_class = InventorySerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["variant__product", "variant"]
    search_fields = ["variant__sku"]
