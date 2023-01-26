from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.service.models import ServiceCategory, Service, AddServiceImg


class AddServiceImgInline(admin.TabularInline):
    model = AddServiceImg
    fk_name = 'service'
    fields = ['img_preview', 'img']
    readonly_fields = ['img_preview']
    extra = 0

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="100" />')
        return ""

    img_preview.short_description = 'Изображение'


# class ServiceInline(admin.TabularInline):
#     model = Service
#     fk_name = 'category'
#     list_display = ['name', 'price', 'category', 'is_publish', 'created_at', 'updated_at']
#     fields = ['name', 'price', 'category', 'salons', 'is_publish']
#     list_filter = ['category', 'is_publish']
#     search_fields = ['name', 'price', 'category']
#     ordering = ['-updated_at']
#     extra = 0
#     filter_horizontal = ['salons']
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         if request.user.is_superuser:
#             return queryset
#         elif request.user.is_staff:
#             return queryset.filter(salons=request.user.profile.salon.id)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'img_preview', 'title', 'is_publish', 'created_at', 'updated_at']
    fields = ['name', 'img', 'img_preview', 'title', 'text', 'is_publish']
    readonly_fields = ['img_preview']
    list_filter = ['is_publish']
    search_fields = ['name']
    ordering = ['-updated_at']
    inlines = [AddServiceImgInline]

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="100" />')
        return ""

    img_preview.short_description = 'Изображение'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_publish', 'created_at', 'updated_at']
    fields = ['name', 'price', 'category', 'salons', 'is_publish']
    list_filter = ['category', 'is_publish', 'salons']
    search_fields = ['name', 'price', 'category']
    ordering = ['-updated_at']

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return queryset
    #     elif request.user.is_staff:
    #         return queryset.filter(salons=request.user.profile.salon.id)



