from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from apps.auth_app.models import BaseModel
from apps.salon.models import Salon

User = get_user_model()


class Profile(BaseModel):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField('Аватар', upload_to='avatars', null=True, blank=True)
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, null=True, blank=True)
    expo_token = models.CharField('Push токен', max_length=128, null=True, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        db_table = 'profile'

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url

    def avatar_img(self):
        if src := self.get_avatar():
            return mark_safe(f'<img src="{src}" width="50" height="50" />')
        else:
            return '-'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
