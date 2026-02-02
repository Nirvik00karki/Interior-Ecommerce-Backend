from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Order)
def clear_cart_on_order(sender, instance, created, **kwargs):
    """
    Clear user's cart automatically after successful order creation.
    This prevents stale cart data and improves user experience.
    """
    if created and instance.status == "pending":
        # Clear user's cart after successful order
        if hasattr(instance.user, "cart"):
            instance.user.cart.items.all().delete()
