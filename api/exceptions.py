from rest_framework.exceptions import Throttled as BaseThrottled


class Throttled(BaseThrottled):
    """Класс переопределяющий аттрибуты базового класса ошибки"""

    default_code = "limited"
    default_detail = "Превышен лимит запросов."
    extra_detail_plural = "Попробуйте через {wait} секунд."
    extra_detail_singular = "Попробуйте через {wait} секунд."
