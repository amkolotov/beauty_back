from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.salon.models import Salon, SalonImg, Specialist, Sale, \
    Messenger, MessengerType, MobileAppSection, Store, AppReasons, Ceo
from apps.service.models import ServiceCategory, Service, AddServiceImg

User = get_user_model()


class MessengerTypeSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для изображений салона"""

    class Meta:
        model = MessengerType
        fields = ['id', 'img', 'is_social']


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


class SalonFooterSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для footera"""
    salon_messengers = SalonMessengersSerializer(many=True)

    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'email', 'phone', 'work_time',
                  'salon_messengers', 'slug']

    def get_slug(self, obj):
        if not obj.slug:
            return str(obj.id)
        return obj.slug


class SalonListSerializer(SalonFooterSerializer):
    """Класс сериалайзер для списка салонов"""

    salon_imgs = SalonImgSerializer(many=True)
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'email', 'phone', 'salon_imgs', 'work_time',
                  'coords', 'short_desc', 'desc', 'salon_messengers', 'slug']


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


class SalonHomeSerializer(serializers.ModelSerializer):
    """Класс сериалайзер салона для домашней страницы"""

    salon_imgs = SalonImgSerializer(many=True)
    sales = SaleSerializer(many=True)
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'phone', 'email', 'short_desc', 'desc',
                  'work_time', 'coords', 'salon_imgs', 'sales', 'slug']

    def get_slug(self, obj):
        if not obj.slug:
            return str(obj.id)
        return obj.slug


class SalonSerializer(SalonHomeSerializer):
    """Класс сериалайзер для салона"""

    specialists = SpecialistSerializer(many=True)

    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'phone', 'email', 'short_desc', 'desc',
                  'work_time', 'coords', 'salon_imgs', 'specialists', 'sales', 'slug']


class ServiceSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для услуги"""

    class Meta:
        model = Service
        fields = ['id', 'name', 'price']


class ServiceImgSerializer(serializers.ModelSerializer):

    """Сериализатор для изображения услуги"""
    class Meta:
        model = AddServiceImg
        fields = ['id', 'img']


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Класс сериалайзер для категории услуг"""

    services = ServiceSerializer(many=True)
    service_imgs = ServiceImgSerializer(many=True)
    slug = serializers.SerializerMethodField()

    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'img', 'service_imgs', 'title', 'text', 'services', 'slug']

    def get_slug(self, obj):
        if not obj.slug:
            return str(obj.id)
        return obj.slug


class StoreSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для секции мобильного приложения"""
    class Meta:
        model = Store
        fields = ['id', 'name', 'img', 'link']


class ReasonSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для плюсов приложения"""
    class Meta:
        model = AppReasons
        fields = ['id', 'title', 'img', 'text']


class MobileAppSectionSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для секции мобильного приложения"""

    stores = StoreSerializer(many=True)
    reasons = ReasonSerializer(many=True)

    class Meta:
        model = MobileAppSection
        fields = ['title', 'text', 'promo', 'img', 'img_for_section', 'reasons', 'stores']


class CeoSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для CEO"""

    class Meta:
        model = Ceo
        fields = ['head', 'body']
