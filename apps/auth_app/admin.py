from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from apps.auth_app.models import User, Code
from apps.profile.models import Profile

admin.site.site_title = "Beauty"
admin.site.site_header = "Beauty"
# admin.site.unregister(Group)


class ProfileInlineAdmin(admin.TabularInline):
    model = Profile
    readonly_fields = ['avatar_img']
    fields = ['avatar_img', 'avatar', 'salon']


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [
        ProfileInlineAdmin
    ]
    list_display = ['email', 'username', 'phone', 'avatar_img', 'created_at', 'updated_at', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    ordering = ['-updated_at']
    search_fields = ['email', 'username', 'phone']

    def avatar_img(self, obj):
        return obj.profile.avatar_img()

    avatar_img.short_description = 'Аватар'


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass

