from rest_framework import serializers

from apps.salon.models import Salon, SalonImg, Specialist, Sale, Review, WorkImg, CompanyInfo
from apps.service.models import ServiceCategory, Service


class SalonImgSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для специалиста"""

    class Meta:
        model = SalonImg
        fields = ['id', 'img', 'is_main']


class SalonListSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для списка салонов"""

    salon_imgs = SalonImgSerializer(many=True)
    avg_rating = serializers.FloatField()

    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'salon_imgs', 'avg_rating']


class WorkImgSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для специалиста"""

    class Meta:
        model = WorkImg
        fields = ['id', 'name', 'img']


class ReviewSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для акции"""

    username = serializers.CharField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'username', 'rating', 'text', 'text', 'spec', 'salon', 'created_at']


class SpecialistSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для изображений салона"""

    work_imgs = WorkImgSerializer(many=True)
    spec_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Specialist
        fields = ['id', 'name', 'photo', 'position', 'experience', 'title',
                  'text', 'services', 'work_imgs', 'spec_reviews']


class SaleSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для акции"""

    class Meta:
        model = Sale
        fields = ['id', 'title', 'desc', 'text', 'button_text', 'img']


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
        fields = ['id', 'name', 'img', 'title', 'text', 'services']


class CompanyInfoSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для компании"""

    class Meta:
        model = CompanyInfo
        exclude = ['is_publish']
