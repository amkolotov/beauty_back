from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.salon.views import MainSalonInfoView, NotificationViewSet, OrderViewSet, \
    ReviewViewSet, FaqViewSet, ConfView

urlpatterns = [
    path('main-info/', MainSalonInfoView.as_view(), name='main_info'),
    path('conf/', ConfView.as_view(), name='conf'),
]

router = DefaultRouter()
router.register(r'notification', NotificationViewSet, basename='notification')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'review', ReviewViewSet, basename='review')
router.register(r'faq', FaqViewSet, basename='faq')
urlpatterns += router.urls
