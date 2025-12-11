from rest_framework.routers import DefaultRouter
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

urlpatterns = router.urls
