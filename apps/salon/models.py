from django.contrib.auth import get_user_model
from django.db import models

from apps.auth_app.fields import PhoneField
from apps.auth_app.models import BaseModel
from apps.auth_app.validators import validate_image_and_svg_file_extension
from apps.service.models import ServiceCategory

User = get_user_model()


class CompanyInfo(BaseModel):
    """Модель компании"""
    name = models.CharField('Наименование', max_length=128)
    logo = models.FileField('Логотип', upload_to='company',
                            validators=[validate_image_and_svg_file_extension])
    img = models.ImageField('Изображение', upload_to='company')
    address = models.CharField('Адрес', max_length=128, null=True, blank=True)
    phone = PhoneField('Телефон', max_length=20, null=True, blank=True)
    tagline = models.CharField('Слоган', max_length=256)
    decs = models.TextField('Описание')
    is_publish = models.BooleanField('Опубликована', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Компания'
        verbose_name_plural = 'Компания'

    def __str__(self):
        return self.name


class Salon(BaseModel):
    """Модель салона"""
    name = models.CharField('Наименование', max_length=128)
    address = models.CharField('Адрес', max_length=256)
    phone = PhoneField('Телефон', max_length=20, null=True, blank=True)
    desc = models.TextField('Описание')
    is_publish = models.BooleanField('Опубликован', default=False)

    class Meta:
        ordering = ['address']
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'

    def __str__(self):
        return self.name


class SalonImg(BaseModel):
    """Модель изображения салона"""
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE,
                              related_name='salon_imgs', verbose_name='Салон')
    img = models.ImageField('Изображение салона', upload_to='salons')
    is_main = models.BooleanField('Главное фото', default=False)
    is_publish = models.BooleanField('Опубликовано', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Изображение салона'
        verbose_name_plural = 'Изображения салона'

    def __str__(self):
        return self.salon.name


class Specialist(BaseModel):
    """Модель специалиста"""
    name = models.CharField('Имя', max_length=128)
    photo = models.ImageField('Фото', upload_to='specialists')
    position = models.CharField('Должность', max_length=128)
    experience = models.CharField('Стаж работы', max_length=128)
    title = models.CharField('Заголовок описания', max_length=128,
                             null=True, blank=True)
    text = models.TextField('Полное описание')
    services = models.ManyToManyField(ServiceCategory, verbose_name='Услуги',
                                      related_name='specialists')
    salons = models.ManyToManyField(Salon, verbose_name='Салоны',
                                    related_name='specialists')
    is_publish = models.BooleanField('Опубликовано', default=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return self.name


class WorkImg(BaseModel):
    """Модель изображения выполненной работы"""
    name = models.CharField('Наименование', max_length=128, null=True, blank=True)
    spec = models.ForeignKey(Specialist, on_delete=models.CASCADE,
                             related_name='work_imgs', verbose_name='Сотрудник')
    img = models.ImageField('Выполненная работа', upload_to='works')
    is_publish = models.BooleanField('Опубликовано', default=False)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Пример работы'
        verbose_name_plural = 'Примеры работ'

    def __str__(self):
        return f'{self.spec} - {self.name}'


class Sale(BaseModel):
    """Модель акций"""
    title = models.CharField('Заголовок', max_length=128)
    desc = models.CharField('Описание', max_length=512)
    text = models.TextField('Текст')
    button_text = models.CharField('Текст кнопки', max_length=29)
    img = models.ImageField('Изображение', upload_to='sales')
    salons = models.ManyToManyField(Salon, verbose_name='Салоны', related_name='sales')
    is_publish = models.BooleanField('Опубликована', default=False)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return self.title


class Review(BaseModel):
    """Модель отзыва"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             verbose_name='Пользователь', null=True)
    rating = models.IntegerField('Рейтинг')
    text = models.TextField('Текст')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, verbose_name='Салон',
                              related_name='salon_reviews', null=True, blank=True)
    spec = models.ForeignKey(Specialist, on_delete=models.CASCADE, verbose_name='Специалист',
                             related_name='spec_reviews', null=True, blank=True)
    is_publish = models.BooleanField('Опубликован', default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.user.username
