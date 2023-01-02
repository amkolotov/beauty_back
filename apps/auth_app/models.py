from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone

from apps.auth_app.fields import PhoneField


class BaseModel(models.Model):
    """Базовая модель"""
    created_at = models.DateTimeField('Дата создания', default=timezone.now, db_index=True)
    updated_at = models.DateTimeField('Дата обновления', default=timezone.now, db_index=True)

    class Meta:
        ordering = ('-updated_at',)
        abstract = True


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """Создает пользователя"""
        if not email:
            raise ValueError("Вы не ввели Email")
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Создает обычного пользователя"""
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Создает суперпользователя"""
        return self._create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractUser):
    """Модель пользователя"""
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField('Email', unique=True)
    phone = PhoneField('Телефон', max_length=20, null=True, blank=True)
    username = models.CharField('Имя пользователя', max_length=150, null=True,
                                blank=True, validators=[username_validator])
    created_at = models.DateTimeField('Дата создания', default=timezone.now, db_index=True)
    updated_at = models.DateTimeField('Дата обновления', default=timezone.now, db_index=True)

    objects = UserManager()

    class Meta:
        ordering = ('-updated_at',)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Code(BaseModel):
    """Модель кода авторизации"""
    hash = models.CharField(max_length=128)
    expires_at = models.DateTimeField(db_index=True)
    user = models.ForeignKey(User, models.CASCADE, related_name="codes")

    class Meta:
        verbose_name = "Код авторизации"
        verbose_name_plural = "Коды авторизации"
        db_table = 'codes'
