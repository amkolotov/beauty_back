from django.urls import path

from api.v1.site_api.views import SiteMainSalonInfoView

urlpatterns = [

    path('main-info/', SiteMainSalonInfoView.as_view(), name='site_main_info'),

]
