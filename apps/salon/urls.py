from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.salon.views import MainSalonInfoView, NotificationViewSet, OrderViewSet, ReviewViewSet

urlpatterns = [
    path('main-info/', MainSalonInfoView.as_view(), name='main_info'),
]

router = DefaultRouter()
router.register(r'notification', NotificationViewSet, basename='notification')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'review', ReviewViewSet, basename='review')
urlpatterns += router.urls
