from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.services import get_absolute_uri
from apps.salon.models import Salon, SalonImg, Specialist, Sale, Review, WorkImg, \
    CompanyInfo, Notification, Order, Messenger, MessengerType, Faq, ConfInfo
from apps.service.models import ServiceCategory, Service
from apps.auth_app.validators import validate_phone as phone_validator

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


class SalonListSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для списка салонов"""

    salon_imgs = SalonImgSerializer(many=True)
    avg_rating = serializers.FloatField()
    salon_messengers = SalonMessengersSerializer(many=True)

    class Meta:
        model = Salon
        fields = ['id', 'name', 'address', 'email', 'phone', 'work_time', 'salon_imgs',
                  'coords', 'salon_messengers', 'avg_rating']


class WorkImgSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для специалиста"""

    class Meta:
        model = WorkImg
        fields = ['id', 'name', 'img']


class ReviewSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для акции"""

    username = serializers.CharField(source='user.username', required=False)
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ['id', 'username', 'user', 'rating', 'text', 'spec', 'salon', 'created_at']
        read_only_fields = ['id', 'username', 'created_at']


class SpecialistSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для изображений салона"""

    work_imgs = WorkImgSerializer(many=True)
    spec_reviews = ReviewSerializer(many=True)
    avg_rating = serializers.FloatField()

    class Meta:
        model = Specialist
        fields = ['id', 'name', 'photo', 'position', 'experience', 'title', 'is_manager',
                  'text', 'services', 'work_imgs', 'spec_reviews', 'avg_rating']


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
        fields = ['id', 'name', 'address', 'phone', 'short_desc', 'desc', 'work_time', 'salon_imgs',
                  'coords', 'specialists', 'sales', 'salon_reviews']


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

    logo = serializers.SerializerMethodField()
    logo_black = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()
    about_img = serializers.SerializerMethodField()

    def get_logo(self, obj):
        if obj.logo:
            return get_absolute_uri(self.context['request'], obj.logo.url)

    def get_logo_black(self, obj):
        if obj.logo_black:
            return get_absolute_uri(self.context['request'], obj.logo_black.url)

    def get_img(self, obj):
        if obj.img:
            return get_absolute_uri(self.context['request'], obj.img.url)

    def get_about_img(self, obj):
        if obj.about_img:
            return get_absolute_uri(self.context['request'], obj.about_img.url)

    class Meta:
        model = CompanyInfo
        exclude = ['is_publish']


class OrderSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для заявки"""
    user = serializers.PrimaryKeyRelatedField(
        default=None, queryset=User.objects.all(),
    )
    salon_name = serializers.CharField(source='salon.name', required=False)
    service_name = serializers.CharField(source='service.name', required=False)
    spec_name = serializers.CharField(source='spec.name', required=False)
    source = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = ['user', 'name', 'phone', 'salon', 'service', 'spec', 'comment',
                  'salon_name', 'service_name', 'spec_name', 'date', 'status', 'source']
        read_only_fields = ['status', 'service_name', 'salon_name', 'spec_name']
        extra_kwargs = {"comment": {"write_only": True, }}

    def validate_phone(self, value):
        return phone_validator(value)


class NotificationSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для уведомления"""
    is_read = serializers.BooleanField(default=False)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'text', 'is_read', 'created_at']


class FaqSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для faq"""

    class Meta:
        model = Faq
        fields = '__all__'


class ConfInfoSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для политики конфиденциальности"""

    class Meta:
        model = ConfInfo
        fields = '__all__'
