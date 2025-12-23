# APP: cms

from django.db import models
from cloudinary.models import CloudinaryField


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    cover_image = CloudinaryField("image", blank=True, null=True)
    brief = models.TextField(blank=True)

    def __str__(self):
        return self.title


class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200, blank=True)
    image = CloudinaryField("image", blank=True, null=True)
    video_url = CloudinaryField(
        resource_type="video",
        blank=True,
        null=True
    )
    link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Methodology(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_or_icon = CloudinaryField("image", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question
