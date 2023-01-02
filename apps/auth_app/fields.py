from django.db import models
from django.db.models import fields

from apps.auth_app.validators import validate_phone, validate_image_and_svg_file_extension


class PhoneField(fields.CharField):
    """Поле номера телефона"""

    default_validators = [validate_phone]


class SVGImageField(models.ImageField):
    """Поле svg изображения"""

    default_validators = [validate_image_and_svg_file_extension]
