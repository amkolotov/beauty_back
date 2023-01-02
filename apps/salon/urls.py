from django.urls import path

from apps.salon.views import MainSalonInfoView

urlpatterns = [
    path('main-info/', MainSalonInfoView.as_view(), name='main_info'),
]