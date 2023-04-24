from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.salon.models import Salon, Specialist
from apps.schedule.models import Segment, PlannedSegment, Schedule


class ReadOnlyMixin:
    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False


@admin.register(PlannedSegment)
class PlannedSegmentAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ['date', 'get_start_time', 'get_end_time', 'spec', 'get_is_busy']
    list_filter = ['date', 'spec']
    search_fields = ['spec', 'date']

    def get_start_time(self, obj):
        return obj.segment.start_time

    def get_end_time(self, obj):
        return obj.segment.end_time

    def get_is_busy(self, obj):
        return bool(obj.order)

    get_start_time.short_description = 'Время начала'
    get_end_time.short_description = 'Время окончания'
    get_is_busy.boolean = True
    get_is_busy.short_description = 'Занят?'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('-date', 'spec', 'segment__start_time')
        return queryset


class SalonInlineAdmin(admin.TabularInline):
    model = Salon
    # fk_name = 'company'
    # exclude = ['id', 'created_at', 'updated_at', ]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['date', 'spec', 'work_time_start', 'work_time_end', 'break_time_start',
                    'break_time_end', 'get_salon_schedule_link', 'get_spec_schedule_link']
    ordering = ['-date', 'spec']
    list_filter = ['date', 'spec']

    def get_salon_schedule_link(self, obj):
        display_text = f'<div style="display: flex">' \
                       f'<a href={reverse("schedule_salon")}' \
                       f'?salon={obj.salon.id}&date={obj.date} ' \
                       f'target="_blank" class="button">График салона</a>' \
                       f'</div>'
        return mark_safe(display_text)

    def get_spec_schedule_link(self, obj):
        display_text = f'<div style="display: flex">' \
                       f'<a href={reverse("schedule_spec", kwargs={"pk":obj.spec_id})}' \
                       f'?date={obj.date} target="_blank" class="button">График специалиста</a></div>'
        return mark_safe(display_text)

    get_salon_schedule_link.short_description = 'Графики салона'
    get_spec_schedule_link.short_description = 'Графики специалистов'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            if request.user.profile.salon:
                return queryset.filter(salon=request.user.profile.salon.id)
            return queryset.filter(salon=0)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "salon":
                kwargs["queryset"] = Salon.objects.filter(profile=request.user.profile)
                kwargs['initial'] = Salon.objects.filter(profile=request.user.profile).first()
            if db_field.name == "spec":
                kwargs["queryset"] = Specialist.objects.filter(salons=request.user.profile.salon)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        return {'salon': request.user.profile.salon}


