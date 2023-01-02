from rest_framework import serializers

from apps.profile.models import Profile


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
