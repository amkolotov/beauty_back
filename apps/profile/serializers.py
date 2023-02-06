from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.profile.models import Profile

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

    avatar = serializers.ImageField(source='profile.avatar', required=False)
    salon_id = serializers.IntegerField(source='profile.salon_id', required=False)
    expo_token = serializers.CharField(source='profile.expo_token', required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'phone', 'avatar', 'expo_token', 'salon_id')
        read_only_fields = ('email', 'avatar',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not hasattr(instance, 'profile'):
            Profile.objects.get_or_create(user=self.instance)
        if instance.profile.avatar:
            request = self.context.get('request')
            data['avatar'] = request.build_absolute_uri(instance.profile.avatar.url)
        return data

    def update(self, instance, validated_data):
        profile_data = validated_data.get('profile')
        if profile_data and profile_data.get('expo_token'):
            instance.profile.expo_token = profile_data.get('expo_token')
            instance.profile.save()
        if profile_data and profile_data.get('salon_id'):
            instance.profile.salon_id = profile_data.get('salon_id')
            instance.profile.save()
        return instance
