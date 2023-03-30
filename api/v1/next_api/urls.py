from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.next_api.views import HomeView, PostSiteViewSet, FaqSiteViewSet,\
    FooterView, ContactsView, SalonsView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home_info'),
    path('footer/', FooterView.as_view(), name='footer_info'),
    path('contacts/', ContactsView.as_view(), name='contacts_info'),
    path('salons/<str:slug>', SalonsView.as_view(), name='contacts_info'),
]

router = DefaultRouter()
router.register(r'post', PostSiteViewSet, basename='post')
router.register(r'faq', FaqSiteViewSet, basename='faq')

urlpatterns += router.urls

