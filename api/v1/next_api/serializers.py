from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.services import get_absolute_uri
from apps.salon.models import Salon, SalonImg, Specialist, Sale, \
    Messenger, MessengerType, MobileAppSection, Store, AppReasons, Ceo, HeadScript, WorkImg
from apps.service.models import ServiceCategory, Service, AddServiceImg

User = get_user_model()


class MessengerTypeSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для изображений салона"""

    img = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

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

    img = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

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
    """Класс сериалайзер для изображений специалиста"""

    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if obj.photo:
            return get_absolute_uri(self.context['request'], obj.photo.url)

    class Meta:
        model = Specialist
        fields = ['id', 'name', 'photo', 'position', 'experience', 'title',
                  'text', 'services']


class WorkImgSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для специалиста"""

    img = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

    class Meta:
        model = WorkImg
        fields = ['id', 'name', 'img']


class SpecialistRetrieveSerializer(SpecialistSerializer):
    """Класс сериалайзер для специалиста"""
    work_imgs = WorkImgSerializer(many=True)

    class Meta:
        model = Specialist
        fields = ['id', 'name', 'photo', 'position', 'experience', 'title',
                  'text', 'work_imgs']


class SaleSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для акции"""

    img = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

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
    salon_imgs = SalonImgSerializer(many=True)

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

    img = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

    class Meta:
        model = AddServiceImg
        fields = ['id', 'img']


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Класс сериалайзер для категории услуг"""

    services = ServiceSerializer(many=True)
    service_imgs = ServiceImgSerializer(many=True)
    slug = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'img', 'service_imgs', 'title', 'text', 'services', 'slug']

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

    def get_slug(self, obj):
        if not obj.slug:
            return str(obj.id)
        return obj.slug


class ServiceDetailCategorySerializer(ServiceCategorySerializer):
    specialists = SpecialistSerializer(many=True)
    service_imgs = ServiceImgSerializer(many=True)
    img = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'img', 'service_imgs', 'title', 'text', 'services',
                  'slug', 'specialists']


class StoreSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для секции мобильного приложения"""

    img = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

    class Meta:
        model = Store
        fields = ['id', 'name', 'img', 'link']


class ReasonSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для плюсов приложения"""

    img = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

    class Meta:
        model = AppReasons
        fields = ['id', 'title', 'img', 'text']


class MobileAppSectionSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для секции мобильного приложения"""

    stores = StoreSerializer(many=True)
    reasons = ReasonSerializer(many=True)
    img = serializers.SerializerMethodField()
    img_for_section = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

    def get_img_for_section(self, obj):
        if obj.img_for_section:
            return get_absolute_uri(self.context['request'], obj.img_for_section.url)

    class Meta:
        model = MobileAppSection
        fields = ['title', 'text', 'promo', 'img', 'img_for_section', 'reasons', 'stores']


class HeadScriptSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для скрипта head"""
    class Meta:
        model = HeadScript
        fields = ['name', 'script']


class BodyScriptSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для скрипта body"""

    class Meta:
        model = HeadScript
        fields = ['name', 'script']


class CeoSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для Ceo"""

    head_scripts = HeadScriptSerializer(many=True)
    body_scripts = BodyScriptSerializer(many=True)

    class Meta:
        model = Ceo
        fields = ['head', 'head_scripts', 'body_scripts']
