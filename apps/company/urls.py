from rest_framework.routers import DefaultRouter
from django.urls import path
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
    # slug-based detail route for customer-facing API (use the action on the viewset)
    path(
        "partners/slug/<slug:slug>/",
        PartnerViewSet.as_view({"get": "retrieve_by_slug"}),
        name="partner-by-slug"
    ),
] + router.urls
