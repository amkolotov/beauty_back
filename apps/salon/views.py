from django.db.models import Prefetch, Avg, Subquery, OuterRef, Case, When, Value, BooleanField
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from api.v1.views import BaseGenericAPIView
from apps.auth_app.throttles import TokenObtainThrottle
from apps.salon.models import Salon, SalonImg, Specialist, Sale, Review, CompanyInfo, Order, Notification
from apps.salon.serializers import SalonSerializer, ServiceCategorySerializer, CompanyInfoSerializer, \
    SalonListSerializer, ReviewSerializer, OrderSerializer, NotificationSerializer
from apps.service.models import Service, ServiceCategory


class MainSalonInfoView(BaseGenericAPIView):
    """Возвращает информацию для главной страницы"""

    def get(self, request):
        data = {}
        salons = Salon.objects.filter(is_publish=True) \
            .annotate(avg_rating=Avg('salon_reviews__rating')) \
            .prefetch_related(
            Prefetch(
                'salon_imgs',
                queryset=SalonImg.objects.filter(is_main=True)
            )).all()
        data['salons'] = SalonListSerializer(
            salons, many=True, context={'request': request}
        ).data

        company = CompanyInfo.objects.filter(is_publish=True).first()
        data['company'] = CompanyInfoSerializer(company, context={'request': request}).data

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


class ReviewCreateApiView(BaseGenericAPIView):
    """Создание нового отзыва"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TokenObtainThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(source=kwargs['slug'])
        instance.save()

        return Response({'status': 'success'})


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


class NotificationViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin,
                          viewsets.GenericViewSet, BaseGenericAPIView):
    """Вьюсет уведомлений"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    throttle_classes = [TokenObtainThrottle]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(is_publish=True)\
            .annotate(is_read=Case(
                When(read=self.request.user, then=True),
                default=False,
                output_field=BooleanField())
        )

    def update(self, request, *args, **kwargs):
        notification_id = kwargs.get('pk')
        if Notification.objects.filter(id=notification_id).exists():
            notification = Notification.objects.get(id=notification_id)
            notification.read.add(request.user)
            return Response({'status': 'success'})
        return Response(status=HTTP_404_NOT_FOUND)
