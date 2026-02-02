from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import Order
from .serializers import OrderSerializer

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class AdminOrderViewSet(viewsets.ModelViewSet):
    """
    Admin-only Order Management:
    - Full read access
    - Update order status
    - Filter by status/date/user
    """

    queryset = Order.objects.select_related(
        "user", "shipping_address"
    ).prefetch_related("items__variant")

    serializer_class = OrderSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__email", "shipping_address__full_name", "id"]
    ordering_fields = ["created_at", "status", "total"]

    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["processing", "shipped", "completed", "cancelled", "refunded"]:
            return Response({"error": "Invalid status"}, status=400)

        order.status = new_status
        order.save()
        return Response({"message": f"Order updated to {new_status}"})

    @action(detail=True, methods=["post"])
    def mark_shipped(self, request, pk=None):
        order = self.get_object()

        if order.status not in ["processing"]:
            return Response({"error": "Order must be processing to ship"}, status=400)

        order.status = "shipped"
        order.save()

        return Response({"message": "Order marked as shipped"})

    @action(detail=True, methods=["post"])
    def mark_completed(self, request, pk=None):
        order = self.get_object()

        if order.status not in ["shipped"]:
            return Response({"error": "Only shipped orders can be completed"}, status=400)

        order.status = "completed"
        order.commit_stock()
        order.save()

        return Response({"message": "Order marked as completed"})

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def refund(self, request, pk=None):
        order = self.get_object()

        if order.status not in ["completed", "shipped"]:
            return Response({"error": "Only shipped or completed orders can be refunded"}, status=400)

        # Restore inventory for all items with locking
        for item in order.items.all():
            from apps.catalog.models import Inventory
            inv = Inventory.objects.select_for_update().get(variant=item.variant)
            inv.stock += item.quantity
            inv.save()

        order.status = "refunded"
        order.save()

        return Response({"message": "Order refunded and inventory restored"})
