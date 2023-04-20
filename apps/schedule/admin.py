from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.schedule.models import Segment, PlannedSegment, Schedule


class ReadOnlyMixin:
    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False


@admin.register(PlannedSegment)
class PlannedSegmentAdmin(admin.ModelAdmin):
    list_display = ['date', 'get_start_time', 'get_end_time', 'spec', 'is_busy']
    list_filter = ['is_busy', 'date', 'spec']
    search_fields = ['spec', 'date']

    def get_start_time(self, obj):
        return obj.segment.start_time

    def get_end_time(self, obj):
        return obj.segment.end_time

    get_start_time.short_description = 'Время начала'
    get_end_time.short_description = 'Время окончания'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('-date', 'spec', 'segment__start_time')
        return queryset


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['date', 'spec', 'work_time_start', 'work_time_end', 'break_time_start',
                    'break_time_end', 'get_salon_schedule_link', 'get_spec_schedule_link']
    ordering = ['-date', 'spec']
    list_filter = ['date', 'spec']
    # search_fields = ['spec__name']
    # change_list_template = "schedule/schedule_changelist.html"

    def get_salon_schedule_link(self, obj):
        display_text = f'<div style="display: flex"><a href={reverse("schedule_salon")} target="_blank" class="button">График салона</a></div>'
        return mark_safe(display_text)

    def get_spec_schedule_link(self, obj):
        display_text = f'<div style="display: flex"><a href={reverse("schedule_spec")} target="_blank" class="button">График специалиста</a></div>'
        return mark_safe(display_text)

    get_salon_schedule_link.short_description = 'Графики салона'
    get_spec_schedule_link.short_description = 'Графики специалистов'


