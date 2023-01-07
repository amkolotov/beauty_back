from django.contrib.auth import get_user_model
from django.db import models

from apps.auth_app.models import BaseModel

User = get_user_model()


class ServiceCategory(BaseModel):
    """Модель категории услуг"""
    name = models.CharField('Наименование', max_length=128)
    img = models.ImageField('Изображение', upload_to='service_types')
    title = models.CharField('Заголовок описания', max_length=128,
                             null=True, blank=True)
    text = models.TextField('Полное описание')
    is_publish = models.BooleanField('Опубликовано', default=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'

    def __str__(self):
        return self.name


class Service(BaseModel):
    """Модель услуги"""
    name = models.CharField('Наименование', max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,
                                 related_name='services', verbose_name='Услуга')
    salons = models.ManyToManyField('salon.Salon', verbose_name='Салон', related_name='services')
    is_publish = models.BooleanField('Опубликовано', default=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class Order(BaseModel):
    """Модель заявки"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             verbose_name='Пользователь', related_name='orders')
    salon = models.ForeignKey('salon.Salon', on_delete=models.CASCADE,
                              verbose_name='Салон', related_name='salon_orders')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True,
                                verbose_name='Услуга', related_name='service_orders')
    spec = models.ForeignKey('salon.Specialist', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Cпециалист', related_name='spec_orders')
    date = models.DateTimeField('Дата бронирования')
    is_confirmed = models.BooleanField('Подтверждена', default=False)
    is_canceled = models.BooleanField('Отменена', default=False)
    is_completed = models.BooleanField('Выполнена', default=False)

    class Meta:
        ordering = ['user']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.salon}-{self.user}'
