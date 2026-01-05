# catalog/models.py

from django.db import models
from cloudinary.models import CloudinaryField


# ---------------------------------------------------------
# CATEGORY
# ---------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = CloudinaryField("image", blank=True, null=True)

    # SEO - standard for ecommerce
    # meta_title = models.CharField(max_length=255, blank=True, null=True)
    # meta_description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ---------------------------------------------------------
# PRODUCT
# ---------------------------------------------------------
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    # main display image
    main_image = CloudinaryField("image", blank=True, null=True)

    # SEO fields
    # meta_title = models.CharField(max_length=255, blank=True, null=True)
    # meta_description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def min_price(self):
        variant = self.variants.order_by("price").first()
        return variant.price if variant else None

    @property
    def max_price(self):
        variant = self.variants.order_by("-price").first()
        return variant.price if variant else None


# ---------------------------------------------------------
# PRODUCT IMAGE (ADDITIONAL GALLERY IMAGES)
# ---------------------------------------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = CloudinaryField("image")

    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_featured"]

    def __str__(self):
        return f"Image for {self.product.name}"


# ---------------------------------------------------------
# DYNAMIC ATTRIBUTE SYSTEM
# The same attributes apply at both product & variant levels
# ---------------------------------------------------------
class Attribute(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Example: Color, Size, Material

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="values"
    )
    value = models.CharField(max_length=100)

    class Meta:
        unique_together = ("attribute", "value")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


# ---------------------------------------------------------
# PRODUCT VARIANT
# ---------------------------------------------------------
class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )

    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)  # Example: "Red / Large"
    image = CloudinaryField("image", blank=True, null=True)

    # Pricing lives ONLY here
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Inventory lives here (variant-specific)
    stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product", "sku"]

    def __str__(self):
        return f"{self.product.name} - {self.name}"


# ---------------------------------------------------------
# MAPPING TABLE FOR VARIANT ATTRIBUTES
# ---------------------------------------------------------
class ProductVariantAttribute(models.Model):
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="attributes"
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("variant", "attribute")

    def __str__(self):
        return f"{self.variant} - {self.attribute.name}: {self.value.value}"

# ---------------------------------------------------------
# Inventory
# ---------------------------------------------------------
class Inventory(models.Model):
    variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory"
    )
    quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    reserved_stock = models.PositiveIntegerField(default=0)

    @property
    def available_stock(self):
        return self.stock - self.reserved_stock

    def __str__(self):
        return f"{self.product_variant.sku} | Stock: {self.stock} | Reserved: {self.reserved_stock}"
