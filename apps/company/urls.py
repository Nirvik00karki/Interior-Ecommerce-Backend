from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from .views import (
    OfficeViewSet, TeamMemberViewSet, AwardViewSet,
    PartnerViewSet, TestimonialViewSet, SocialMediaViewSet
)

router = DefaultRouter()
router.register("offices", OfficeViewSet)
router.register("team-members", TeamMemberViewSet)
router.register("awards", AwardViewSet)
router.register("partners", PartnerViewSet)
router.register("testimonials", TestimonialViewSet)
router.register("social-media", SocialMediaViewSet)

urlpatterns = [
    # slug-based detail route for customer-facing API (only match non-numeric slugs)
    re_path(
        r"^partners/(?P<slug>(?!\d+$)[\w-]+)/$",
        PartnerViewSet.as_view({"get": "retrieve"}, lookup_field="slug", lookup_url_kwarg="slug"),
        name="partner-by-slug"
    ),
] + router.urls
