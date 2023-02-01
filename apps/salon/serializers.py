from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.salon.models import Salon, SalonImg, Specialist, Sale, Review, WorkImg, \
    CompanyInfo, Notification, Order, Messenger, MessengerType, Faq
from apps.service.models import ServiceCategory, Service

c


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

    class Meta:
        model = Order
        fields = ['user', 'name', 'phone', 'salon', 'service', 'spec',
                  'salon_name', 'service_name', 'spec_name', 'date', 'status']
        read_only_fields = ['status', 'service_name', 'salon_name', 'spec_name']


class NotificationSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для уведомления"""
    is_read = serializers.BooleanField(default=False)

    class Meta:
        model = Notification
        fields = ['id', 'text', 'is_read', 'created_at']


class FaqSerializer(serializers.ModelSerializer):
    """Класс сериалайзер для faq"""
    class Meta:
        model = Faq
        fields = '__all__'
