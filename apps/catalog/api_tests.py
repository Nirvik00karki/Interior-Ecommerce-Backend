from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.catalog.models import (
    Category, Product, ProductImage, 
    Attribute, AttributeValue, 
    ProductVariant, ProductVariantAttribute, Inventory
)
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class CatalogAPITests(APITestCase):
    def setUp(self):
        # Create admin user for write operations
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", 
            password="adminpassword"
        )
        # Create regular user for read-only checks if applicable
        self.regular_user = User.objects.create_user(
            email="user@example.com", 
            password="userpassword"
        )
        self.client.force_authenticate(user=self.admin_user)

        # Base test data
        self.category = Category.objects.create(name="Furniture", slug="furniture")
        self.product = Product.objects.create(
            name="Wooden Table", 
            slug="wooden-table", 
            category=self.category
        )
        self.attribute = Attribute.objects.create(name="Color")
        self.attr_value = AttributeValue.objects.create(attribute=self.attribute, value="Brown")
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku="WT-BRW",
            name="Brown Table",
            price=150.00
        )
        self.variant_attr = ProductVariantAttribute.objects.create(
            variant=self.variant,
            attribute=self.attribute,
            value=self.attr_value
        )
        self.inventory = Inventory.objects.create(
            variant=self.variant,
            stock=10,
            low_stock_threshold=2
        )

    # -------------------
    # Category Tests
    # -------------------
    def test_category_list(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_create(self):
        url = reverse("category-list")
        data = {"name": "Decor", "slug": "decor", "description": "Home decor items"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_category_retrieve_by_slug(self):
        url = reverse("category-by-slug", kwargs={"slug": self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    # -------------------
    # Product Tests
    # -------------------
    def test_product_list(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create(self):
        url = reverse("product-list")
        data = {
            "name": "Metal Chair", 
            "slug": "metal-chair", 
            "category": self.category.id,
            "description": "Sturdy metal chair"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_retrieve_by_slug_action(self):
        url = reverse("product-by-slug", kwargs={"slug": self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    # -------------------
    # Product Variant Tests
    # -------------------
    def test_variant_list(self):
        url = reverse("productvariant-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_variant_create(self):
        url = reverse("productvariant-list")
        data = {
            "product": self.product.id,
            "sku": "WT-BLK",
            "name": "Black Table",
            "price": 160.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # -------------------
    # Attribute & Value Tests
    # -------------------
    def test_attribute_list(self):
        url = reverse("attribute-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attribute_value_list(self):
        url = reverse("attributevalue-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------
    # Product Image Tests
    # -------------------
    def test_product_image_create(self):
        url = reverse("productimage-list")
        # Mocking an image upload might be complex without real image handling, 
        # but let's try a simple one if the field allows it.
        # If it uses Cloudinary, we might just test without image file or mock it.
        data = {
            "product": self.product.id,
            "alt_text": "Main image",
            "is_featured": True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # -------------------
    # Variant Attribute Tests
    # -------------------
    def test_variant_attribute_list(self):
        url = reverse("productvariantattribute-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------
    # Inventory Tests
    # -------------------
    def test_inventory_list(self):
        url = reverse("inventory-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inventory_update(self):
        url = reverse("inventory-detail", kwargs={"pk": self.inventory.id})
        data = {"stock": 20}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.stock, 20)
