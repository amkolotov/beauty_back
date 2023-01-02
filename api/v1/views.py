from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.exceptions import Throttled


class BaseAPIView(APIView):
    """Базовая view для апи, переопределяющая класс ошибки превышения лимита запросов"""

    def throttled(self, request: Request, wait: float) -> None:
        raise Throttled(wait)


class BaseGenericAPIView(GenericAPIView, BaseAPIView):
    """Базовый GenericAPIView"""


class BaseGenericViewSet(GenericViewSet, BaseAPIView):
    """Базовый GenericViewSet"""
