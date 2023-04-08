from rest_framework.request import Request

from config import settings


def get_absolute_uri(request: Request, url: str) -> str:
    if settings.DEBUG:
        return request.build_absolute_uri(url)
    return request.build_absolute_uri(url).replace('http', 'https')
