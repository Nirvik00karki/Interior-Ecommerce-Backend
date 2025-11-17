from rest_framework.routers import DefaultRouter
from .views import PageViewSet, HeroSlideViewSet, MethodologyViewSet, FAQViewSet

router = DefaultRouter()
router.register("pages", PageViewSet)
router.register("hero-slides", HeroSlideViewSet)
router.register("methodologies", MethodologyViewSet)
router.register("faq", FAQViewSet)

urlpatterns = router.urls
