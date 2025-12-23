# APP: projects

from django.db import models
from cloudinary.models import CloudinaryField
from apps.company.models import TeamMember
from django.conf import settings

class Service(models.Model):
    SERVICE_TYPE_CHOICES = (
        ("service", "Service"),
        ("product", "Product"),
        ("both", "Both"),
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover_image = CloudinaryField("cover_image", blank=True, null=True)
    icon = CloudinaryField("icon", blank=True, null=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children"
    )

    type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default="service")
    is_ksp = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover_image = CloudinaryField("cover_image", blank=True, null=True)
    icon = CloudinaryField("icon", blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = (
        ("completed", "Completed"),
        ("ongoing", "Ongoing"),
        ("future", "Future"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cover_image = CloudinaryField("cover_image", blank=True, null=True)

    location = models.CharField(max_length=200, blank=True)
    date_completed = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    is_featured = models.BooleanField(default=False)

    sector = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects"
    )

    services = models.ManyToManyField(
        Service,
        through="ProjectServiceLink",
        related_name="projects"
    )

    team = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

class ProjectServiceLink(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("project", "service")

    def __str__(self):
        return f"{self.project} - {self.service}"

class ProjectGalleryImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )
    image = CloudinaryField("image", blank=True, null=True)

    def __str__(self):
        return f"Gallery image for {self.project.title}"
    
class Package(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    cover_image = CloudinaryField("cover_image", blank=True, null=True)

    project_design_time = models.PositiveIntegerField(help_text="Days")
    project_manufacture_time = models.PositiveIntegerField(help_text="Days")
    project_installation_time = models.PositiveIntegerField(help_text="Days")

    basic_price = models.DecimalField(max_digits=10, decimal_places=2)
    premium_price = models.DecimalField(max_digits=10, decimal_places=2)

    support_service = models.TextField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class PackageItem(models.Model):
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product_id = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.package.name} item {self.product_id}"



