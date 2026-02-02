from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review


@receiver([post_save, post_delete], sender=Review)
def update_product_rating(sender, instance, **kwargs):
    """
    Update cached rating fields on Product when Review is created, updated, or deleted.
    This significantly improves performance by avoiding repeated aggregations.
    """
    product = instance.product
    
    # Calculate new ratings from active reviews only
    active_reviews = product.reviews.filter(is_active=True)
    avg_rating = active_reviews.aggregate(Avg("rating"))["rating__avg"]
    
    # Update product fields
    product.average_rating = round(avg_rating, 1) if avg_rating else 0
    product.review_count = active_reviews.count()
    product.save(update_fields=["average_rating", "review_count"])
