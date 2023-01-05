from django.db.models import Prefetch, Avg
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
        salons = Salon.objects.filter(is_publish=True)\
            .annotate(avg_rating=Avg('salon_reviews__rating')).all()
        data['salons'] = SalonListSerializer(salons, many=True).data
        company = CompanyInfo.objects.filter(is_publish=True).first()
        data['company'] = CompanyInfoSerializer(company).data

        if salon_id := request.GET.get('salon'):

            salon = Salon.objects.filter(id=salon_id, is_publish=True) \
                .prefetch_related(
                    Prefetch(
                        'salon_imgs',
                        queryset=SalonImg.objects.filter(is_main=True)
                    )
                ).prefetch_related(
                    Prefetch(
                        'specialists',
                        queryset=Specialist.objects.filter(is_publish=True).prefetch_related('work_imgs')
                    )
                ).prefetch_related(
                    Prefetch(
                        'sales',
                        queryset=Sale.objects.filter(is_publish=True)
                    )
                ).prefetch_related(
                    Prefetch(
                        'salon_reviews',
                        queryset=Review.objects.filter(is_publish=True)
                    )
                ).first()

            categories = ServiceCategory.objects.filter(is_publish=True).prefetch_related(
                Prefetch(
                    'services',
                    queryset=Service.objects.filter(salons=salon_id, is_publish=True)
                )
            ).filter(services__salons=salon_id).distinct()

            salon_data = SalonSerializer(salon).data
            salon_data['service_categories'] = ServiceCategorySerializer(categories, many=True).data
            salon_data.update(data)

            return Response(salon_data)

        return Response(data)
