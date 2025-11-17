from django.contrib import admin
from .models import Office, TeamMember, Award, Partner, Testimonial

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "address", "email")

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "office", "order")
    search_fields = ("name", "designation")
    list_filter = ("office",)
    ordering = ("order",)

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("title", "date_received")
    search_fields = ("title",)

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "website_url")
    search_fields = ("name",)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "designation")
    search_fields = ("name", "designation", "message")
