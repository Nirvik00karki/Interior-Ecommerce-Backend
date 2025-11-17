from django.contrib import admin
from .models import BlogCategory, BlogPost

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "blog_category", "author", "is_published", "date")
    search_fields = ("title", "excerpt", "content")
    list_filter = ("is_published", "blog_category", "date")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date"
