from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction

from apps.accounts.permissions import IsAdminOrReadOnly
from .models import Coupon, CouponUsage
from .serializers import (
    CouponSerializer,
    CouponCreateUpdateSerializer,
    CouponUsageSerializer,
)


class CouponViewSet(viewsets.ModelViewSet):
    """
    Admin: Full CRUD
    Customers: Read-only list & detail
    """
    queryset = Coupon.objects.all().order_by("-created_at")
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "code"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CouponCreateUpdateSerializer
        return CouponSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=400)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=400)

    def destroy(self, request, *args, **kwargs):
        coupon = self.get_object()

        # check usage before deletion
        if CouponUsage.objects.filter(coupon=coupon).exists():
            return Response(
                {"error": "Cannot delete coupon that has been used."},
                status=400
            )

        return super().destroy(request, *args, **kwargs)

class CouponUsageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin view for all coupon usage history.
    """
    queryset = CouponUsage.objects.select_related("coupon", "user").order_by("-used_at")
    serializer_class = CouponUsageSerializer
    permission_classes = [IsAdminOrReadOnly]
