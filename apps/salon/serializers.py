from rest_framework import serializers

from apps.salon.models import Salon, SalonImg, Specialist, Sale, Review, WorkImg, CompanyInfo
from apps.service.models import ServiceCategory, Service


class SalonListSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для списка салонов"""

    avg_rating = serializers.FloatField()

    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'avg_rating']


class SalonImgSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для специалиста"""

    class Meta:
        model = SalonImg
        fields = ['id', 'img', 'is_main']


class WorkImgSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для специалиста"""

    class Meta:
        model = WorkImg
        fields = ['id', 'name', 'img']


class SpecialistSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для изображений салона"""

    work_imgs = WorkImgSerializer(many=True)

    class Meta:
        model = Specialist
        fields = ['id', 'name', 'photo', 'position', 'experience', 'title',
                  'text', 'services', 'work_imgs']


class SaleSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для акции"""

    class Meta:
        model = Sale
        fields = ['id', 'title', 'desc', 'text', 'img']


class ReviewSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для акции"""

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'text', 'text', 'spec']


class SalonSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для салона"""

    salon_imgs = SalonImgSerializer(many=True)
    specialists = SpecialistSerializer(many=True)
    sales = SaleSerializer(many=True)
    salon_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'phone', 'desc', 'salon_imgs',
                  'specialists', 'sales', 'salon_reviews']
        # depth = 2


class ServiceSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для услуги"""

    class Meta:
        model = Service
        fields = ['id', 'name', 'price']


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Класс сериалайзер для категории услуг"""

    services = ServiceSerializer(many=True)

    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'img', 'services']


class CompanyInfoSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для компании"""

    class Meta:
        model = CompanyInfo
        exclude = ['is_publish']
