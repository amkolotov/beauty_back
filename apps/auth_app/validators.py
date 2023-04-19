import datetime

import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import (get_available_image_extensions, FileExtensionValidator)


def validate_phone(phone: str) -> str:
    """Провалидировать номер телефона"""

    try:
        phone = phonenumbers.parse(phone)
    except phonenumbers.NumberParseException:
        raise ValidationError("Неверный формат номера")

    if not phonenumbers.is_valid_number(phone):
        raise ValidationError("Неверный формат номера")

    if str(phone.country_code) not in ('7', '8'):
        raise ValidationError("Номер из данной страны не поддерживается")

    return f"+{phone.country_code}{phone.national_number}"


def validate_image_and_svg_file_extension(value):
    """Добавить svg в допустимые расширения изображений"""
    allowed_extensions = get_available_image_extensions() + ["svg"]
    return FileExtensionValidator(allowed_extensions=allowed_extensions)(value)


def validate_segment(number: int) -> int:
    """Провалидировать сегмент расписание"""
    if number > 48 or number <= 0:
        raise ValidationError("Несуществующий сегмент расписания")
    return number


def validate_time(time: datetime.time) -> datetime.time:
    if time.minute == 0 or time.minute == 30:
        return time
    raise ValidationError('Минуты должны быть кратны 0 или 30')
