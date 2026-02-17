from django.db import models
from django.conf import settings
from apps.accounts.models import ShippingAddress
from apps.catalog.models import ProductVariant
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.catalog.models import Inventory
from apps.coupons.models import Coupon

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders"
    )

    shipping_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @transaction.atomic
    def reserve_stock(self):
        """
        Reserve stock with database-level locking.
        Prevents race conditions under heavy traffic.
        """
        for item in self.items.all():

            # Lock the inventory row!
            inventory = (
                Inventory.objects
                .select_for_update()         # <-- database-level row lock
                .get(variant=item.variant)
            )

            if inventory.available_stock < item.quantity:
                raise ValidationError(
                    f"Insufficient stock for {item.variant.sku}"
                )

            # Reserve the stock
            inventory.reserved_stock += item.quantity
            inventory.save()

    @transaction.atomic
    def release_stock(self):
        """Release reserved stock (e.g., on cancellation or expiration)"""
        for item in self.items.all():
            inventory = (
                Inventory.objects
                .select_for_update()
                .get(variant=item.variant)
            )

            inventory.reserved_stock -= item.quantity
            if inventory.reserved_stock < 0:
                inventory.reserved_stock = 0
            inventory.save()

    @transaction.atomic
    def commit_stock(self):
        """
        Move reserved stock into actual sold stock.
        Should be triggered when payment succeeds.
        """
        # Idempotency check - prevent double deduction
        if self.status == 'completed':
            return
        
        for item in self.items.all():
            inventory = (
                Inventory.objects
                .select_for_update()
                .get(variant=item.variant)
            )

            # Verify we have enough reserved stock
            if inventory.reserved_stock < item.quantity:
                raise ValidationError(
                    f"Reserved stock mismatch for {item.variant.sku}"
                )

            inventory.reserved_stock -= item.quantity
            inventory.stock -= item.quantity
            inventory.save()

    @transaction.atomic
    def restore_stock(self):
        """
        Return committed stock back to inventory (e.g., on refund).
        """
        # Idempotency check - if already refunded, don't restore again
        # However, status update happens AFTER this call in the view usually.
        # So we trust the view logic to only call this once.
        
        for item in self.items.all():
            inventory = (
                Inventory.objects
                .select_for_update()
                .get(variant=item.variant)
            )

            inventory.stock += item.quantity
            inventory.save()



    def __str__(self):
        return f"Order {self.id} - {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_items"
    )

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # final price snapshot

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.variant.sku} x {self.quantity}"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cod", "Cash on Delivery"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
