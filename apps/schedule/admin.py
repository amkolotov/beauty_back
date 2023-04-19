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
    ordering = ['-date', 'spec']
    list_filter = ['is_busy', 'date', 'spec']
    search_fields = ['spec']

    def get_start_time(self, obj):
        return obj.segment.start_time

    def get_end_time(self, obj):
        return obj.segment.end_time

    get_start_time.short_description = 'Время начала'
    get_end_time.short_description = 'Время окончания'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['date', 'spec', 'work_time_start', 'work_time_end',
                    'break_time_start', 'break_time_end', 'get_schedule_link']
    ordering = ['-date', 'spec']
    list_filter = ['date', 'spec']
    search_fields = ['spec']

    def get_schedule_link(self, obj):
        display_text = f'<a href={reverse("schedule")} target="_blank">Ссылка на график</a>'
        return mark_safe(display_text)

