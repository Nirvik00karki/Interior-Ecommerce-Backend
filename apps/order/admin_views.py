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
    @transaction.atomic
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")
        old_status = order.status

        # Define statuses that imply stock commitment
        sold_statuses = ["paid", "processing", "shipped", "delivered", "completed"]

        if new_status not in ["pending", "paid", "processing", "shipped", "delivered", "completed", "cancelled", "refunded"]:
            return Response({"error": "Invalid status"}, status=400)

        # Handle stock transitions
        try:
            # 1. Commit Stock: pending -> paid/processing/etc.
            if new_status in sold_statuses and old_status == "pending":
                order.commit_stock()
            
            # 2. Restore Stock: paid/processing/etc. -> refunded/cancelled
            elif (new_status in ["refunded", "cancelled"]) and (old_status in sold_statuses):
                order.restore_stock()

            # 3. Release Stock: pending -> cancelled
            elif new_status == "cancelled" and old_status == "pending":
                order.release_stock()
        except Exception as e:
            return Response({"error": str(e)}, status=400)

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
        # Note: commit_stock might have already been called when status moved to 'paid' or 'processing'
        # but commit_stock should ideally be idempotent if we add the check.
        # However, for consistency with OrderViewSet, we'll let the logic above handle it.
        order.save()

        return Response({"message": "Order marked as completed"})

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def refund(self, request, pk=None):
        order = self.get_object()

        if order.status not in ["completed", "shipped", "delivered", "paid", "processing"]:
            return Response({"error": "Only paid or shipped orders can be refunded"}, status=400)

        # Restore inventory using centralized method
        try:
            order.restore_stock()
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        order.status = "refunded"
        order.save()

        return Response({"message": "Order refunded and inventory restored"})

