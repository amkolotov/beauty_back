from rest_framework.routers import DefaultRouter

from apps.blog.views import PostViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='post')

urlpatterns = router.urls
