from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'service', ServiceViewSet, basename='post')

urlpatterns = router.urls