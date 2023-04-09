from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from api.exceptions import Throttled
from api.services import get_absolute_uri
from apps.auth_app import services
from apps.profile.models import Profile
from apps.auth_app.validators import validate_phone as phone_validator

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Регистрация пользователя"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'username', 'phone')

    def validate_phone(self, value):
        return phone_validator(value)

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        return attrs

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data['email']).first()
        if user:
            if user.is_active:
                raise AuthenticationFailed("Пользователь уже существует")
            if (wait := services.get_code_wait_time(user)) > timedelta():
                raise Throttled(wait=wait.total_seconds(), code="limited_phone")

        user, created = User.objects.update_or_create(
            email=validated_data['email'],
            defaults={
                'username': validated_data.get('username'),
                'phone': validated_data.get('phone'),
                'is_active': False
            }
        )
        if created:
            user.set_password(validated_data['password'])

        user.save()
        return user

    def update(self, user, validated_data):
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Изменение данных пользователя"""

    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        if obj.profile.avatar:
            return get_absolute_uri(self.context['request'], obj.profile.avatar.url)

    class Meta:
        model = User
        fields = ('email', 'username', 'phone', 'avatar')
        read_only_fields = ('email', 'avatar')


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """Получение токенов доступа"""

    email = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, attrs: dict) -> dict:
        self.instance = authenticate(
            self.context.get("request"),
            email=attrs["email"],
            code=attrs["code"],
        )
        if self.instance:
            self.instance.is_active = True
            self.instance.save(update_fields=['is_active'])
            profile, _ = Profile.objects.get_or_create(user=self.instance)

        if self.instance is None or not self.instance.is_active:
            raise AuthenticationFailed("Неверный email или код")

        token = RefreshToken.for_user(self.instance)
        data = {"refresh": str(token), "access": str(token.access_token)}
        data.update(UserSerializer(self.instance, context={'request': self.context.get('request')}).data)
        return data


class ResetPasswordSerializer(serializers.Serializer):
    """Сброс пароля"""
    email = serializers.EmailField(required=True)
