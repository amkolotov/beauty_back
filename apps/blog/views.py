from rest_framework import viewsets, mixins

from apps.blog.models import Post
from apps.blog.serializers import PostSerializer


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Вьюсет постов"""
    serializer_class = PostSerializer
    queryset = Post.objects.all()
