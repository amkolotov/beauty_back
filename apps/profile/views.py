from django.contrib.auth import get_user_model
from django.db.models import Case, When, BooleanField, Prefetch, Subquery
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.views import GenericAPIView, BaseGenericAPIView

from apps.profile.serializers import ProfileAvatarSerializer, UserDataSerializer
from apps.salon.models import Notification

User = get_user_model()


class ProfileAvatarView(GenericAPIView):
    """View профиля пользователя"""
    serializer_class = ProfileAvatarSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user.profile)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUserDataView(UpdateAPIView):
    """Изменение данных пользователя"""
    queryset = User.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class GetUserDataView(BaseGenericAPIView):
    """Получение данных пользователя"""
    queryset = User.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.queryset.filter(id=request.user.id).first()
        data = self.get_serializer(user).data
        data['unread_count'] = Notification.objects.filter(
            is_publish=True, created_at__gt=self.request.user.created_at)\
            .exclude(read=request.user).count()
        return Response(data)
