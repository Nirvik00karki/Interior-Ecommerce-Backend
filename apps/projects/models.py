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
    gallery_images = models.JSONField(default=list, blank=True)  # ["url1", "url2"]
    location = models.CharField(max_length=200, blank=True)
    date_completed = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    is_featured = models.BooleanField(default=False)

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    team = models.ManyToManyField(TeamMember, blank=True)

    def __str__(self):
        return self.title
