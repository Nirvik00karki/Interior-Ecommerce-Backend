from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PageViewSet, HeroSlideViewSet, MethodologyViewSet, FAQViewSet

router = DefaultRouter()
router.register("pages", PageViewSet)
router.register("hero-slides", HeroSlideViewSet)
router.register("methodologies", MethodologyViewSet)
router.register("faq", FAQViewSet)

urlpatterns = [
    # slug-based detail route for customer-facing API
    path(
        "pages/<slug:slug>/",
        PageViewSet.as_view({"get": "retrieve"}),
        name="page-by-slug"
    ),
] + router.urls
