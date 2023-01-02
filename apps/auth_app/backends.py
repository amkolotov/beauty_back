from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from apps.auth_app import services

User = get_user_model()


class CodeBackend(ModelBackend):
    """Бэкенд для авторизации по номеру телефона и коду авторизации"""

    def authenticate(self, *args, email: str = None, code: str = None, **kwargs) -> User | None:
        """Авторизовать пользователя по номеру телефона и коду авторизации"""

        if None not in [email, code]:
            return services.authenticate(email, code)
