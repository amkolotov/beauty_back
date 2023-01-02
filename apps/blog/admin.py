from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'img_preview', 'salon', 'is_publish', 'created_at', 'updated_at']
    fields = ['title', 'image', 'img_preview', 'text', 'salon', 'is_publish']
    readonly_fields = ['img_preview']
    list_filter = ['salon', 'is_publish']
    search_fields = ['title', 'text', 'salon']
    ordering = ['-updated_at']

    def img_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return ""

    img_preview.short_description = 'Изображение'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            return queryset.filter(salons=request.user.profile.salon.id)

