from django.contrib.auth import get_user_model
from django.db.models import Case, When, BooleanField, Prefetch, Subquery
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.views import GenericAPIView, BaseGenericAPIView

from apps.profile.serializers import ProfileAvatarSerializer, UserDataSerializer
from apps.salon.models import Order, Notification
from apps.salon.serializers import NotificationSerializer

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
        orders_subqery = Subquery(Order.objects.filter(user=self.request.user)
                                  .values_list('id', flat=True)[:10])
        user = self.queryset.filter(id=request.user.id) \
            .prefetch_related(
            Prefetch(
                'orders',
                queryset=Order.objects.filter(id__in=orders_subqery)
            )).first()
        data = self.get_serializer(user).data

        notifications = Notification.objects.filter(is_publish=True) \
            .annotate(is_read=Case(
                When(read=request.user, then=True),
                default=False,
                output_field=BooleanField())
            )[:10]
        data['notifications'] = NotificationSerializer(notifications, many=True).data

        return Response(data)
