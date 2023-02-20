from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.auth_app.fields import PhoneField
from apps.auth_app.models import BaseModel
from apps.auth_app.validators import validate_image_and_svg_file_extension
from apps.service.models import ServiceCategory
from apps.salon.tasks import send_push_notifications_task, send_push_order_confirmed_task, \
    send_salon_new_order_to_telegram_task

User = get_user_model()


class CompanyInfo(BaseModel):
    """Модель компании"""
    name = models.CharField('Наименование', max_length=128)
    logo = models.FileField('Логотип cветлый', upload_to='company',
                            validators=[validate_image_and_svg_file_extension])
    logo_black = models.FileField('Логотип темный', upload_to='company', null=True, blank=True,
                                  validators=[validate_image_and_svg_file_extension])
    img = models.ImageField('Изображение', upload_to='company')
    about_img = models.ImageField('Доп изображение для сайта', upload_to='company', null=True, blank=True)
    address = models.CharField('Адрес', max_length=128, null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, null=True, blank=True)
    email = models.EmailField('E-mail', null=True, blank=True)
    tagline = models.CharField('Слоган', max_length=256)
    decs = models.TextField('Описание')
    work_time = models.CharField('Часы работы', max_length=64, null=True, blank=True)
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
    phone = models.CharField('Телефон', max_length=20, null=True, blank=True)
    email = models.EmailField('E-mail', null=True, blank=True)
    short_desc = models.CharField('Краткое описание', max_length=128, null=True, blank=True)
    desc = models.TextField('Описание')
    work_time = models.CharField('Часы работы', max_length=64, null=True, blank=True)
    coords = models.CharField('Координаты(58.786093,62.516021)', max_length=64, null=True, blank=True)
    is_publish = models.BooleanField('Опубликован', default=False)

    class Meta:
        ordering = ['address']
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'

    def __str__(self):
        return self.name


class SalonImg(BaseModel):
    """Модель изображения салона"""
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='salon_imgs',
                              verbose_name='Салон')
    img = models.ImageField('Изображение салона', upload_to='salons')
    is_main = models.BooleanField('Главное фото', default=False)
    is_publish = models.BooleanField('Опубликовано', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Изображение салона'
        verbose_name_plural = 'Изображения салона'

    def __str__(self):
        return self.salon.name


class MessengerType(BaseModel):
    """Модель изображения мессенджера"""
    name = models.CharField('Наименование', max_length=28)
    img = models.FileField('Иконка', upload_to='messengers', validators=[validate_image_and_svg_file_extension])
    is_social = models.BooleanField('Это социальная сеть', default=False)
    is_publish = models.BooleanField('Опубликовано', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Тип мессенджера'
        verbose_name_plural = 'Типы мессенджеров'

    def __str__(self):
        return self.name


class Messenger(BaseModel):
    """Модель мессенджера"""
    type = models.ForeignKey(MessengerType, on_delete=models.CASCADE, verbose_name='Тип мессенджера')
    link = models.CharField('Ссылка на мессенджер', max_length=128)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='salon_messengers', verbose_name='Салон')
    for_company = models.BooleanField('Использовать для компании (салон не заполнять)', default=False)
    is_publish = models.BooleanField('Опубликована', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ссылка на мессенджер'
        verbose_name_plural = 'Ссылки на мессенджеры'

    def __str__(self):
        return self.link


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
                                      related_name='specialists', blank=True)
    salons = models.ManyToManyField(Salon, verbose_name='Салоны',
                                    related_name='specialists')
    is_manager = models.BooleanField('Менеджер', default=False)
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
    title = models.CharField('Заголовок', max_length=64,
                             help_text='Максимальная длина 64 символа')
    desc = models.CharField('Описание', max_length=128,
                            help_text='Максимальная длина 128 символов')
    text = models.TextField('Текст', max_length=512,
                            help_text='Максимальная длина 512 символов')
    button_text = models.CharField('Текст кнопки', max_length=29,
                                   help_text='Максимальная длина 29 символов')
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
                             verbose_name='Пользователь', null=True, blank=True)
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
        if self.user:
            return self.user.email
        return ''


STATUSES = (
    (New := 'new', 'Новая'),
    (CONFIRMED := 'confirmed', 'Подтверждена'),
    (CANCELED := 'canceled', 'Отменена'),
    (COMPLETED := 'completed', 'Выполнена'),
)


class Order(BaseModel):
    """Модель заявки"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Пользователь', related_name='orders')
    name = models.CharField('Имя', max_length=256, null=True, blank=True)
    phone = PhoneField('Телефон', max_length=20)
    salon = models.ForeignKey('salon.Salon', on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Салон', related_name='salon_orders')
    service = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Услуга', related_name='service_orders')
    spec = models.ForeignKey('salon.Specialist', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Cпециалист', related_name='spec_orders')
    date = models.DateTimeField('Дата и время бронирования')
    status = models.CharField('Статус', max_length=10, choices=STATUSES, default='new')
    source = models.CharField('Источник', max_length=10, default='app')
    comment = models.TextField('Комментарий', null=True, blank=True)
    is_processed = models.BooleanField('Обработана', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        user = self.user if self.user else ''
        return f'{self.salon}-{user}'

    def save(self, *args, **kwargs):
        if self.status != 'new':
            self.is_processed = True
            super().save(*args, **kwargs)


@receiver(post_save, sender=Order)
def send_order_confirm(sender, instance, **kwargs):
    if instance.user and instance.status == 'confirmed':
        send_push_order_confirmed_task.delay(instance.id)


@receiver(post_save, sender=Order)
def send_telegram(sender, instance, created, **kwargs):
    if created and instance.salon and instance.status == 'new':
        send_salon_new_order_to_telegram_task.delay(instance.id)


class Notification(BaseModel):
    """Модель уведомлений"""
    title = models.CharField('Заголовок', max_length=128, null=True, blank=True)
    text = models.TextField('Текст', max_length=512, null=True, blank=True)
    read = models.ManyToManyField(User, related_name='read_notifications')
    for_users = models.ManyToManyField(User, related_name='personal_notifications',
                                       blank=True, verbose_name='Для конкретных клиентов')
    for_salons = models.ManyToManyField(Salon, blank=True, verbose_name='Для клиентов салонов')
    for_all = models.BooleanField('Для всех клиентов компании', default=True)
    is_publish = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return self.text


@receiver(post_save, sender=Notification)
def update_notification(sender, instance, **kwargs):
    if instance.is_publish:
        send_push_notifications_task.delay(instance.id)


class Faq(BaseModel):
    """Модель вопроса"""
    question = models.CharField('Вопрос', max_length=512)
    answer = RichTextField('Текст')
    is_publish = models.BooleanField('Опубликован', default=False)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'FAQ'

    def __str__(self):
        return self.question


class MobileAppSection(BaseModel):
    """Модель секции мобильного приложения для сайта"""
    title = models.CharField('Текст блока', max_length=70)
    text = models.CharField('Текст блока', max_length=128)
    promo = models.CharField('Промо', max_length=15)
    img = models.ImageField('Изображение для страницы приложения',
                            upload_to='site', null=True, blank=True)
    img_for_section = models.ImageField('Изображение для секции приложения',
                            upload_to='site', null=True, blank=True)
    is_publish = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Секция мобильного приложения'
        verbose_name_plural = 'Секция мобильного приложения'

    def __str__(self):
        return self.title


class Store(BaseModel):
    """Модель магазина приложений"""
    name = models.CharField('Наименование', max_length=64)
    section = models.ForeignKey(MobileAppSection, on_delete=models.CASCADE,
                                verbose_name='Секция', related_name='stores')
    img = models.FileField('Изображение ', upload_to='app_stores',
                           validators=[validate_image_and_svg_file_extension])
    link = models.CharField('Ссылка', max_length=512)
    is_publish = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Магазин приложений'
        verbose_name_plural = 'Магазины приложений'

    def __str__(self):
        return self.name


class AppReasons(BaseModel):
    """Модель причин для установки приложения"""
    title = models.CharField('Заголовок', max_length=64)
    section = models.ForeignKey(MobileAppSection, on_delete=models.CASCADE,
                                verbose_name='Секция', related_name='reasons')
    img = models.FileField('Изображение ', upload_to='app_stores',
                           validators=[validate_image_and_svg_file_extension])
    text = models.TextField('Текст')
    is_publish = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Причина для установки приложения'
        verbose_name_plural = 'Причины для установки приложения'

    def __str__(self):
        return self.title


class ConfInfo(BaseModel):
    """Модель политики конфиденциальности"""
    title = models.CharField('Заголовок', max_length=64)
    text = models.TextField('Текст')
    is_publish = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Политика конфиденциальности'
        verbose_name_plural = 'Политика конфиденциальности'

    def __str__(self):
        return self.title


class TgSettings(BaseModel):
    """Модель настройки телеграмм бота"""
    salon = models.OneToOneField('salon.Salon', on_delete=models.CASCADE, verbose_name='Салон')
    token = models.CharField('Токен бота ТГ', max_length=128, null=True)
    is_publish = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Телеграмм бота'
        verbose_name_plural = 'Телеграмм боты'

    def __str__(self):
        return f'{self.salon.name}-{self.token if self.token else ""}'


class ChatsIds(BaseModel):
    """ID чата пользователя"""
    name = models.CharField('Имя пользователя', max_length=128)
    chat_id = models.PositiveIntegerField('ID чата')
    tg_bot = models.ForeignKey(TgSettings, on_delete=models.CASCADE, related_name='chats')

    class Meta:
        ordering = ['name']
        verbose_name = 'Пользователь ТГ'
        verbose_name_plural = 'Пользователи ТГ'

    def __str__(self):
        return f'{self.name}-{self.chat_id}'
