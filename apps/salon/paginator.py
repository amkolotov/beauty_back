from rest_framework import pagination


class NotificationPagination(pagination.PageNumberPagination):
    page_size = 5
