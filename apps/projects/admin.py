from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Service, Project, ProjectServiceLink


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    
class ProjectServiceInline(admin.TabularInline):
    model = ProjectServiceLink
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "get_services",
        "status",
        "is_featured",
        "date_completed",
    )

    search_fields = ("title", "slug", "location")
    list_filter = ("status", "is_featured")
    prepopulated_fields = {"slug": ("title",)}

    inlines = [ProjectServiceInline]

    def get_services(self, obj):
        return ", ".join(obj.services.values_list("name", flat=True))

    get_services.short_description = "Services"
