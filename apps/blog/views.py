from rest_framework import viewsets, mixins

from apps.blog.models import Post
from apps.blog.serializers import PostSerializer
from apps.salon.paginator import NotificationPagination


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Вьюсет постов"""
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_publish=True)
    pagination_class = NotificationPagination
