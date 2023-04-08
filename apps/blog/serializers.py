from rest_framework import serializers

from apps.blog.models import Post
from apps.salon.models import Faq


class PostSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url).replace('http', 'https')

    class Meta:
        model = Post
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = '__all__'
