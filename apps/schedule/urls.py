from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.salon.views import MainSalonInfoView, NotificationViewSet, OrderViewSet, \
    ReviewViewSet, FaqViewSet, ConfView
from apps.schedule.views import schedule

urlpatterns = [
    path('', schedule, name='schedule'),
]

