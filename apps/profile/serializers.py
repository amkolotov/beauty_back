from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.profile.models import Profile
from apps.salon.serializers import OrderSerializer, NotificationSerializer

User = get_user_model()


class ProfileAvatarSerializer(serializers.ModelSerializer):
    """Сериалайзер данных профиля пользователя"""

    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar']

    def save(self, *args, **kwargs):
        if self.instance.avatar:
            self.instance.avatar.delete()
        return super().save(*args, **kwargs)


class UserDataSerializer(serializers.ModelSerializer):
    """Изменение данных пользователя"""

    avatar = serializers.ImageField(source='profile.avatar')
    orders = OrderSerializer(many=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'phone', 'avatar', 'orders')
        read_only_fields = ('email', 'avatar', 'orders')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.profile.avatar:
            data['avatar'] = instance.profile.avatar.url
        return data
