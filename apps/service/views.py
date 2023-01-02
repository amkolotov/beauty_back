from django.shortcuts import render

from apps.service.models import ServiceType


class ServiceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Вьюсет видов сервисов"""
    serializer_class = ServiceTypeSerializer
    queryset = ServiceType.objects.all()

