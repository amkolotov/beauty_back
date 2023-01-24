from django.db import models
from ckeditor.fields import RichTextField

from apps.auth_app.models import BaseModel
from apps.salon.models import Salon


class Post(BaseModel):
    """Модель поста"""
    image = models.ImageField('Изображение', upload_to='posts')
    title = models.CharField('Заголовок', max_length=256)
    text = RichTextField('Текст')
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, null=True, blank=True)
    is_publish = models.BooleanField('Опубликован', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title
