from rest_framework.routers import DefaultRouter
from .views import BlogCategoryViewSet, BlogPostViewSet

router = DefaultRouter()
router.register("categories", BlogCategoryViewSet)
router.register("posts", BlogPostViewSet)

urlpatterns = router.urls
