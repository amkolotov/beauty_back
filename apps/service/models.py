from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

from apps.auth_app.models import BaseModel

User = get_user_model()


class ServiceCategory(BaseModel):
    """Модель категории услуг"""
    name = models.CharField('Наименование', max_length=128)
    img = models.ImageField('Изображение', upload_to='service_types',
                            help_text='Рекомендуемый размер 370Х310px')
    title = models.CharField('Заголовок описания', max_length=128,
                             null=True, blank=True)
    text = models.TextField('Полное описание')
    is_publish = models.BooleanField('Опубликовано', default=False)
    slug = models.SlugField('Слаг', unique=True, max_length=255, db_index=True,
                            help_text='Если не заполнено, создается автоматически',
                            null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class AddServiceImg(BaseModel):
    """Модель изображения услуги для сайта"""
    service = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,
                                related_name='service_imgs', verbose_name='Услуга')
    img = models.ImageField('Изображение услуги для сайта', upload_to='services_types_site',
                            help_text='Рекомендуемый размер 370Х310px')

    class Meta:
        ordering = ['service']
        verbose_name = 'Изображение для сайта'
        verbose_name_plural = 'Изображения для сайта'

    def __str__(self):
        return f'{self.id} - {self.service}'


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
