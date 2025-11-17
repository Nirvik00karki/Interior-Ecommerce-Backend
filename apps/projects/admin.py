from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Service, Project
from apps.company.models import TeamMember

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "service", "status", "is_featured", "date_completed")
    search_fields = ("title", "slug", "location")
    list_filter = ("status", "is_featured", "service")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("team",)
