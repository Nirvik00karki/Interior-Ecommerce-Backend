# catalog/admin.py

from django.contrib import admin
from .models import (
    Category, Product, ProductImage,
    Attribute, AttributeValue,
    ProductVariant, ProductVariantAttribute
)


# ---------------------------------------------------------
# CATEGORY ADMIN
# ---------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


# ---------------------------------------------------------
# PRODUCT IMAGE INLINE
# ---------------------------------------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# ---------------------------------------------------------
# PRODUCT VARIANT ATTRIBUTE INLINE
# ---------------------------------------------------------
class ProductVariantAttributeInline(admin.TabularInline):
    model = ProductVariantAttribute
    extra = 1
    autocomplete_fields = ["attribute", "value"]


# ---------------------------------------------------------
# PRODUCT VARIANT INLINE
# ---------------------------------------------------------
class ProductVariantInline(admin.StackedInline):
    model = ProductVariant
    extra = 1
    show_change_link = True
    autocomplete_fields = ["product"]
    inlines = [ProductVariantAttributeInline]


# ---------------------------------------------------------
# PRODUCT ADMIN
# ---------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductVariantInline]
    ordering = ("name",)


# ---------------------------------------------------------
# ATTRIBUTE ADMIN
# ---------------------------------------------------------
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("attribute", "value")
    list_filter = ("attribute",)
    search_fields = ("value",)


# ---------------------------------------------------------
# PRODUCT VARIANT ADMIN
# ---------------------------------------------------------
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product", "name", "sku", "price",
        "stock", "is_active", "created_at"
    )
    list_filter = ("is_active", "product")
    search_fields = ("sku", "name")
    inlines = [ProductVariantAttributeInline]
    ordering = ("product", "sku")
