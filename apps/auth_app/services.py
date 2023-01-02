import hashlib
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from apps.auth_app.models import Code
from config import settings

User = get_user_model()


def make_hash(code: str) -> str:
    """Создать хэш кода авторизации"""

    payload = code + settings.SECRET_KEY
    return hashlib.sha256(payload.encode("utf8")).hexdigest()


def check_hash(code: str, hash: str) -> bool:
    """Проверить хэш кода авторизации"""

    return make_hash(code) == hash


def generate_code(length: int) -> str:
    """Сгенерировать код авторизации"""

    code = random.randint(0, 10**length)
    return str(code).rjust(length, "0")


def send_email(user: User, code: str) -> None:
    """Отправить электронное письмо"""
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения регистрации: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def send_code(user: User) -> Code:
    """Выдать код авторизации"""

    from apps.auth_app.models import Code

    code = generate_code(settings.AUTH_CODE_LENGTH)

    expires_at = timezone.now() + settings.AUTH_CODE_LIFETIME
    instance = Code.objects.create(user=user, expires_at=expires_at, hash=make_hash(code))

    send_email(user, code)

    return instance


def authenticate(email: str, code: str) -> User | None:
    """Авторизовать пользователя по номеру телефона и коду авторизации"""

    unexpired_codes = Code.objects.filter(user__email=email, expires_at__gte=timezone.now())

    for code_instance in unexpired_codes:
        if check_hash(code, code_instance.hash):
            code_instance.delete()
            return code_instance.user


def get_code_wait_time(user: User) -> timedelta:
    """Получить время ожидания для отправки следующего авторизационного кода"""

    if (code := user.codes.order_by("-created_at").first()) is not None:
        wait_to = code.created_at + settings.AUTH_CODE_ISSUE_THRESHOLD
        return wait_to - timezone.now()

    return timedelta()
