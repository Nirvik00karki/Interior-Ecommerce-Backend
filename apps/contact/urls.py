from rest_framework.routers import DefaultRouter
from .views import ContactSubmissionViewSet

router = DefaultRouter()
router.register("contact-submissions", ContactSubmissionViewSet)

urlpatterns = router.urls
