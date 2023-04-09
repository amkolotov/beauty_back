from django.db.models import Subquery, OuterRef, Prefetch
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from api.v1.next_api.paginator import PostPagination, SalePagination
from api.v1.views import BaseGenericAPIView
from apps.blog.models import Post
from apps.blog.serializers import PostSerializer
from apps.salon.models import Messenger, Salon, SalonImg, CompanyInfo, Specialist, Sale, MobileAppSection, Faq, Ceo
from apps.salon.serializers import CompanyInfoSerializer, FaqSerializer

from apps.service.models import ServiceCategory, Service, AddServiceImg
from api.v1.next_api.serializers import SalonListSerializer, SalonMessengersSerializer, SalonHomeSerializer, \
    ServiceCategorySerializer, MobileAppSectionSerializer, CeoSerializer, SalonFooterSerializer, SalonSerializer, \
    SaleSerializer, ServiceDetailCategorySerializer


class HomeView(BaseGenericAPIView):
    """Возвращает информацию для главной страницы сайта"""

    def get(self, request):
        data = {}
        company = CompanyInfo.objects.filter(is_publish=True).first()
        data['company'] = CompanyInfoSerializer(company, context={'request': request}).data

        if request.GET.get('salon'):
            salon_slug = request.GET.get('salon')
        else:
            salon_slug = Salon.objects.filter(is_publish=True).first().slug

        salon = Salon.objects.filter(slug=salon_slug, is_publish=True).first()

        categories = ServiceCategory.objects.filter(is_publish=True).prefetch_related(
            Prefetch(
                'services',
                queryset=Service.objects.filter(salons=salon, is_publish=True)
            )).prefetch_related(
            Prefetch(
                'service_imgs',
                queryset=AddServiceImg.objects.all()
            )).filter(services__salons=salon).distinct()

        salon_data = SalonHomeSerializer(salon, context={'request': request}).data
        salon_data['service_categories'] = ServiceCategorySerializer(
            categories, many=True, context={'request': request}
        ).data
        salon_data.update(data)

        app_section = MobileAppSection.objects.filter(is_publish=True) \
            .prefetch_related('stores').first()
        salon_data['app_section'] = MobileAppSectionSerializer(
            app_section, context={'request': request}
        ).data

        posts = Post.objects.filter(is_publish=True)[:4]
        salon_data['posts'] = PostSerializer(
            posts, many=True, context={'request': request}
        ).data

        faqs = Faq.objects.filter(is_publish=True)[:4]
        salon_data['faqs'] = FaqSerializer(faqs, many=True).data

        ceo = Ceo.objects.first()
        if ceo:
            data['ceo'] = CeoSerializer(ceo).data

        return Response(salon_data)


class SalonsView(generics.RetrieveAPIView):
    queryset = Salon.objects.filter(is_publish=True) \
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
    ).all()
    serializer_class = SalonSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        company = CompanyInfo.objects.filter(is_publish=True).first()
        response.data['company'] = CompanyInfoSerializer(company, context={'request': request}).data
        app_section = MobileAppSection.objects.filter(is_publish=True) \
            .prefetch_related('stores').first()
        response.data['app_section'] = MobileAppSectionSerializer(
            app_section, context={'request': request}
        ).data
        categories = ServiceCategory.objects.filter(is_publish=True).prefetch_related(
            Prefetch(
                'services',
                queryset=Service.objects.filter(salons__slug=kwargs.get('slug'), is_publish=True)
            )).prefetch_related(
            Prefetch(
                'service_imgs',
                queryset=AddServiceImg.objects.all()
            )).filter(services__salons__slug=kwargs.get('slug')).distinct()
        response.data['service_categories'] = ServiceCategorySerializer(
            categories, many=True, context={'request': request}
        ).data

        return response


class ContactsView(BaseGenericAPIView):
    """Возвращает контактную"""

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

        app_section = MobileAppSection.objects.filter(is_publish=True) \
            .prefetch_related('stores').first()
        data['app_section'] = MobileAppSectionSerializer(
            app_section, context={'request': request}
        ).data

        ceo = Ceo.objects.first()
        if ceo:
            data['ceo'] = CeoSerializer(ceo).data

        return Response(data)


class AboutView(BaseGenericAPIView):
    """Возвращает информацию для страницы о нас"""

    def get(self, request):
        data = {}
        salons = Salon.objects.filter(is_publish=True) \
            .prefetch_related(
            Prefetch(
                'salon_imgs',
                queryset=SalonImg.objects.filter(is_main=True, is_publish=True)
            )
        ).all()
        data['salons'] = SalonListSerializer(
            salons, many=True, context={'request': request}
        ).data

        company = CompanyInfo.objects.filter(is_publish=True).first()
        data['company'] = CompanyInfoSerializer(company, context={'request': request}).data

        faqs = Faq.objects.filter(is_publish=True)[:4]
        data['faqs'] = FaqSerializer(faqs, many=True).data

        ceo = Ceo.objects.first()
        if ceo:
            data['ceo'] = CeoSerializer(ceo).data

        return Response(data)


class ServiceView(BaseGenericAPIView):
    """Возвращает информацию для страницы услуги"""

    def get(self, request, *args, **kwargs):

        if salon_slug := kwargs.get('salon_slug'):
            salon = Salon.objects.filter(slug=salon_slug).first()
            if kwargs.get('service_slug') and salon:
                service_slug = kwargs.get('service_slug')
                categories = ServiceCategory.objects.filter(is_publish=True).prefetch_related(
                    Prefetch(
                        'services',
                        queryset=Service.objects.filter(salons=salon, is_publish=True)
                    )).prefetch_related(
                        Prefetch(
                            'specialists',
                            queryset=Specialist.objects.filter(is_publish=True)
                        )
                    ).prefetch_related(
                        Prefetch(
                            'service_imgs',
                            queryset=AddServiceImg.objects.all()
                        )).filter(services__salons=salon).distinct()
                category = categories.filter(slug=service_slug).first()
                if category:
                    data = ServiceDetailCategorySerializer(
                        category, context={'request': request}
                    ).data
                    data['service_categories'] = ServiceCategorySerializer(
                        categories, many=True, context={'request': request}
                    ).data
                    app_section = MobileAppSection.objects.filter(is_publish=True) \
                        .prefetch_related('stores').first()
                    data['app_section'] = MobileAppSectionSerializer(
                        app_section, context={'request': request}
                    ).data

                    data['salon'] = {
                        'salon_name': salon.name,
                        'salon_id': salon.id,
                        'salon_slug': salon.slug
                    }

                    return Response(data)

        return Response(status=HTTP_404_NOT_FOUND)


class FooterView(BaseGenericAPIView):
    """Возвращает информацию для футера"""

    def get(self, request):

        if request.GET.get('salon'):
            salon_slug = request.GET.get('salon')
        else:
            salon_slug = Salon.objects.filter(is_publish=True).first().slug

        messengers_subquery = Subquery(Messenger.objects
                                       .filter(salon_id=OuterRef('salon_id'), is_publish=True)
                                       .values_list('id', flat=True))

        salon = Salon.objects.filter(is_publish=True, slug=salon_slug) \
            .prefetch_related(
            Prefetch(
                'salon_messengers',
                queryset=Messenger.objects.filter(id__in=messengers_subquery)
            )).first()

        salon_data = SalonFooterSerializer(salon, context={'request': request}).data

        company = CompanyInfo.objects.filter(is_publish=True).first()
        salon_data['company'] = CompanyInfoSerializer(company, context={'request': request}).data

        app_section = MobileAppSection.objects.filter(is_publish=True) \
            .prefetch_related('stores').first()
        salon_data['app_section'] = MobileAppSectionSerializer(
            app_section, context={'request': request}
        ).data

        return Response(salon_data)


class SaleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет акций"""
    serializer_class = SaleSerializer
    pagination_class = SalePagination

    def get_queryset(self):
        if slug := self.request.GET.get('salon'):
            salon = Salon.objects.filter(is_publish=True, slug=slug).first()
        else:
            salon = Salon.objects.filter(is_publish=True).first()
        return Sale.objects.filter(is_publish=True, salons=salon)


class PostSiteViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Вьюсет постов"""
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_publish=True)
    pagination_class = PostPagination


class FaqSiteViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Вьюсет faqs"""
    serializer_class = FaqSerializer
    queryset = Faq.objects.filter(is_publish=True)
    pagination_class = PostPagination


class CeoView(BaseGenericAPIView):
    """Возвращает ceo"""

    def get(self, request):
        ceo = Ceo.objects.first()
        if ceo:
            return Response(CeoSerializer(ceo).data)
        return Response(status=HTTP_204_NO_CONTENT)
