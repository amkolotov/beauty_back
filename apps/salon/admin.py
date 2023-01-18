from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.salon.models import Salon, SalonImg, Specialist, CompanyInfo, WorkImg, \
    Sale, Review, Order, Messenger, MessengerType, Notification


class MessengerInlineCompanyAdmin(admin.TabularInline):
    model = Messenger
    fk_name = 'company'
    exclude = ['id', 'created_at', 'updated_at', ]
    extra = 0


class MessengerInlineSalonAdmin(admin.TabularInline):
    model = Messenger
    fk_name = 'salon'
    exclude = ['id', 'created_at', 'updated_at']
    extra = 0


@admin.register(MessengerType)
class MessengerTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'img_preview', 'is_publish']
    fields = ['name', 'img_preview', 'img', 'is_publish']
    readonly_fields = ['img_preview']

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="50" />')
        return ""

    img_preview.short_description = 'Иконка'


@admin.register(Messenger)
class MessengerAdmin(admin.ModelAdmin):
    list_display = ['type', 'link', 'salon', 'for_company', 'is_publish']
    list_filter = ['type', 'is_publish', 'for_company']
    search_fields = ['salon', 'link']
    ordering = ['-updated_at']


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview', 'tagline', 'img_preview', 'address', 'phone', 'is_publish',
                    'created_at', 'updated_at']
    fields = ['name', 'logo', 'logo_preview', 'img', 'img_preview', 'address',
              'phone', 'email', 'tagline', 'decs', 'is_publish']
    readonly_fields = ['logo_preview', 'img_preview']

    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="50" />')
        return ""

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="50" />')
        return ""

    logo_preview.short_description = 'Превью логотипа'
    img_preview.short_description = 'Превью изображения'


class SalonImgInlineAdmin(admin.TabularInline):
    model = SalonImg
    fields = ['img', 'img_preview', 'is_main', 'is_publish']
    readonly_fields = ['img_preview']
    extra = 0
    ordering = ['is_main', '-updated_at']

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="300" />')
        return ""

    img_preview.short_description = 'Изображение'


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone', 'email', 'is_publish',
                    'created_at', 'updated_at']
    fields = ['name', 'address', 'phone', 'email', 'desc', 'is_publish', ]
    inlines = [SalonImgInlineAdmin]
    list_filter = ['name']
    search_fields = ['name', 'address', 'phone', 'email']
    ordering = ['-updated_at']


class WorkImgInlineAdmin(admin.TabularInline):
    model = WorkImg
    fields = ['name', 'img_preview', 'is_publish']
    readonly_fields = ['img_preview']
    extra = 1
    list_filter = ['is_publish']
    search_fields = ['name']
    ordering = ['-updated_at']

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="100" />')
        return ""

    img_preview.short_description = 'Изображение'


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo_preview', 'position', 'is_publish', 'created_at', 'updated_at']
    fields = ['name', 'photo', 'photo_preview', 'position', 'experience', 'title', 'text',
              'services', 'salons', 'is_publish', ]
    readonly_fields = ['photo_preview']
    inlines = [WorkImgInlineAdmin]
    list_filter = ['is_publish']
    search_fields = ['name']
    ordering = ['-updated_at']

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" />')
        return ""

    photo_preview.short_description = 'Изображение'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            return queryset.filter(salons=request.user.profile.salon.id)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc', 'img_preview', 'is_publish', 'created_at', 'updated_at']
    fields = ['title', 'desc', 'text', 'button_text', 'img', 'img_preview', 'salons', 'is_publish', ]
    readonly_fields = ['img_preview']
    list_filter = ['is_publish']
    search_fields = ['name']
    ordering = ['-updated_at']

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="100" />')
        return ""

    img_preview.short_description = 'Изображение'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            return queryset.filter(salons=request.user.profile.salon.id)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'text', 'salon', 'spec', 'is_publish', 'created_at', 'updated_at']
    fields = ['user', 'rating', 'text', 'salon', 'spec', 'is_publish', ]
    list_filter = ['salon', 'spec', 'rating', 'is_publish']
    search_fields = ['user', 'salon', 'spec']
    ordering = ['-updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['salon', 'service', 'spec', 'user', 'name', 'phone',  'date', 'status',
                    'is_processed', 'created_at', 'updated_at']
    fields = ['salon', 'service', 'spec', 'user', 'name', 'phone', 'date', 'status', 'is_processed']
    list_filter = ['salon', 'service', 'spec', 'status', 'is_processed']
    search_fields = ['user', 'salon', 'service', 'spec', 'name', 'phone']
    ordering = ['-updated_at']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            return queryset.filter(salons=request.user.profile.salon.id)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['text', 'for_salon', 'for_all', 'is_publish', 'created_at', 'updated_at']
    fields = ['text', 'for_salon', 'for_all', 'is_publish', 'for_users']
    list_filter = ['for_salon', 'for_all', 'is_publish']
    search_fields = ['text']

