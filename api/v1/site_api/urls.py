from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.site_api.views import SiteMainSalonInfoView, PostSiteViewSet

urlpatterns = [
    path('main-info/', SiteMainSalonInfoView.as_view(), name='site_main_info'),
]

router = DefaultRouter()
router.register(r'post', PostSiteViewSet, basename='post')

urlpatterns += router.urls

