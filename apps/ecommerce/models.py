# APP: ecommerce

from django.db import models
from cloudinary.models import CloudinaryField


class ProductCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField("image")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
