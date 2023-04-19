from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.salon.models import Salon, SalonImg, Specialist, CompanyInfo, WorkImg, \
    Sale, Review, Order, Messenger, MessengerType, Notification, Faq, MobileAppSection, Store, AppReasons, ConfInfo, \
    ChatsIds, TgSettings, Ceo, HeadScript, BodyScript


class ReadChangeOnlyMixin:
    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False


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
    list_display = ['name', 'img_preview', 'is_social', 'is_publish']
    fields = ['name', 'img_preview', 'img', 'is_social', 'is_publish']
    readonly_fields = ['img_preview']

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="50" />')
        return ""

    img_preview.short_description = 'Иконка'


@admin.register(Messenger)
class MessengerAdmin(admin.ModelAdmin):
    list_display = ['type', 'link', 'salon', 'for_company', 'is_publish']
    fields = ['type', 'link', 'salon', 'for_company', 'is_publish']
    list_filter = ['type', 'is_publish', 'for_company']
    search_fields = ['salon', 'link']
    ordering = ['-updated_at']


@admin.register(CompanyInfo)
class CompanyInfoAdmin(ReadChangeOnlyMixin, admin.ModelAdmin):
    list_display = ['name', 'logo_preview', 'logo_black_preview', 'tagline', 'img_preview', 'about_img_preview',
                    'address', 'phone', 'work_time_start', 'work_time_end', 'is_publish', 'created_at', 'updated_at']
    fields = ['name', 'logo', 'logo_preview', 'logo_black', 'logo_black_preview', 'img',
              'img_preview', 'about_img', 'about_img_preview', 'address', 'phone', 'email',
              'work_time_start', 'work_time_end',  'tagline', 'decs', 'is_publish']
    readonly_fields = ['logo_preview', 'logo_black_preview', 'img_preview', 'about_img_preview']

    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="50" />')
        return ""

    def logo_black_preview(self, obj):
        if obj.logo_black:
            return mark_safe(f'<img src="{obj.logo_black.url}" width="50" />')
        return ""

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="50" />')
        return ""

    def about_img_preview(self, obj):
        if obj.about_img:
            return mark_safe(f'<img src="{obj.about_img.url}" width="50" />')
        return ""

    logo_preview.short_description = 'Превью логотипа'
    logo_black_preview.short_description = 'Превью темного логотипа'
    img_preview.short_description = 'Превью изображения'
    about_img_preview.short_description = 'Превью доп изображения для сайта'


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
    list_display = ['name', 'address', 'phone', 'email', 'work_time_start', 'work_time_end',
                    'is_publish', 'created_at', 'updated_at']
    fields = ['name', 'address', 'phone', 'email', 'work_time_start', 'work_time_end', 'coords',
              'short_desc', 'desc', 'is_publish', 'slug']
    readonly_fields = ['slug']
    inlines = [SalonImgInlineAdmin]
    list_filter = ['name']
    search_fields = ['name', 'address', 'phone', 'email']
    ordering = ['-updated_at']


class WorkImgInlineAdmin(admin.TabularInline):
    model = WorkImg
    fields = ['name', 'img_preview', 'img', 'is_publish']
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
    list_display = ['name', 'photo_preview', 'position', 'is_manager', 'is_publish',
                    'created_at', 'updated_at']
    fields = ['name', 'photo', 'photo_preview', 'position', 'experience', 'title', 'text',
              'services', 'salons', 'is_manager', 'is_publish', ]
    readonly_fields = ['photo_preview']
    inlines = [WorkImgInlineAdmin]
    list_filter = ['is_publish', 'salons', 'is_manager']
    search_fields = ['name']
    ordering = ['-updated_at']

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" />')
        return ""

    photo_preview.short_description = 'Изображение'


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc', 'img_preview', 'get_salons', 'is_publish', 'created_at', 'updated_at']
    fields = ['title', 'desc', 'text', 'button_text', 'img', 'img_preview', 'salons', 'is_publish']
    readonly_fields = ['img_preview']
    list_filter = ['is_publish', 'salons']
    search_fields = ['name']
    ordering = ['-updated_at']

    def img_preview(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="100" />')
        return ""

    def get_salons(self, obj):
        return ", ".join([salon.name for salon in obj.salons.all()])

    img_preview.short_description = 'Изображение'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            if request.user.profile.salon:
                return queryset.filter(salons=request.user.profile.salon.id)
            return queryset.filter(salons=0)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'text', 'salon', 'spec', 'is_publish', 'created_at', 'updated_at']
    fields = ['user', 'rating', 'text', 'salon', 'spec', 'is_publish', ]
    list_filter = ['salon', 'spec', 'rating', 'is_publish']
    search_fields = ['user', 'salon', 'spec']
    ordering = ['-updated_at']
    list_display_links = ['rating']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            if request.user.profile.salon:
                return queryset.filter(salon=request.user.profile.salon.id)
            return queryset.filter(salon=0)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['salon', 'service', 'spec', 'user', 'name', 'phone', 'date',
                    'source', 'status', 'is_processed', 'created_at', 'updated_at']
    fields = ['salon', 'service', 'spec', 'user', 'name', 'phone', 'comment',
              'date', 'start_time', 'end_time', 'source', 'status']
    list_filter = ['salon', 'service', 'spec', 'source', 'status', 'is_processed']
    search_fields = ['user', 'salon', 'service', 'spec', 'name', 'phone']
    ordering = ['-updated_at']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            if request.user.profile.salon:
                return queryset.filter(salon=request.user.profile.salon.id)
            return queryset.filter(salon=0)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'text',  'is_for_salons', 'is_for_users', 'is_publish', 'created_at', 'updated_at']
    fields = ['title', 'text', 'for_salons', 'is_publish', 'for_users']
    list_filter = ['for_salons', 'is_publish']
    search_fields = ['title', 'text']
    filter_horizontal = ['for_users']
    list_display_links = ['title', 'text']

    def is_for_salons(self, obj):
        return bool(obj.for_salons.count())

    def is_for_users(self, obj):
        return bool(obj.for_users.count())

    is_for_salons.boolean = True
    is_for_salons.short_description = "Для салонов"
    is_for_users.boolean = True
    is_for_users.short_description = "Для пользователей"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            if request.user.profile.salon:
                return queryset.filter(for_salons=request.user.profile.salon.id)
            return queryset.filter(for_salons=0)


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'is_publish', 'created_at', 'updated_at']
    fields = ['question', 'answer', 'is_publish']


class StoreInlineAdmin(admin.TabularInline):
    model = Store
    list_display = ['name', 'img', 'link', 'is_publish', 'created_at', 'updated_at']
    fields = ['name', 'img', 'link', 'is_publish']
    extra = 1


class ReasonsInlineAdmin(admin.TabularInline):
    model = AppReasons
    list_display = ['title', 'img', 'text', 'is_publish', 'created_at', 'updated_at']
    fields = ['title', 'img', 'text', 'is_publish', ]
    extra = 1


@admin.register(MobileAppSection)
class MobileAppSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'promo', 'is_publish', 'created_at', 'updated_at']
    fields = ['title', 'text', 'promo', 'img', 'img_for_section', 'is_publish']

    inlines = [StoreInlineAdmin, ReasonsInlineAdmin]


@admin.register(ConfInfo)
class ConfInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_publish', 'created_at', 'updated_at']
    fields = ['title', 'text', 'is_publish']


class TGUserAdmin(admin.TabularInline):
    model = ChatsIds
    fk_name = 'tg_bot'
    exclude = ['id', 'created_at', 'updated_at', ]
    extra = 0


@admin.register(TgSettings)
class TgSettingsAdmin(admin.ModelAdmin):
    list_display = ['salon', 'is_publish', 'created_at', 'updated_at']
    fields = ['salon', 'token', 'is_publish']
    inlines = [TGUserAdmin]


class HeadScriptInline(admin.TabularInline):
    model = HeadScript
    extra = 0
    verbose_name = "Head скрипт"
    verbose_name_plural = "Head скрипты"


class BodyScriptInline(admin.TabularInline):
    model = BodyScript
    extra = 0
    verbose_name = "Body скрипт"
    verbose_name_plural = "Body скрипты"


@admin.register(Ceo)
class CeoAdmin(ReadChangeOnlyMixin, admin.ModelAdmin):
    list_display = ['__str__', 'created_at', 'updated_at']
    fields = ['head']
    inlines = [HeadScriptInline, BodyScriptInline]
