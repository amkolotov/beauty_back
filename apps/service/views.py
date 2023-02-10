from django.shortcuts import render
from rest_framework import mixins, viewsets


class ServiceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Вьюсет видов сервисов"""
    pass

