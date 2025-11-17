from rest_framework.routers import DefaultRouter
from .views import (
    OfficeViewSet, TeamMemberViewSet, AwardViewSet,
    PartnerViewSet, TestimonialViewSet
)

router = DefaultRouter()
router.register("offices", OfficeViewSet)
router.register("team-members", TeamMemberViewSet)
router.register("awards", AwardViewSet)
router.register("partners", PartnerViewSet)
router.register("testimonials", TestimonialViewSet)

urlpatterns = router.urls
