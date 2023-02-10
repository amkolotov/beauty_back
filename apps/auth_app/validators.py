import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import (get_available_image_extensions, FileExtensionValidator)


def validate_phone(phone: str) -> str:
    """Провалидировать номер телефона"""
    print('validate')
    try:
        phone = phonenumbers.parse(phone)
    except phonenumbers.NumberParseException:
        raise ValidationError("Неверный формат номера")

    if not phonenumbers.is_valid_number(phone):
        raise ValidationError("Неверный формат номера")

    if str(phone.country_code) not in ('7', '8'):
        raise ValidationError("Номер из данной страны не поддерживается")

    print(phone, f"+{phone.country_code}{phone.national_number}")

    return f"+{phone.country_code}{phone.national_number}"


def validate_image_and_svg_file_extension(value):
    """Добавить svg в допустимые расширения изображений"""
    allowed_extensions = get_available_image_extensions() + ["svg"]
    return FileExtensionValidator(allowed_extensions=allowed_extensions)(value)
