from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductVariant, Inventory


@receiver(post_save, sender=ProductVariant)
def create_inventory_for_variant(sender, instance, created, **kwargs):
    """
    Automatically create Inventory record when ProductVariant is created.
    Ensures every variant has inventory tracking from the start.
    """
    if created:
        Inventory.objects.get_or_create(
            variant=instance,
            defaults={"stock": 10, "low_stock_threshold": 5}
        )
