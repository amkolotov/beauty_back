from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.salon.views import MainSalonInfoView, ReviewCreateApiView,\
    NotificationViewSet, OrderViewSet

urlpatterns = [
    path('main-info/', MainSalonInfoView.as_view(), name='main_info'),
    path('review/', ReviewCreateApiView.as_view(), name='review'),
]

router = DefaultRouter()
router.register(r'notification', NotificationViewSet, basename='notification')
router.register(r'order', OrderViewSet, basename='order')
urlpatterns += router.urls
