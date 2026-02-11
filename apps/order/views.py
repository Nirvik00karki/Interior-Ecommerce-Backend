from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

from .models import Order, Payment
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    PaymentSerializer,
)
from apps.accounts.models import ShippingAddress
from apps.accounts.serializers import ShippingAddressSerializer
from apps.catalog.services.coupon_service import CouponService
from .serializers import ApplyCouponSerializer, OrderStatusUpdateSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user

class OrderViewSet(viewsets.ModelViewSet):
    """
    Admin → Full access
    User → Only own orders
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        qs = Order.objects.select_related("shipping_address", "user").prefetch_related("items__variant")

        if self.request.user.is_staff:
            return qs.order_by("-created_at")

        return qs.filter(user=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        if self.action in ["create"]:
            return OrderCreateSerializer
        return OrderSerializer
    
    @action(detail=False, methods=["post"], url_path="apply-coupon")
    def apply_coupon(self, request):
        order_total = float(request.data.get("order_total", 0))

        serializer = ApplyCouponSerializer(
            data={"code": request.data.get("code")},
            context={"request": request, "order_total": order_total}
        )
        serializer.is_valid(raise_exception=True)

        coupon = serializer.validated_data["coupon"]
        discounted_total, discount_amount = CouponService.apply_discount(coupon, order_total)

        return Response({
            "valid": True,
            "coupon": coupon.code,
            "discount": discount_amount,
            "total_after_discount": discounted_total
        })

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = OrderCreateSerializer(
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)

            order = serializer.save()

            # Reserve stock
            try:
                order.reserve_stock()
            except Exception as e:
                # Let @transaction.atomic handle rollback
                return Response({"error": str(e)}, status=400)

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.status not in ["pending"]:
            return Response(
                {"error": "Only pending orders can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Release reserved stock
        order.release_stock()
        order.status = "cancelled"
        order.save()

        return Response({"message": "Order cancelled."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="update-status", permission_classes=[permissions.IsAdminUser])
    @transaction.atomic
    def update_status(self, request, pk=None):
        """
        Admin-only endpoint to update order status.
        Handles stock commitment for paid/processing/completed statuses.
        """
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_status = serializer.validated_data["status"]
        old_status = order.status

        # If status is changing to a "sold" status and it was "pending" (reserved)
        # then commit the stock.
        sold_statuses = ["paid", "processing", "shipped", "delivered", "completed"]
        
        if new_status in sold_statuses and old_status == "pending":
            try:
                order.commit_stock()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Special case: if moving from "paid/shipped/etc" back to "pending"
        # we would technically need to revert commit_stock -> reserve_stock
        # but for now, we'll keep it simple and focus on the forward flow.
        
        order.status = new_status
        order.save()

        # Sync payment status if order is marked as paid
        if new_status == "paid" and hasattr(order, "payment"):
            order.payment.status = "success"
            order.payment.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.select_related("order")
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]
