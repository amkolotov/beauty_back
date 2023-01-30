from django.db.models import Subquery, OuterRef, Prefetch
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from api.v1.site_api.paginator import PostPagination
from api.v1.views import BaseGenericAPIView
from apps.blog.models import Post
from apps.blog.serializers import PostSerializer
from apps.salon.models import Messenger, Salon, SalonImg, CompanyInfo, Specialist, Sale, MobileAppSection, Faq
from apps.salon.serializers import CompanyInfoSerializer, FaqSerializer

from apps.service.models import ServiceCategory, Service, AddServiceImg
from api.v1.site_api.serializers import SalonListSerializer, SalonMessengersSerializer, SalonSerializer, \
    ServiceCategorySerializer, MobileAppSectionSerializer


class SiteMainSalonInfoView(BaseGenericAPIView):
    """Возвращает информацию для главной страницы сайта"""

    def get(self, request):
        data = {}
        messengers_subquery = Subquery(Messenger.objects
                                       .filter(salon_id=OuterRef('salon_id'), is_publish=True)
                                       .values_list('id', flat=True))

        salons = Salon.objects.filter(is_publish=True) \
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
            Messenger.objects.filter(for_company=True, is_publish=True), many=True,
            context={'request': request}
        ).data

        if request.GET.get('salon'):
            salon_id = request.GET.get('salon')
        else:
            salon_id = Salon.objects.filter(is_publish=True).first().id

        salon = Salon.objects.filter(id=salon_id, is_publish=True) \
            .prefetch_related(
            Prefetch(
                'salon_imgs',
                queryset=SalonImg.objects.filter(is_publish=True)
            )
        ).prefetch_related(
            Prefetch(
                'specialists',
                queryset=Specialist.objects.filter(is_publish=True)
            )
        ).prefetch_related(
            Prefetch(
                'sales',
                queryset=Sale.objects.filter(is_publish=True)
            )
        ).first()

        categories = ServiceCategory.objects.filter(is_publish=True).prefetch_related(
            Prefetch(
                'services',
                queryset=Service.objects.filter(salons=salon_id, is_publish=True)
            )).prefetch_related(
            Prefetch(
                'service_imgs',
                queryset=AddServiceImg.objects.all()
            )).filter(services__salons=salon_id).distinct()

        salon_data = SalonSerializer(salon, context={'request': request}).data
        salon_data['service_categories'] = ServiceCategorySerializer(
            categories, many=True, context={'request': request}
        ).data
        salon_data.update(data)

        app_section = MobileAppSection.objects.filter(is_publish=True)\
            .prefetch_related('stores').first()
        salon_data['app_section'] = MobileAppSectionSerializer(
            app_section, context={'request': request}
        ).data

        posts = Post.objects.filter(is_publish=True)[:8]
        salon_data['posts'] = PostSerializer(
            posts, many=True, context={'request': request}
        ).data

        faqs = Faq.objects.filter(is_publish=True)[:4]
        salon_data['faqs'] = FaqSerializer(faqs, many=True).data

        return Response(salon_data)


class PostSiteViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Вьюсет постов"""
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_publish=True)
    pagination_class = PostPagination
