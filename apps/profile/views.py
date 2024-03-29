from django.contrib.auth import get_user_model
from django.db.models import Q
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
            instance = serializer.save()
            return Response({'avatar': request.build_absolute_uri(instance.avatar.url).replace('http', 'https')},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUserDataView(UpdateAPIView):
    """Изменение данных пользователя"""
    queryset = User.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RemovePushTokenView(BaseGenericAPIView):
    """Удаление пуш токена"""
    def post(self, request, user_id):
        if User.objects.filter(id=user_id).exists():
            user = User.objects.get(id=user_id)
            user.profile.expo_token = None
            user.profile.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetUserDataView(BaseGenericAPIView):
    """Получение данных пользователя"""
    queryset = User.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.queryset.filter(id=request.user.id).first()
        data = self.get_serializer(user, context={'request': request}).data
        if salon_id := self.request.GET.get('salon'):
            data['unread_count'] = Notification.objects.filter(
                is_publish=True, created_at__gt=self.request.user.created_at
            ) \
                .filter(Q(for_users=self.request.user) | Q(for_salons=salon_id) \
                        | Q(for_users=None, for_salons=None, for_all=True)) \
                .order_by('-id') \
                .distinct('id') \
                .exclude(read=request.user).\
                count()
        else:
            data['unread_count'] = Notification.objects.filter(
                is_publish=True, created_at__gt=self.request.user.created_at
            ) \
                .filter(Q(for_users=self.request.user) | Q(for_users=None, for_salons=None, for_all=True)) \
                .order_by('-id') \
                .distinct('id') \
                .exclude(read=request.user)\
                .count()
        return Response(data)
