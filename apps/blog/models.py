# APP: blog

from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings


class BlogCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    cover_image = CloudinaryField("image")
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    tags = models.JSONField(default=list, blank=True)
    blogpost_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=150, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
