# APP: projects

from django.db import models
from cloudinary.models import CloudinaryField
from apps.company.models import TeamMember
from django.conf import settings

class Service(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cover_image = CloudinaryField("image", blank=True, null=True)

    def __str__(self):
        return self.name

class ServiceList(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="service_lists"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    cover_image = CloudinaryField("cover_image", blank=True, null=True)

    class Meta:
        unique_together = ("service", "slug")

    def __str__(self):
        return f"{self.service.name} - {self.name}"

class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover_image = CloudinaryField("cover_image", blank=True, null=True)
    icon = CloudinaryField("icon", blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("Completed", "Completed"),
        ("Ongoing", "Ongoing"),
        ("Future", "Future"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cover_image = CloudinaryField("image")
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
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects"
    )
    service_list = models.ForeignKey(
        ServiceList,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects"
    )
    team = models.ManyToManyField(TeamMember, blank=True)

    def __str__(self):
        return self.title

class ProjectGalleryImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )
    image = CloudinaryField("image")

    def __str__(self):
        return f"Image for {self.project.title}"
