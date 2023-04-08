from rest_framework import serializers

from api.services import get_absolute_uri
from apps.blog.models import Post
from apps.salon.models import Faq


class PostSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return get_absolute_uri(self.context['request'], obj.image.url)

    class Meta:
        model = Post
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = '__all__'
