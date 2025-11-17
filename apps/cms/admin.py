from django.contrib import admin
from .models import Page, HeroSlide, Methodology, FAQ

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_published")
    ordering = ("order",)

@admin.register(Methodology)
class MethodologyAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    ordering = ("order",)
