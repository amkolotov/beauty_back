from rest_framework import pagination


class PostPagination(pagination.PageNumberPagination):
    page_size = 4
