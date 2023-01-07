from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.service.models import ServiceCategory, Service, Order


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'img_preview', 'title', 'is_publish', 'created_at', 'updated_at']
    fields = ['name', 'img', 'img_preview', 'title', 'text', 'is_publish']
    readonly_fields = ['img_preview']
    list_filter = ['is_publish']
    search_fields = ['name']
    ordering = ['-updated_at']

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="100" />')
        return ""

    img_preview.short_description = 'Изображение'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_publish', 'created_at', 'updated_at']
    fields = ['name', 'price', 'category', 'salons', 'is_publish']
    list_filter = ['category', 'is_publish']
    search_fields = ['name', 'price', 'category']
    ordering = ['-updated_at']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            return queryset.filter(salons=request.user.profile.salon.id)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'salon', 'service', 'spec', 'date', 'is_confirmed',
                    'is_canceled', 'is_completed', 'created_at', 'updated_at']
    fields = ['user', 'salon', 'service', 'spec', 'date', 'is_confirmed',
              'is_canceled', 'is_completed']
    list_filter = ['salon', 'service', 'spec', 'is_confirmed', 'is_canceled', 'is_completed']
    search_fields = ['user', 'salon', 'service', 'spec']
    ordering = ['-updated_at']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            return queryset.filter(salons=request.user.profile.salon.id)
