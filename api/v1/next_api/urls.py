from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.next_api.views import SiteMainSalonInfoView, PostSiteViewSet, FaqSiteViewSet

urlpatterns = [
    path('main-info/', SiteMainSalonInfoView.as_view(), name='site_main_info'),
]

router = DefaultRouter()
router.register(r'post', PostSiteViewSet, basename='post')
router.register(r'faq', FaqSiteViewSet, basename='faq')

urlpatterns += router.urls

