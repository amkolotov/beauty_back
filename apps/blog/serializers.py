from rest_framework import serializers

from apps.blog.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
