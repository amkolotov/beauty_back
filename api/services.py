from config import settings


def get_absolute_uri(context: dict, url: str) -> str:
    if settings.DEBUG:
        return context['request'].build_absolute_uri(url)
    return context['request'].build_absolute_uri(url).replace('http', 'https')
