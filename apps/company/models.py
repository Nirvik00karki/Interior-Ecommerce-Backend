# APP: company

from django.db import models
from cloudinary.models import CloudinaryField


class Office(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField()
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    google_maps_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    profile_picture = CloudinaryField("image", blank=True, null=True)
    designation = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    social_links = models.JSONField(default=list, blank=True)  # [{platform, url}]
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Award(models.Model):
    title = models.CharField(max_length=200)
    image = CloudinaryField("image", blank=True, null=True)
    date_received = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Partner(models.Model):
    name = models.CharField(max_length=200)
    logo = CloudinaryField("image", blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    message = models.TextField()
    profile_picture = CloudinaryField("image", blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.designation}"

class SocialMedia(models.Model):
    name = models.CharField(max_length=100)
    icon = CloudinaryField('icon', blank=True, null=True)
    link = models.URLField(max_length=300, blank=True, null=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name