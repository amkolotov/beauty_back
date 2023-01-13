from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.views import BaseGenericAPIView
from .models import Code
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, UserSerializer, ResetPasswordSerializer
from .services import send_code
from .throttles import SendCodeThrottle, TokenObtainThrottle, TokenObtainEmailThrottle

User = get_user_model()


class RegisterView(BaseGenericAPIView):
    """Регистрация пользователя"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    throttle_classes = [SendCodeThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        Code.objects.filter(user_id=user.id).delete()
        code = send_code(user)

        retry_after = code.created_at + settings.AUTH_CODE_ISSUE_THRESHOLD

        return Response(
            status=status.HTTP_200_OK,
            headers={"Retry-After": int(retry_after.timestamp())}
        )


class TokenObtainPairFromCodeView(TokenObtainPairView):
    """Получение токена в обмен на авторизационный код"""
    throttle_classes = [TokenObtainThrottle, TokenObtainEmailThrottle]
    serializer_class = CustomTokenObtainPairSerializer


class TokenObtainPairFromLoginView(TokenObtainPairView):
    """Получение токена в обмен на авторизационный код"""
    throttle_classes = [TokenObtainThrottle]
    extra_serializer = UserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(email=request.data['email'])
        user_serializer = self.extra_serializer(user)
        response.data.update(user_serializer.data)
        return response


class ResetPasswordView(BaseGenericAPIView):
    """Отправка кода для смены пароля"""
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer
    throttle_classes = [SendCodeThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.queryset.filter(
            email=request.data.get('email'), is_active=True
        ).first()
        if not user:
            raise ValidationError('Пользователь с указанным адресом не зарегистрирован')
        Code.objects.filter(user_id=user.id).delete()
        send_code(user)
        return Response(status=status.HTTP_200_OK)


class ResetPasswordSetView(BaseGenericAPIView):
    """Установка нового пароля"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        instance = self.queryset.filter(email=request.data.get('email')).first()
        if not instance:
            raise ValidationError('Пользователь с указанным адресом не зарегистрирован')
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
