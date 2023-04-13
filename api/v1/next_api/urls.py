from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.next_api.views import HomeView, PostSiteViewSet, FaqSiteViewSet, \
    FooterView, ContactsView, SalonsView, AboutView, SaleViewSet, ServiceView,\
    CeoView, SpecialistViewSet

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', ContactsView.as_view(), name='contacts'),

    path('salons/<slug:salon_slug>/<slug:service_slug>', ServiceView.as_view(), name='service'),
    path('salons/<slug:slug>', SalonsView.as_view(), name='salons'),

    path('footer/', FooterView.as_view(), name='footer'),
    path('ceo/', CeoView.as_view(), name='footer'),
]

router = DefaultRouter()
router.register(r'posts', PostSiteViewSet, basename='posts')
router.register(r'faqs', FaqSiteViewSet, basename='faqs')
router.register(r'sales', SaleViewSet, basename='sales')
router.register(r'specialists', SpecialistViewSet, basename='specialists')

urlpatterns += router.urls

