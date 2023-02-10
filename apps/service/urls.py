from rest_framework.routers import DefaultRouter

from apps.service.views import ServiceViewSet

router = DefaultRouter()
router.register(r'service', ServiceViewSet, basename='service')

urlpatterns = router.urls
