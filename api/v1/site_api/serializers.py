from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.salon.models import Salon, SalonImg, Specialist, Sale, Review, WorkImg, \
    CompanyInfo, Notification, Order, Messenger, MessengerType, MobileAppSection, Store
from apps.service.models import ServiceCategory, Service

User = get_user_model()


class MessengerTypeSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для изображений салона"""

    class Meta:
        model = MessengerType
        fields = ['id', 'img']


class SalonMessengersSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для мессенджера"""

    type = MessengerTypeSerializer()

    class Meta:
        model = Messenger
        exclude = ['salon', 'for_company', 'is_publish', 'created_at', 'updated_at']


class SalonImgSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для изображений салона"""

    class Meta:
        model = SalonImg
        fields = ['id', 'img', 'is_main']


class SalonListSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для списка салонов"""

    salon_imgs = SalonImgSerializer(many=True)
    salon_messengers = SalonMessengersSerializer(many=True)

    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'email', 'phone', 'salon_imgs',
                  'salon_messengers']


class SpecialistSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для изображений салона"""

    class Meta:
        model = Specialist
        fields = ['id', 'name', 'photo', 'position', 'experience', 'title',
                  'text', 'services']


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

    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'phone', 'email', 'desc', 'salon_imgs',
                  'specialists', 'sales']


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
        fields = ['id', 'name', 'img', 'service_imgs', 'title', 'text', 'services']


class StoreSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для секции мобильного приложения"""
    class Meta:
        model = Store
        fields = ['id', 'name', 'img', 'link']


class MobileAppSectionSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для секции мобильного приложения"""

    stores = StoreSerializer(many=True)

    class Meta:
        model = MobileAppSection
        fields = ['title', 'text', 'promo', 'img', 'img_for_section', 'stores']
