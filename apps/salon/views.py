from django.db.models import Prefetch, Avg, Subquery, OuterRef
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.salon.models import Salon, SalonImg, Specialist, Sale, Review, CompanyInfo
from apps.salon.serializers import SalonSerializer, ServiceCategorySerializer, CompanyInfoSerializer, \
    SalonListSerializer
from apps.service.models import Service, ServiceCategory


class MainSalonInfoView(APIView):
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
                        .prefetch_related('work_imgs')\
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
