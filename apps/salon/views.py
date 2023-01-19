from django.db.models import Prefetch, Avg, Subquery, OuterRef, Case, When, Value, BooleanField, Q
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from api.v1.views import BaseGenericAPIView
from apps.auth_app.throttles import TokenObtainThrottle
from apps.salon.models import Salon, SalonImg, Specialist, Sale, Review, CompanyInfo, Order, Notification, Messenger
from apps.salon.serializers import SalonSerializer, ServiceCategorySerializer, CompanyInfoSerializer, \
    SalonListSerializer, ReviewSerializer, OrderSerializer, NotificationSerializer, SalonMessengersSerializer
from apps.service.models import Service, ServiceCategory


class MainSalonInfoView(BaseGenericAPIView):
    """Возвращает информацию для главной страницы"""

    def get(self, request):
        data = {}
        messengers_subquery = Subquery(Messenger.objects \
                                       .filter(salon_id=OuterRef('salon_id'), is_publish=True) \
                                       .values_list('id', flat=True))

        salons = Salon.objects.filter(is_publish=True) \
            .annotate(avg_rating=Avg('salon_reviews__rating')) \
            .prefetch_related(
            Prefetch(
                'salon_imgs',
                queryset=SalonImg.objects.filter(is_main=True, is_publish=True)
            )
        ).prefetch_related(
            Prefetch(
                'salon_messengers',
                queryset=Messenger.objects.filter(id__in=messengers_subquery)
            )).all()
        data['salons'] = SalonListSerializer(
            salons, many=True, context={'request': request}
        ).data

        company = CompanyInfo.objects.filter(is_publish=True).first()
        data['company'] = CompanyInfoSerializer(company, context={'request': request}).data

        data['company']['messengers'] = SalonMessengersSerializer(
            Messenger.objects.filter(for_company=True, is_publish=True), many=True, context={'request': request}
        ).data

        if salon_id := request.GET.get('salon'):
            review_subqery = Subquery(Review.objects \
                                      .filter(salon_id=OuterRef('salon_id'), is_publish=True, spec__isnull=True) \
                                      .values_list('id', flat=True)[:3])
            review_spec_subqery = Subquery(Review.objects \
                                           .filter(is_publish=True, salon_id=salon_id) \
                                           .values_list('id', flat=True)[:3])

            salon = Salon.objects.filter(id=salon_id, is_publish=True) \
                .prefetch_related(
                Prefetch(
                    'salon_imgs',
                    queryset=SalonImg.objects.filter(is_main=True)
                )
            ).prefetch_related(
                Prefetch(
                    'specialists',
                    queryset=Specialist.objects.filter(is_publish=True) \
                        .annotate(avg_rating=Avg('spec_reviews__rating'))
                        .prefetch_related('work_imgs') \
                        .prefetch_related(
                        Prefetch(
                            'spec_reviews',
                            queryset=Review.objects.filter(id__in=review_spec_subqery)
                        )
                    )
                )
            ).prefetch_related(
                Prefetch(
                    'sales',
                    queryset=Sale.objects.filter(is_publish=True)
                )
            ).prefetch_related(
                Prefetch(
                    'salon_reviews',
                    queryset=Review.objects.filter(id__in=review_subqery)
                )
            ).first()

            categories = ServiceCategory.objects.filter(is_publish=True).prefetch_related(
                Prefetch(
                    'services',
                    queryset=Service.objects.filter(salons=salon_id, is_publish=True)
                )
            ).filter(services__salons=salon_id).distinct()

            salon_data = SalonSerializer(salon, context={'request': request}).data
            salon_data['service_categories'] = ServiceCategorySerializer(
                categories, many=True, context={'request': request}
            ).data
            salon_data.update(data)

            return Response(salon_data)

        return Response(data)


class ReviewViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    viewsets.GenericViewSet, BaseGenericAPIView):
    """Вьюсет отзывов"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TokenObtainThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.save()

        return Response({'status': 'success'})

    def get_queryset(self):
        queryset = super().get_queryset()
        if salon_id := self.request.GET.get('salon'):
            return queryset.filter(spec__isnull=True, salon_id=salon_id)
        elif spec_id := self.request.GET.get('spec'):
            return queryset.filter(spec_id=spec_id)


class OrderViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   viewsets.GenericViewSet, BaseGenericAPIView):
    """Вьюсет заявок"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    throttle_classes = [TokenObtainThrottle]

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class NotificationViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin,
                          viewsets.GenericViewSet, BaseGenericAPIView):
    """Вьюсет уведомлений"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    throttle_classes = [TokenObtainThrottle]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(is_publish=True, created_at__gt=self.request.user.created_at)\
            .filter(Q(for_salon=self.request.user.profile.salon) | Q(for_users=self.request.user) | Q(for_all=True))\
            .annotate(is_read=Case(
                When(read=self.request.user, then=True),
                default=False,
                output_field=BooleanField())
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['unread_count'] = self.get_queryset().exclude(is_read=True).count()
        return response

    def update(self, request, *args, **kwargs):
        notification_id = kwargs.get('pk')
        if Notification.objects.filter(id=notification_id).exists():
            notification = Notification.objects.get(id=notification_id)
            notification.read.add(request.user)
            count = Notification.objects.filter(
                is_publish=True, created_at__gt=self.request.user.created_at)\
                .exclude(read=request.user).count()
            return Response({'unread_count': count})
        return Response(status=HTTP_404_NOT_FOUND)
